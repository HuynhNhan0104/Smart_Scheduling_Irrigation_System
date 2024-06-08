from queue import Queue
# from system import IrrigationSystem
import time
import datetime
from threading import Thread
class Task:
    def __init__(self, _pTask, _Delay, _Period):
        self.pTask = _pTask                                                                                                              
        self.Delay = _Delay                                                                                                              
        self.Period = _Period                                                                                                            
                                                                                                                                         
    pTask = None
    Delay = 0                                                                                                                            
    Period = 0                                                                                                                           
    RunMe = 0                   # set state of sched: 1 -> 0 -> Run pTask (pTask is a pointer function)
    TaskID = -1                                                                                                                          
    
# QUEUE = 1                                                                                                                                
TICK_CYCLE = 10       
print(f"Tick cycle is {TICK_CYCLE} ms or {TICK_CYCLE/1000} s")                                                                                                                   
# q = Queue()    
                                                                                                                          
class Scheduler:
    TICK = TICK_CYCLE                 
    SCH_MAX_TASKS = 40          
    SCH_tasks_G = []            # List task (type list)
    current_index_task = 0      # total number task current 
    def __int__(self):
      return
                                                                                                                                         
    def SCH_Init(self):
      self.current_index_task = 0                                                                                                        
      
    def SCH_Add_Task(self, pFunction, DELAY, PERIOD):
      if self.current_index_task < self.SCH_MAX_TASKS:
        aTask = Task(pFunction, DELAY / self.TICK, PERIOD / self.TICK)                                                                   
        aTask.TaskID = self.current_index_task                                                                                           
        self.SCH_tasks_G.append(aTask)                                                                                                   
        self.current_index_task += 1                                                                                                     
      else:
        print("PrivateTasks are full!!!")
        
    def SCH_Add_Task_with_specific_time(self, pFunction,datetime_str,datetime_format,cycle = 0):
        try:
            expected_datetime = datetime.datetime.strptime(datetime_str,datetime_format)
            excepted_timestamp = expected_datetime.timestamp()
            current_timestamp = time.time()
            differ_time = excepted_timestamp - current_timestamp
            if differ_time >= 0:
                self.SCH_Add_Task(pFunction,differ_time*1000,10*1000)
            else:
                print("ERROR: TIME SUPPLY IS NOT VALID!")
        except Exception as e:
            print(e)
      
                                                                                                                                            
    def SCH_Update(self):
        for i in range(0, len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].Delay > 0:
                self.SCH_tasks_G[i].Delay -= 1                                                                                                 
            else:
                self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period                                                                         
                self.SCH_tasks_G[i].RunMe += 1   
                                                                                                            
    def SCH_Dispatch_Tasks(self):
        deleteArr=[]                                                                                                                       
        for i in range(0, len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].RunMe > 0:
                self.SCH_tasks_G[i].RunMe -= 1                                                                                                 
                self.SCH_tasks_G[i].pTask()                                                                                                    
            if self.SCH_tasks_G[i].Period == 0 :
                deleteArr.append(self.SCH_tasks_G[i])                                                                                        
            # self.SCH_Delete(self.SCH_tasks_G[i])
            # self.SCH_Dispatch_Tasks()
            # break        
        for i in range(0,len(deleteArr)):
            self.SCH_Delete(deleteArr[i])                                                                                                    
                                                                                                                                            
    def SCH_Delete(self, aTask):
        if aTask in self.SCH_tasks_G:
            self.SCH_tasks_G.remove(aTask)                                                                                                   
            self.current_index_task -= 1  

    def SCH_Detele_All(self):
        pass  
                                                                                                                                            
    def SCH_GenerateID(self):
        return -1
class TaskManagament:
  def __init__(self):
    self.scheduler_run = True
    self.scheduler = Scheduler()                                                                                                         
    self.scheduler.SCH_Init()                                                                                                            
    # self.system = IrrigationSystem()                                                                                                     
    
  def run(self):
    # self.scheduler.SCH_Add_Task(self.system.run_irrigation, 0, 1000)                                                                     
    # self.scheduler.SCH_Add_Task(self.system.control_pump, 1000, 3000)                                                                    
    try:
        # self.scheduler.SCH_Add_Task(self.system.readSensor, 0, 1000) 
        self.scheduler.SCH_Add_Task(Say_hello, 0, 0)                                                                   
        # self.system.cloud.connect()                                                                                                        
    except Exception as e:
        print("Error: ", e)
        
    while self.scheduler_run:
      self.scheduler.SCH_Update()                                                                                                        
      self.scheduler.SCH_Dispatch_Tasks()                                                                                                
      time.sleep(TICK_CYCLE/1000)


def Say_hello():
    print("-----------------System Starting----------------")




# try: 
#     my_scheduler = TaskManagament()
#     my_scheduler.run()

# except KeyboardInterrupt:
#     my_scheduler.run = False