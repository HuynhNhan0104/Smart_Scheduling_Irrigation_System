from scheduler import *
from mqtt import *
from utils import *
from rs485 import *
import datetime
from enum import Enum
class State(Enum):
    INIT = 0
    IDLE = 1
    MIXER1 = 2
    MIXER2 = 3
    MIXER3 = 4
    PUMP_IN =5
    SELECTOR1  = 6
    SELECTOR2  = 7
    SELECTOR3  = 8
    PUMP_OUT = 9
    
    



    
    
class System:
    state = State.INIT
    modbus485 = Modbus485()
    flow1 = 20
    flow2 = 20
    flow3 = 20
    
    def __init__(self) -> None:
        
        pass
    
    def finite_state_machine(self):
        if self.state == State.INIT:
            pass
        elif self.state == State.MIXER1:
            pass
            
        elif self.state == State.MIXER2:
            pass
            
        elif self.state == State.MIXER3:
            pass
        elif self.state == State.PUMP_IN:
            pass
        elif self.state == State.SELECTOR1:
            
            pass
        elif self.state == State.SELECTOR2:
            
            pass
        elif self.state == State.SELECTOR3:
            
            pass
        elif self.state == State.PUMP_OUT:
            pass
        else:
            pass 
        