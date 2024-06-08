import paho.mqtt.client as mqtt
import json
class MQTTHelper:
    MQTT_SERVER = "io.adafruit.com"
    MQTT_PORT = 1883                                                                                                                       
    MQTT_USERNAME = "NhanHuynh"
    MQTT_PASSWORD = ""
     
    recvCallBack = None
    TOPIC = [
        "NhanHuynh/feeds/schedule"
    ]
    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected mqtt server succesfully!!")
        for topic in self.TOPIC:
            client.subscribe(topic)

    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("Subscribed to Topic!!!")

                                                                                                                                            
    def mqtt_recv_message(self, client, userdata, message):
        self.recvCallBack(message.payload.decode("utf-8"))
                                                                                                                                            
    def __init__(self):
        self.mqttClient = mqtt.Client()                                                                                                      
        self.mqttClient.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)                                                              
        self.mqttClient.connect(self.MQTT_SERVER, int(self.MQTT_PORT), 60)                                                                   
                                                                                                                                                
        # Register mqtt events
        self.mqttClient.on_connect = self.mqtt_connected                                                                                     
        self.mqttClient.on_subscribe = self.mqtt_subscribed                                                                                  
        self.mqttClient.on_message = self.mqtt_recv_message                                                                                  
                                                                                                                                                
        self.mqttClient.loop_start()                                                                                                         
                                                                                                                                            
    def setRecvCallBack(self, func):
        self.recvCallBack = func                                                                                                             

    def publish(self, topic, message):
        print(message)                                                                                                                       
        self.mqttClient.publish(topic, str(message), retain=True)