import paho.mqtt.client as mqtt #import the client1
import time




broker_address="192.168.2.53"
topic = "#"

configTopic = "homeassistant/switch/{}/config" 
stateTopic = "stat/{}/state" 
cmdTopic = "cmd/{}/exec" 



#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop

print("Subscribing to topic",topic)
client.subscribe(topic)

time.sleep(1200) # wait
client.loop_stop() #stop the loop


def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
