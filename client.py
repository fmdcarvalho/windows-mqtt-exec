import paho.mqtt.client as mqtt 
import time
import uuid
import subprocess

conf = {
    "name" : "win",
    "configTopic" : "homeassistant/switch/win/config", 
    "stateTopic" : "stat/win/state" ,
    "cmdTopic" : "cmd/win/exec",
    "lwtTopic" : "some/thing/lwt"
}

configMsgTemplate ='{{"name": "{name}","command_topic":"{cmd_topic}","state_topic":"{state_topic}","value_template":{{{{value_json.POWER}}}}, "payload_off":"OFF","payload_on":"ON","availability_topic":"{lwt_topic}","payload_available":"Online","payload_not_available":"Offline"}}'

stateMsgTemplate = '{{"POWER":"{state}"}}'

class WinClient:

    def __init__(self, host, conf, port=1883):
        self.client = mqtt.Client(str(uuid.uuid4))
        print(host)
        self.client.connect(host, port)
        self.confs = [conf]
        self.subTopics()
        self.pushLWT()
        self.pushConfigs()
        #self.pushStates()
        self.client.on_message = self.on_message
        print("qwe2")

    def on_message(self, client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        payload = str(message.payload.decode("utf-8"))

        msg = stateMsgTemplate.format(state=payload)
        if "ON" in payload:
            res = subprocess.check_output(["start", "../nircmd/setSpeakers.bat"])
            self.client.publish(conf["stateTopic"], str(msg), qos=0)
        elif "OFF" in payload:
            res = subprocess.check_output(["start", "../nircmd/setTV.bat"])
            self.client.publish(conf["stateTopic"], str(msg), qos=0)
        print(msg)

    def subTopics(self):
        for c in self.confs:
            cmdTopic = c['cmdTopic']
            self.client.subscribe(cmdTopic)
            print("Subscribing to topic",cmdTopic)
    
    def pushConfigs(self):
        for c in self.confs:
            msg = configMsgTemplate.format(name=c['name'], cmd_topic=c['cmdTopic'], state_topic=c['stateTopic'], lwt_topic=c['lwtTopic'])
            print(msg)
            self.client.publish(c["configTopic"], msg, retain=True)

    def pushLWT(self):
        for c in self.confs:
            self.client.publish(c["lwtTopic"], "Online", retain=True)

    def pushStates(self):
        for c in self.confs:
            msg = stateMsgTemplate.format(state="ON")
            print(msg)
            self.client.publish(c["stateTopic"], msg)

    def run(self):
        self.client.loop_start()
        while True:
            time.sleep(1)

w = WinClient('127.0.0.1', conf, 7001)
w.run()
