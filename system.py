from scheduler import *
from mqtt import *
from utils import *
from rs485 import *
from mqtt import *
from activity import *
import datetime
from enum import Enum


ON = 1
OFF = 0
    
class Relay(Enum):
    MIX1 = 1
    MIX2 = 2
    MIX3 = 3
    AREA1 = 4
    AREA2 = 5
    AREA3 = 6
    PUMP_IN = 7
    PUMP_OUT = 8
    
    
    
class System:
    class State(Enum):
        INIT = 0
        IDLE = 1
        MIXER1 = 2              #<----- Starting
        MIXER1_WATING = 3       #<----- Running
        
        MIXER2 = 4              #<----- Starting
        MIXER2_WATING = 5       #<----- Running
        
        MIXER3 = 6              #<----- Starting
        MIXER3_WATING = 7       #<----- Running
        
        PUMP_IN = 8             #<----- Starting
        PUMP_IN_WAITING = 9     #<----- Running
        
        SELECTOR1  = 10         #<----- Starting
        SELECTOR2  = 11         #<----- Starting
        SELECTOR3  = 12         #<----- Starting
        
        PUMP_OUT = 13           #<----- Starting
        PUMP_OUT_WAITING = 14   #<----- Running
        
        NEXT_CYCLE_WAITING = 15 #<----- Starting
        
    state = State.INIT
    trigger = False
    is_waiting_response= False
    
    
    modbus485 = Modbus485()
    # mqtt_handler = MQTTHelper()
    scheduler = Scheduler()
    activity_manager = ActivityManager()
    
    flow1 = 20
    flow2 = 20
    flow3 = 20
    area_selector1 = 20
    area_selector2 = 20
    area_selector3 = 20
    pump_in = 10
    pump_out = 10
    cycle = 0
    
    start_send = time.time()
    
    def __init__(self) -> None:
        self.activity_manager.set_trigger_func(self.trigger_action)
        self.activity_manager.set_stop_func(self.stop_action)
        # self.mqtt_handler.setRecvCallBack(self.receive_message)
        
    
    def trigger_action(self):
        acitivity = self.activity_manager.get_current_activity_json()
        print(acitivity.to_string())
        if acitivity:
            kwargs = {
                "flow1 ": acitivity.get("flow1"),
                "flow2 ": acitivity.get("flow2"),
                "flow3 ": acitivity.get("flow3"),
                "selector1 ": acitivity.get("selector1"),
                "selector2 ": acitivity.get("selector2"),
                "selector3 ": acitivity.get("selector3"),
                "pump_in": acitivity.get("pump_in"),
                "pump_out": acitivity.get("pump_out"),
                "cycle": acitivity.get("cycle")
            }
            self.set_config(**kwargs)
        self.state = self.State.IDLE
        self.trigger = True
        
            
        
        
    def set_config(self,flow1: int, flow2: int, flow3: int, 
                   selector1: int, selector2: int, selector3: int, 
                   cycle:int, punp_in:int, punp_out:int):
        self.flow1 = flow1
        self.flow2 = flow2
        self.flow3 = flow3
        self.area_selector1 = selector1
        self.area_selector2 = selector2
        self.area_selector3 = selector3
        self.pump_in = punp_in
        self.pump_out = punp_out
        self.cycle = cycle
        
        
        
    
    def stop_action(self):
        pass
    
    def receive_message(self,payload):
        pass
    
    def send_command_reliable(self, command, expected_value):
            # self.start_send = time.time()
            self.modbus485.send_command(command)
            reponse = None
            while reponse := self.modbus485.serial_read_data():
                if reponse == expected_value:
                    return
                self.modbus485.send_command(command)
                
                
                
    def send_command_reliable_and_to_next_state(self, command,next_state):
        if not self.is_waiting_response:
            self.start_send = time.time()
            print(f"Send: {command}")
            self.modbus485.send_command(command)
            self.is_waiting_response = True
        else:
            reponse = self.modbus485.serial_read_data()
            print(f"Response :{reponse}")
            if reponse:
                self.is_waiting_response = False
                self.state = next_state
                print(f"System in state : {next_state}")
            else:
                self.start_send = time.time()
                self.modbus485.send_command(command)
                
                
    def timeout_callback_to_stop(self, duration, off_commamd, next_state):
        current = time.time()
        if not self.is_waiting_response:
            if current - self.start_send > duration:
                print(f"delta = {current - self.start_send}")
                print(f"Send: {off_commamd}")
                self.modbus485.send_command(off_commamd)
                self.is_waiting_response = True
        else :        
            reponse = self.modbus485.serial_read_data()
            print(f"Response :{reponse}")
            if reponse == 0:
                self.is_waiting_response = False
                self.state = next_state
                print(f"System in state : {next_state}")
            else:
                self.modbus485.send_command(off_commamd)
                
    def finite_state_machine(self):
        if self.state == self.State.INIT:
            print("System Initial...")
            self.state = self.State.IDLE
        elif self.state == self.State.IDLE:
            if self.trigger:
                self.state = self.State.MIXER1 
                
        elif self.state == self.State.MIXER1:
            self.send_command_reliable_and_to_next_state(relay_ON[Relay.MIX1.value-1], self.State.MIXER1_WATING)
                    
        elif self.state == self.State.MIXER1_WATING:
            self.timeout_callback_to_stop(self.flow1,relay_OFF[Relay.MIX1.value-1],self.State.MIXER2)
            
        elif self.state == self.State.MIXER2:
            self.send_command_reliable_and_to_next_state(relay_ON[Relay.MIX2.value-1], self.State.MIXER2_WATING)
            
        elif self.state == self.State.MIXER2_WATING:
            self.timeout_callback_to_stop(self.flow2,relay_OFF[Relay.MIX2.value-1],self.State.MIXER3)
                    
        elif self.state == self.State.MIXER3:
            self.send_command_reliable_and_to_next_state(relay_ON[Relay.MIX3.value-1], self.State.MIXER3_WATING)
            
        elif self.state == self.State.MIXER3_WATING:
            self.timeout_callback_to_stop(self.flow3,relay_OFF[Relay.MIX3.value-1],self.State.PUMP_IN)
            
        elif self.state == self.State.PUMP_IN:
            self.send_command_reliable_and_to_next_state(relay_ON[Relay.PUMP_IN.value-1],self.State.PUMP_IN_WAITING)
            
        elif self.state == self.State.PUMP_IN_WAITING:
            self.timeout_callback_to_stop(self.pump_in,relay_OFF[Relay.PUMP_IN.value-1], self.State.SELECTOR1)
            
        elif self.state == self.State.SELECTOR1:
            if self.area_selector1:
                self.send_command_reliable_and_to_next_state(relay_ON[Relay.AREA1.value-1],self.State.SELECTOR2)
            else:
                self.state =self.State.SELECTOR2
        
        elif self.state == self.State.SELECTOR2:
            if self.area_selector2:
                self.send_command_reliable_and_to_next_state(relay_ON[Relay.AREA2.value-1],self.State.SELECTOR3)
            else:
                self.state =self.State.SELECTOR3
        
        elif self.state == self.State.SELECTOR3:
            if self.area_selector3:
                self.send_command_reliable_and_to_next_state(relay_ON[Relay.AREA3.value-1],self.State.PUMP_OUT)
            else:
                self.state =self.State.PUMP_OUT
                
        elif self.state == self.State.PUMP_OUT:
            self.send_command_reliable_and_to_next_state(relay_ON[Relay.PUMP_OUT.value-1],self.State.PUMP_OUT_WAITING)
            
        elif self.state == self.State.PUMP_OUT_WAITING:
            self.timeout_callback_to_stop(self.pump_out, relay_OFF[Relay.PUMP_IN.value-1],self.State.NEXT_CYCLE_WAITING)
            
        elif self.state == self.State.NEXT_CYCLE_WAITING:
            print("TURN OFF AREA ", Relay.AREA1.value)
            self.send_command_reliable(relay_OFF[Relay.AREA1.value-1],0)
            print("TURN OFF AREA ", Relay.AREA2.value)
            self.send_command_reliable(relay_OFF[Relay.AREA2.value-1],0)
            print("TURN OFF AREA ", Relay.AREA3.value)
            self.send_command_reliable(relay_OFF[Relay.AREA3.value-1],0)
            
            if self.cycle > 0:
                self.state = self.State.MIXER1
                self.cycle -= 1
            else:                
                self.state = self.State.IDLE
                print(f"System in state : {self.state}")
                
        else:
            print(f"SYSTEM IN ERROR: {self.state}")
        

                
    def run(self):
        act2 = {
                # "id": -1,
                "name": "lich tuoi 2",
                "is_active": True,
                # "state": Activity.State.READY.name,
                "start_time": "19:55:00 10-06-2024",
                "stop_time": "19:54:00 10-06-2024",
                "flow1": 5,
                "flow2": 5,
                "flow3": 5,
                "selector1": 1,
                "selector2": 1,
                "selector3": 1,
                "pump_in":5,
                "pump_out":5,
                "cycle": 1
        }
        act2 = Activity(**act2)
        self.activity_manager.add_activity(act2)
        self.scheduler.SCH_Add_Task(self.finite_state_machine,0,10)
        self.scheduler.SCH_Add_Task(self.activity_manager.run_activity,0,10)
        self.state = self.State.MIXER1
        self.flow1 = 5
        self.flow2 = 5
        self.flow3 = 5
        self.pump_in = 5
        self.pump_out = 5
        self.area_selector1 = 1
        self.area_selector2 = 1
        self.area_selector3 = 1
        self.cycle = 3
        
        # self.start_send = time.time()
        while True:
            self.scheduler.SCH_Update()                                                                                                        
            self.scheduler.SCH_Dispatch_Tasks()
            
                                                                                                           
            time.sleep(TICK_CYCLE/1000)
            
            
newSystem = System()
newSystem.run()
    