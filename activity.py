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
    def __init__(self, name: str, start_time:str, stop_time: str, flow1: int, flow2: int, flow3: int, selector: int, cycle:int, is_active: int = 1):
        self.name = name
        self.start_time = int(datetime.datetime.strptime(start_time,datetime_format).timestamp())
        self.stop_time = int(datetime.datetime.strptime(stop_time,datetime_format).timestamp() )
        self.flow1 = flow1 
        self.flow2 = flow2 
        self.flow3 = flow3 
        self.selector = selector
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
        self.selector = json_object.selector
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
            "cycle": self.cycle,
            "start_time": datetime.fromtimestamp(self.start_time).strftime(datetime_format),
            "stop_time ": datetime.fromtimestamp(self.stop_time_time).strftime(datetime_format),
            "flow1 ": self. flow1,
            "flow2 ": self.flow2,
            "flow3 ": self.flow3,
            "selector ": self.selector,
        }
    def to_string(self):
        return json.dumps(self.to_json(),indent=4)

class ActivityManager:
    def __init__(self):
        self.activitiy_list = []
        self.current_id = 0
        # self.current_activity
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
        
    def run_activity(self,scheduler=None):
        if len(self.activitiy_list) > 0:
            current_activity = self.activitiy_list[0]
            current_time = time.time()
            
            # check thời gian
            if current_activity.state == Activity.State.READY:
                #  Thong bao sap dien ra hoat dong tuoi
                if current_time > current_activity.stop_time:
                    print(f"{current_activity.name} xoa khoi list vi co loi phat sinh")
                    self.remove_activity(current_activity)
                    
                if current_time < current_activity.start_time:
                    delta_time = current_activity.start_time - current_time
                    if delta_time <= 60:
                        print(f"{current_activity.name} se duoc tien hanh sau {delta_time} s")
                        
                    
                if current_time >= current_activity.start_time:
                    print(f"{current_activity.name} dang duoc tien hanh thuc hien")
                    
                    current_activity.state = Activity.State.RUNNING
                
                    
            elif current_activity.state == Activity.State.RUNNING:
                
                
                
                if current_time < current_activity.stop_time:
                    # RUNNING OPERATION HERE
                    # 
                    delta_time = current_activity.stop_time - current_time
                    if delta_time <= 60:
                        print(f"{current_activity.name} se duoc ket thuc sau {delta_time} s")
                        
                if current_time >= current_activity.stop_time:
                    current_activity.state = Activity.State.FINISH
                    
                    print(f"{current_activity.name}  kết thúc")
                    
                    
            elif current_activity.state == Activity.State.FINISH:
                self.remove_activity(current_activity)
                # trigger action to stop
                
            elif current_activity.state == Activity.State.NOT_ACTIVE:
                pass


act1 = {
        # "id": -1,
        "name": "lich tuoi 1",
        "is_active": True,
        # "state": Activity.State.READY.name,
        "cycle": 1,
        "start_time": "11:02:00 10-06-2024" ,
        "stop_time": "11:03:00 10-06-2024",
        "flow1": 10,
        "flow2": 10,
        "flow3": 10,
        "selector": 1,
    }
act1 = Activity(**act1)
act2 = {
        # "id": -1,
        "name": "lich tuoi 2",
        "is_active": True,
        # "state": Activity.State.READY.name,
        "cycle": 1,
        "start_time": "11:04:00 10-06-2024",
        "stop_time": "11:05:00 10-06-2024",
        "flow1": 10,
        "flow2": 10,
        "flow3": 10,
        "selector": 1,
    }
act2 = Activity(**act2)

manager = ActivityManager()
manager.add_activity(act1)
manager.add_activity(act2)


while True:
    try:
        manager.run_activity()
        time.sleep(0.1)
    except KeyboardInterrupt:
        break
        
    
            
            