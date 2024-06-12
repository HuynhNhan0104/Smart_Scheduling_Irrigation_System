from queue import Queue
# from system import IrrigationSystem
import time
import datetime
from threading import Thread
from enum import Enum
import json


def print_current_datetime():
    current_datetime = datetime.datetime.now()
    # print(type(current_daytime))
    current_str = current_datetime.strftime('%H:%M:%S %d-%m-%Y')
    print(f"Function working at: {current_str}")
def print_my_name(name):
    print("My name is: ", name)
class Task:
    pTask = None
    Delay = 0                                                                                                                            
    Period = 0                                                                                                                           
    RunMe = 0                   # set state of sched: 1 -> 0 -> Run pTask (pTask is a pointer function)
    TaskID = -1 
    args = None     
    kwargs = None
    
    def __init__(self, _pTask,_Delay, _Period, *args,  **kwargs ):
        self.pTask = _pTask                                                                                                              
        self.Delay = _Delay                                                                                                              
        self.Period = _Period
        self.args = args
        self.kwargs = kwargs    
        
    def to_string(self):
        json_object ={
            "id" : self.TaskID,
            "period" : self.Period  
        }  
        return json.dumps(json_object,indent=4)                                                                                                      
                                                                                                                                         
    
    
    def run(self):
        return self.pTask(*self.args,**self.kwargs)                                                                                                                    
    
# QUEUE = 1                                                                                                                                
TICK_CYCLE = 10       
print(f"Tick cycle is {TICK_CYCLE} ms or {TICK_CYCLE/1000} s")                                                                                                                   

class Scheduler:
    TICK = 10
    SCH_MAX_TASKS = 40
    SCH_tasks_G = []
    current_index_task = 0
    current_id = 0

    def __int__(self):
        return

    def SCH_Init(self):
        self.current_index_task = 0

    def SCH_Add_Task(self, pFunction, DELAY, PERIOD,*args,  **kwargs):
        if self.current_index_task < self.SCH_MAX_TASKS:
            aTask = Task(pFunction, DELAY / self.TICK, PERIOD / self.TICK,*args,  **kwargs)
            aTask.TaskID = self.SCH_GenerateID()
            self.SCH_tasks_G.append(aTask)
            self.current_index_task += 1
            print("Added task at ID:" + str(aTask.TaskID))
            return aTask
        else:
            return -1
            
            print("PrivateTasks are full!!!")
            
    def SCH_Add_Task_with_specific_time(self, pFunction,datetime_str,datetime_format,period = 0,*args,  **kwargs):
        try:
            expected_datetime = datetime.datetime.strptime(datetime_str,datetime_format)
            excepted_timestamp = expected_datetime.timestamp()
            current_timestamp = time.time()
            differ_time = excepted_timestamp - current_timestamp
            if differ_time >= 0:
                return self.SCH_Add_Task(pFunction,differ_time*1000, period*1000 ,*args, **kwargs)
            else:
                print("ERROR: TIME SUPPLY IS NOT VALID!")
                return -1
        except Exception as e:
            print(e)
            return -1

    def SCH_Update(self):
        for i in range(len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].Delay > 0:
                self.SCH_tasks_G[i].Delay -= 1
            else:
                self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period
                self.SCH_tasks_G[i].RunMe += 1

    def SCH_Dispatch_Tasks(self):
        for i in range(len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].RunMe > 0:
                
                self.SCH_tasks_G[i].RunMe -= 1
                self.SCH_tasks_G[i].run()
                if self.SCH_tasks_G[i].Period == 0:
                    self.SCH_Delete(self.SCH_tasks_G[i])
                    break

    def SCH_Delete(self, aTask):
        # for i in range(0, len(self.SCH_tasks_G)):
        #     if self.SCH_tasks_G[i].TaskID == aTask.TaskID :
        #         print("Deleted task at ID:" + str(self.SCH_tasks_G[i].TaskID))
        #         self.SCH_tasks_G.pop(i)   
        #         self.current_index_task -= 1
        #         self.SCH_GenerateID()
        #         break
        # return
        if aTask in self.SCH_tasks_G:
            self.SCH_tasks_G.remove(aTask)
            self.current_index_task -= 1
            # self.SCH_GenerateID()
            # print(aTask.to_string())
            

    def SCH_GenerateID(self):
        new_id = self.current_id 
        self.current_id += 1
        return new_id
        
                                                                                                                                

# class TaskManagament:
#     def __init__(self):
#         self.scheduler_run = True
#         self.scheduler = Scheduler()                                                                                                         
#         self.scheduler.SCH_Init()                                                                                                            
#         # self.system = IrrigationSystem()                                                                                                     
#     def remove_task(self,task):
#         self.scheduler.SCH_Delete(task)

#     def run(self):
#         # self.scheduler.SCH_Add_Task(self.system.run_irrigation, 0, 1000)                                                                     
#         # self.scheduler.SCH_Add_Task(self.system.control_pump, 1000, 3000)                                                                    
#         try:
#             # self.scheduler.SCH_Add_Task(self.system.readSensor, 0, 1000) 
#             self.scheduler.SCH_Add_Task(Say_hello, 0, 0)     
#             task = self.scheduler.SCH_Add_Task(print_my_name,0,1000,name = "Nhan")    
#             # self.scheduler.SCH_Add_Task(self.remove_task,1000,0,task = task)                                                              
                                                                    
#             # self.system.cloud.connect()                                                                                                        
#         except Exception as e:
#             print("Error: ", e)
            
        
            
            
#         while self.scheduler_run:
#             self.scheduler.SCH_Update()                                                                                                        
#             self.scheduler.SCH_Dispatch_Tasks()                                                                                                
#             time.sleep(TICK_CYCLE/1000)


# def Say_hello():
#     print("-----------------System Starting----------------")

# # my_scheduler = TaskManagament()
# # my_scheduler.run()



