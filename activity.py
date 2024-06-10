from enum import Enum
import datetime
import json
import time

MAX_ACTIVITIES  = 50
datetime_format = "%H:%M:%S %d-%m-%Y"
class Activity:
    class State(Enum):
        NOT_ACTIVE = 0
        READY = 1
        RUNNING = 2
        FINISH = 3
    def __init__(self, name: str, start_time:str, stop_time: str, flow1: int, flow2: int, flow3: int, 
                selector1: int, selector2: int, selector3: int, 
                pump_in:int, pump_out:int, cycle:int, is_active: int = 1):
        self.name = name
        self.start_time = int(datetime.datetime.strptime(start_time,datetime_format).timestamp())
        self.stop_time = int(datetime.datetime.strptime(stop_time,datetime_format).timestamp() )
        self.flow1 = flow1 
        self.flow2 = flow2 
        self.flow3 = flow3 
        self.selector1 = selector1
        self.selector2 = selector2
        self.selector3 = selector3
        self.pump_in = pump_in
        self.pump_out = pump_out
        self.cycle = cycle
        self.is_active = is_active
        self.state = self.State.READY
        self.id = -1
        
    def create_from_json(self,json_object):
        self.name = json_object.name
        self.start_time = int(datetime.datetime.strptime(json_object.start_time,datetime_format).timestamp())
        self.stop_time = int(datetime.datetime.strptime(json_object.stop_time,datetime_format).timestamp() )
        self.flow1 = json_object.flow1 
        self.flow2 = json_object.flow2 
        self.flow3 = json_object.flow3 
        self.selector1 = json_object.selector1
        self.selector2 = json_object.selector2 
        self.selector3 = json_object.selector3
        self.pump_in = json_object.pump_in
        self.pump_out = json_object.pump_out
        self.cycle = json_object.cycle
        self.is_active = json_object.is_active
        self.state = self.State.READY
        self.id = -1
        
    def to_json(self):
        return{
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active,
            "state": self.state.name,
            "start_time": datetime.datetime.fromtimestamp(self.start_time).strftime(datetime_format),
            "stop_time ": datetime.datetime.fromtimestamp(self.stop_time).strftime(datetime_format),
            "flow1 ": self. flow1,
            "flow2 ": self.flow2,
            "flow3 ": self.flow3,
            "selector1 ": self.selector1,
            "selector2 ": self.selector2,
            "selector3 ": self.selector3,
            "pump_in": self.pump_in,
            "pump_out": self.pump_out,
            "cycle": self.cycle
        }
    def to_string(self):
        return json.dumps(self.to_json(),indent=4)

class ActivityManager:
    def __init__(self):
        self.activitiy_list = []
        self.current_id = 0
        self.current_activity = None 
        self.p_trigger_func = None
        self.p_stop_func = None
    
    def set_trigger_func(self,func):
        self.p_trigger_func = func
        
    def set_stop_func(self,func):
        self.p_trigger_func = func
        # self.current_activity
    def get_current_activity_json(self):
        return self.activitiy_list[0].to_json() if len(self.activitiy_list) > 0 else None
    
    def generate_id(self):
        new_id = self.current_id
        self.current_id += 1
        return new_id
    
    def print_activity_list(self):
        for activity in self.activitiy_list:
            print(activity.to_string())
        
    def add_activity(self,new_activity: Activity):
        new_activity.id = self.generate_id()
        if len(self.activitiy_list) < MAX_ACTIVITIES:
            self.activitiy_list.append(new_activity)
            sorted(self.activitiy_list, key= lambda x: (x.start_time, x.stop_time))
            return new_activity.id
        else:
            print("Activities List is full")
            return -1
            
    def remove_activity(self,activity: Activity):
        if len(self.activitiy_list) > 0:
            self.activitiy_list.remove(activity)
            sorted(self.activitiy_list, key= lambda x: (x.start_time, x.stop_time))
            
        else:
            print("Activities List is empty")
        
    def run_activity(self):
        if len(self.activitiy_list) > 0:
            self.current_activity = self.activitiy_list[0]
            current_time = time.time()
            print("current activity")
            print(self.current_activity.to_string())
            print(f"current time: {current_time}")
            print(f"start time: {self.current_activity.start_time}")
            print(f"stop time: {self.current_activity.stop_time}")
            
            # check thời gian
            if self.current_activity.state == Activity.State.READY:
                #  Thong bao sap dien ra hoat dong tuoi
                if current_time >= self.current_activity.stop_time:
                    print(f"{self.current_activity.name} xoa khoi list vi co loi phat sinh")
                    self.remove_activity(self.current_activity)
                    
                elif current_time < self.current_activity.start_time:
                    delta_time = self.current_activity.start_time - current_time
                    if delta_time <= 60:
                        print(f"{self.current_activity.name} se duoc tien hanh sau {delta_time} s")
                        
                    
                elif current_time >= self.current_activity.start_time:
                    print(f"{self.current_activity.name} dang duoc tien hanh thuc hien")
                    
                    self.current_activity.state = Activity.State.RUNNING
                
                    
            elif self.current_activity.state == Activity.State.RUNNING:
                
                
                
                if current_time < self.current_activity.stop_time:
                    # RUNNING OPERATION HERE
                    self.p_trigger_func()
                    # 
                    delta_time = self.current_activity.stop_time - current_time
                    if delta_time <= 60:
                        print(f"{self.current_activity.name} se duoc ket thuc sau {delta_time} s")
                        
                if current_time >= self.current_activity.stop_time:
                    self.current_activity.state = Activity.State.FINISH
                    
                    print(f"{self.current_activity.name}  kết thúc")
                    
                    
            elif self.current_activity.state == Activity.State.FINISH:
                self.remove_activity(self.current_activity)
                # trigger action to stop
                self.p_stop_func()
                
            elif self.current_activity.state == Activity.State.NOT_ACTIVE:
                pass


# act1 = {
#         # "id": -1,
#         "name": "lich tuoi 1",
#         "is_active": True,
#         # "state": Activity.State.READY.name,
#         "cycle": 1,
#         "start_time": "11:02:00 10-06-2024" ,
#         "stop_time": "11:03:00 10-06-2024",
#         "flow1": 10,
#         "flow2": 10,
#         "flow3": 10,
#         "selector": 1,
#     }
# act1 = Activity(**act1)
# act2 = {
#         # "id": -1,
#         "name": "lich tuoi 2",
#         "is_active": True,
#         # "state": Activity.State.READY.name,
#         "cycle": 1,
#         "start_time": "11:04:00 10-06-2024",
#         "stop_time": "11:05:00 10-06-2024",
#         "flow1": 10,
#         "flow2": 10,
#         "flow3": 10,
#         "selector": 1,
#     }
# act2 = Activity(**act2)

# manager = ActivityManager()
# manager.add_activity(act1)
# manager.add_activity(act2)


# while True:
#     try:
#         manager.run_activity()
#         time.sleep(0.1)
#     except KeyboardInterrupt:
#         break
        
    
            
            
