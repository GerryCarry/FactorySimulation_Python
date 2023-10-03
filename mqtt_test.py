import paho.mqtt.client as mqtt
from time import sleep
import threading

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Sindaru")
    
# A callback függvény, amit akkor hívunk meg, amikor üzenetet kapunk
def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))

def mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()

t1 = threading.Thread(target=mqtt_listener, args=())
t1.daemon = True   
t1.start()

#message = "{\"Hali\": \"Gali\"}"
#client.publish("mqtt-test", message)
i = 0
while 1:
   print(i)
   sleep(0.5)
   i = i+1