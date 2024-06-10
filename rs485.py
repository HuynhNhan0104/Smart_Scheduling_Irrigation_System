# cd ~/Desktop/IOT232_L01/2013961/Smart_Scheduling_Irrigation_System
print("Sensors and Actuators")

relay_ON = [
    [1, 6, 0, 0, 0, 255, 201, 138   ],
    [2, 6, 0, 0, 0, 255, 201, 185   ],
    [3, 6, 0, 0, 0, 255, 200, 104   ],
    [4, 6, 0, 0, 0, 255, 201, 223   ],
    [5, 6, 0, 0, 0, 255, 200, 14    ],
    [6, 6, 0, 0, 0, 255, 200, 61    ],
    [7, 6, 0, 0, 0, 255, 201, 236   ],
    [8, 6, 0, 0, 0, 255, 201, 19    ]
]
relay_OFF = [
    [1, 6, 0, 0, 0, 0, 137, 202 ],
    [2, 6, 0, 0, 0, 0, 137, 249 ],
    [3, 6, 0, 0, 0, 0, 136, 40  ],
    [4, 6, 0, 0, 0, 0, 137, 159 ],
    [5, 6, 0, 0, 0, 0, 136, 78  ],
    [6, 6, 0, 0, 0, 0, 136, 125 ],
    [7, 6, 0, 0, 0, 0, 137, 172 ],
    [8, 6, 0, 0, 0, 0, 137, 83  ]
]

soil_temperature = [10, 3, 0, 6, 0, 1, 101, 112]
soil_humidity = [10, 3, 0, 7, 0, 1, 52, 176]
distance1_ON = [9, 3, 0, 5, 0, 1, 149, 67]
distance2_ON = [12, 3, 0, 5, 0, 1, 149, 22]

valve_controll_message = ''

import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

# portName = "/dev/ttyUSB0"
# print(portName)

port_available = getPort()
print(port_available)
class Modbus485:
    ser = None
    def __init__(self, portName = "/dev/ttyUSB0", baudrate = 9600):
        try:
            self.ser = serial.Serial(port=portName, baudrate=9600)
            print("Open successfully")
        except:
            print("Can not open the port")

    # relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
    # relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]
    def send_command(self, command):
        self.ser.write(command)

    def setDevice(self,id, state):
        if state == True:
            print(f"Device {id} is turn ON")
            # print(f"command is :{ relay_ON[id-1]}")
            self.ser.write(relay_ON[id-1])
        else:
            print(f"Device {id} is turn OFF")
            # print(f"command is :{ relay_OFF[id-1]}")
            self.ser.write(relay_OFF[id-1])
        time.sleep(0.05)
        response = self.serial_read_data()
        print(f"Get reponse: {response}")
        return response
        
    def serial_read_data(self):
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]
            print(f"BUFFER: {data_array}")
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return None
        return None

    # soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
    def readTemperature(self):
        print("reading temperature soil")
        self.serial_read_data()
        self.ser.write(soil_temperature)
        time.sleep(0.05)
        return self.serial_read_data()

    # soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
    def readMoisture(self):
        print("reading moisture")
        self.serial_read_data()
        self.ser.write(soil_humidity)
        time.sleep(0.05)
        return self.serial_read_data()


    def readDistance(self,index):
        print(f"Reading sonar { index}")
        self.serial_read_data()
        if index not in [1,2]:
            return "ERROR index out range"
        if index == 1:
            self.ser.write(distance1_ON)
        if index == 2:
            self.ser.write(distance2_ON)
        time.sleep(0.05)
        return self.serial_read_data()
    
# my_rs485 = Modbus485()
# while True:
#     for idx in range(0,7):
#         my_rs485.setDevice(idx+1,True)
#         time.sleep(2)
#         my_rs485.setDevice(idx+1,False)
#         time.sleep(2)
    # for idx, relay in enumerate(relay_ON):
        

# while True:
#     print("TEST SENSOR")
#     print(my_rs485.readMoisture())
#     time.sleep(1)
#     print(my_rs485.readTemperature())
#     time.sleep(1)
#     print(my_rs485.readDistance(1))
#     time.sleep(1)
#     print(my_rs485.readDistance(2))
#     time.sleep(1)