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
    is_waiting= False
    
    
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
            if not self.is_waiting:
                self.start_send = time.time()
                print(f"Send: {relay_ON[Relay.MIX1.value-1]}")
                self.modbus485.send_command(relay_ON[Relay.MIX1.value-1])
                self.is_waiting = True
            else:
                reponse = self.modbus485.serial_read_data()
                print(f"Response :{reponse}")
                if reponse:
                    self.is_waiting = False
                    self.state = self.State.MIXER1_WATING
                    print(f"System in state : {self.state.name}")
                    
                else:
                    self.start_send = time.time()
                    self.modbus485.send_command(relay_ON[Relay.MIX1.value-1])
                    
        elif self.state == self.State.MIXER1_WATING:
            current = time.time()
            if current - self.start_send > self.flow1:
                print(f"Send: {relay_OFF[Relay.MIX1.value-1]}")
                self.modbus485.send_command(relay_OFF[Relay.MIX1.value-1])
                self.is_waiting = True
            
            if self.is_waiting:
                reponse = self.modbus485.serial_read_data()
                print(f"Response :{reponse}")
                if reponse == 0:
                    self.is_waiting = False
                    self.state = self.State.MIXER2
                    print(f"System in state : {self.state.name}")
                    
                else:
                    self.modbus485.send_command(relay_OFF[Relay.MIX1.value-1])
                
            
        elif self.state == self.State.MIXER2:
            # response = my_rs485.setDevice(Relay.MIX2,ON)
            self.state = self.State.MIXER2_WATING
            
            
        elif self.state == self.State.MIXER2_WATING:
            pass
        elif self.state == self.State.MIXER3:
            # response = my_rs485.setDevice(Relay.MIX3,ON)
            self.state = self.State.MIXER3_WATING
            
            
        elif self.state == self.State.MIXER3_WATING:
            pass
        
        elif self.state == self.State.PUMP_IN:
            self.state = self.State.SELECTOR1
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
        
    def run(self):
        self.scheduler.SCH_Add_Task(self.finite_state_machine,0,10)
        self.state = self.State.MIXER1_WATING
        self.flow1 = 5
        self.start_send = time.time()
        while True:
            self.scheduler.SCH_Update()                                                                                                        
            self.scheduler.SCH_Dispatch_Tasks()
                                                                                                           
            time.sleep(TICK_CYCLE/1000)
            
            
newSystem = System()
newSystem.run()
    