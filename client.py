import paho.mqtt.client as mqtt 
import time
import uuid



broker_address="localhost"
topic = "#"

conf = {
    "configTopic" : "homeassistant/switch/win/config", 
    "stateTopic" : "stat/win/state" ,
    "cmdTopic" : "cmd/win/exec",
    "lwtTopic" : "some/thing/lwt"
}

stateMsgTemplate ='{{"name":"bedroom_heater","command_topic":"{cmd_topic}","state_topic":"{state_topic}","value_template":"{{value_json.POWER}}","payload_off":"OFF","payload_on":"ON","availability_topic":"{lwt_topic}","payload_available":"Online","payload_not_available":"Offline"}}' 

class WinClient:
    

    def __init__(self, host, conf):
        self.client = mqtt.Client(str(uuid.uuid4))
        print(host)
        self.client.connect(host)
        self.confs = [conf]
        self.subTopics()
        self.pushConfigs()
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
    
    def subTopics(self):
        for c in self.confs:
            cmdTopic = c['cmdTopic']
            self.client.subscribe(cmdTopic)
            print("Subscribing to topic",cmdTopic)
    
    def pushConfigs(self):
        for c in self.confs:
            msg = stateMsgTemplate.format(cmd_topic=c['cmdTopic'], state_topic=c['stateTopic'], lwt_topic=c['lwtTopic'])
            self.client.publish(c["configTopic"], msg)
    
    def run(self):
        self.client.loop_start()

w = WinClient('127.0.0.1', conf)
w.run()
