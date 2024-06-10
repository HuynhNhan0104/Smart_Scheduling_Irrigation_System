from scheduler import *
from mqtt import *
from utils import *
from rs485 import *
from mqtt import *
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
        MIXER1 = 2
        MIXER1_WATING = 3
        
        MIXER2 = 4
        MIXER2_WATING = 5
        
        MIXER3 = 6
        MIXER3_WATING = 7
        
        PUMP_IN = 8
        SELECTOR1  = 9
        SELECTOR2  = 10
        SELECTOR3  = 11
        PUMP_OUT = 12
        CYCLE = 13
        
    state = State.INIT
    trigger = False
    is_waiting_response= False
    
    
    modbus485 = Modbus485()
    # mqtt_handler = MQTTHelper()
    scheduler = Scheduler()
    
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
        
        pass
    
    def finite_state_machine(self):
        if self.state == self.State.INIT:
            print("System Initial...")
            self.state = self.State.IDLE
            
        elif self.state == self.State.IDLE:
            # if (True):
            if self.trigger:
                self.state = self.State.MIXER1 
                # self.scheduler.SCH_Add_Task(self.modbus485.setDevice,0,0,Relay.MIX1,ON)
                # self.scheduler.SCH_Add_Task(self.modbus485.setDevice,0,self.flow1*1000,Relay.MIX1,OFF)
            
        elif self.state == self.State.MIXER1:
            # sending command an check response
            # if not self.is_waiting_response:
            #     self.start_send = time.time()
            #     print(f"Send: {relay_ON[Relay.MIX1.value-1]}")
            #     self.modbus485.send_command(relay_ON[Relay.MIX1.value-1])
            #     self.is_waiting_response = True
            # else:
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER1_WATING
            #         print(f"System in state : {self.state.name}")
                    
            #     else:
            #         self.start_send = time.time()
            #         self.modbus485.send_command(relay_ON[Relay.MIX1.value-1])
            self.send_command_reliable(relay_ON[Relay.MIX1.value-1], self.State.MIXER1_WATING)
                    
        elif self.state == self.State.MIXER1_WATING:
            # current = time.time()
            # if not self.is_waiting_response:
            #     if current - self.start_send > self.flow1:
            #         print(f"delta = {current - self.start_send}")
            #         print(f"Send: {relay_OFF[Relay.MIX1.value-1]}")
            #         self.modbus485.send_command(relay_OFF[Relay.MIX1.value-1])
            #         self.is_waiting_response = True
            # else :        
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse == 0:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER2
            #         print(f"System in state : {self.state.name}")
                    
            #     else:
            #         self.modbus485.send_command(relay_OFF[Relay.MIX1.value-1])
            self.timeout_callback_to_stop(self.flow1,relay_OFF[Relay.MIX1.value-1],self.State.MIXER2)
            
                
            
                
            
        elif self.state == self.State.MIXER2:
            # response = my_rs485.setDevice(Relay.MIX2,ON)
            # self.state = self.State.MIXER2_WATING
            # sending command an check response
            # if not self.is_waiting_response:
            #     self.start_send = time.time()
            #     print(f"Send: {relay_ON[Relay.MIX2.value-1]}")
            #     self.modbus485.send_command(relay_ON[Relay.MIX2.value-1])
            #     self.is_waiting_response = True
            # else:
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER2_WATING
            #         print(f"System in state : {self.state.name}")
            #     else:
            #         self.start_send = time.time()
            #         self.modbus485.send_command(relay_ON[Relay.MIX2.value-1])
            self.send_command_reliable(relay_ON[Relay.MIX2.value-1], self.State.MIXER2_WATING)
            
            
            
        elif self.state == self.State.MIXER2_WATING:
            # current = time.time()
            # if not self.is_waiting_response:
            #     if current - self.start_send > self.flow2:
            #         print(f"delta = {current - self.start_send}")
            #         print(f"Send: {relay_OFF[Relay.MIX2.value-1]}")
            #         self.modbus485.send_command(relay_OFF[Relay.MIX2.value-1])
            #         self.is_waiting_response = True
            # else :        
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse == 0:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER3
            #         print(f"System in state : {self.state.name}")
                    
            #     else:
            #         self.modbus485.send_command(relay_OFF[Relay.MIX2.value-1])
            self.timeout_callback_to_stop(self.flow2,relay_OFF[Relay.MIX2.value-1],self.State.MIXER3)
                    
        elif self.state == self.State.MIXER3:
            # response = my_rs485.setDevice(Relay.MIX3,ON)
            # self.state = self.State.MIXER3_WATING
            # if not self.is_waiting_response:
            #     self.start_send = time.time()
            #     print(f"Send: {relay_ON[Relay.MIX3.value-1]}")
            #     self.modbus485.send_command(relay_ON[Relay.MIX3.value-1])
            #     self.is_waiting_response = True
            # else:
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER3_WATING
            #         print(f"System in state : {self.state.name}")
            #     else:
            #         self.start_send = time.time()
            #         self.modbus485.send_command(relay_ON[Relay.MIX3.value-1])
            self.send_command_reliable(relay_ON[Relay.MIX3.value-1], self.State.MIXER3_WATING)
            
            
            
        elif self.state == self.State.MIXER3_WATING:
            # current = time.time()
            # if not self.is_waiting_response:
            #     if current - self.start_send > self.flow3:
            #         print(f"delta = {current - self.start_send}")
            #         print(f"Send: {relay_OFF[Relay.MIX3.value-1]}")
            #         self.modbus485.send_command(relay_OFF[Relay.MIX3.value-1])
            #         self.is_waiting_response = True
            # else :        
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse == 0:
            #         self.is_waiting_response = False
            #         self.state = self.State.PUMP_IN
            #         print(f"System in state : {self.state.name}")
                    
            #     else:
            #         self.modbus485.send_command(relay_OFF[Relay.MIX3.value-1])
            self.timeout_callback_to_stop(self.flow3,relay_OFF[Relay.MIX3.value-1],self.State.PUMP_IN)
            
        elif self.state == self.State.PUMP_IN:
            # self.state = self.State.SELECTOR1
            # if not self.is_waiting_response:
            #     self.start_send = time.time()
            #     print(f"Send: {relay_ON[Relay.PUMP_IN.value-1]}")
            #     self.modbus485.send_command(relay_ON[Relay.PUMP_IN.value-1])
            #     self.is_waiting_response = True
            # else:
            #     reponse = self.modbus485.serial_read_data()
            #     print(f"Response :{reponse}")
            #     if reponse:
            #         self.is_waiting_response = False
            #         self.state = self.State.MIXER2_WATING
            #         print(f"System in state : {self.state.name}")
            #     else:
            #         self.start_send = time.time()
            #         self.modbus485.send_command(relay_ON[Relay.PUMP_IN.value-1])
            # pass
            # self.send_command_reliable()
            pass
        
        elif self.state == self.State.SELECTOR1:
            self.state = self.State.SELECTOR2
            pass
        
        elif self.state == self.State.SELECTOR2:
            self.state = self.State.SELECTOR3
            pass
        
        elif self.state == self.State.SELECTOR3:
            self.state = self.State.PUMP_OUT
            pass
        
        elif self.state == self.State.PUMP_OUT:
            pass
        else:
            pass 
        
    def send_command_reliable(self, command,next_state):
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
                
                
    def timeout_callback_to_stop(self, flow, off_commamd, next_state):
        current = time.time()
        if not self.is_waiting_response:
            if current - self.start_send > flow:
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
                
    def run(self):
        self.scheduler.SCH_Add_Task(self.finite_state_machine,0,10)
        self.state = self.State.MIXER1
        self.flow1 = 5
        self.flow2 = 5
        self.flow3 = 5
        
        # self.start_send = time.time()
        while True:
            self.scheduler.SCH_Update()                                                                                                        
            self.scheduler.SCH_Dispatch_Tasks()
                                                                                                           
            time.sleep(TICK_CYCLE/1000)
            
            
newSystem = System()
newSystem.run()
    