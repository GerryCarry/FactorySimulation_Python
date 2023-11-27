from time import sleep
import threading
import ftrobopy
import paho.mqtt.client as mqtt
import sys

txt = ftrobopy.ftrobopy('192.168.0.10', 65000) 

M1 = txt.motor(1)
M2 = txt.motor(2)

O5 = txt.output(5)
O6 = txt.output(6)
O7 = txt.output(7)
O8 = txt.output(8)

I1 = txt.input(1)
I2 = txt.input(4)
I3 = txt.input(3)
I5 = txt.input(5)

a = 1

c = 1

def blink(lamp):
    a = 1
    i = 0
    while a:
        if i >= 11 :
            a = 0
        lamp.setLevel(256)
        sleep(0.5)
        lamp.setLevel(0)
        sleep(0.5)
        i = i+1
      
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Sindaru")      
    
def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))
    if msg.payload.decode('utf-8') == "megerkezett":    
        M2.setSpeed(0)
        O6.setLevel(512)
        O5.setLevel(0)
        sleep(2)
        O6.setLevel(0)
        client.publish("Koho_event_log", "Korong a polírozó állomáson!")
        client.disconnect()
        client.loop_stop()
        sys.exit(0)

      

def mqtt_listener(client):
    client.loop_forever()
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

t1 = threading.Thread(target=mqtt_listener, args=(client,))
t1.daemon = True   
t1.start()
    

sleep(1)
O7.setLevel(512)
M1.setSpeed(-512)

client.publish("Koho_event_log", "Korong behúzása folyamatban...")

button_1_state = I1.state()
while a: 
    button_1_state_newState = I1.state()
    if button_1_state_newState != button_1_state and button_1_state_newState == 1:
        M1.setSpeed(0)
        O7.setLevel(0)
        client.publish("Koho_event_log", "Korong behúzva!")
        t1 = threading.Thread(target=blink, args=(O8,))
        t1.daemon = True   
        t1.start()
        client.publish("Koho_event_log", "Hevítés folyamatban")
        button_1_state = button_1_state_newState
        M2.setSpeed(-512)
        b = 1
        button_3_state = I3.state()
        while b: 
            button_3_state_newState = I3.state()
            if button_3_state_newState != button_3_state and button_3_state_newState == 1:
                M2.setSpeed(0)
                client.publish("Koho_event_log", "Síndaru a kohónál")
                O7.setLevel(512)
                M1.setSpeed(512)
                client.publish("Koho_event_log", "Korong kiadása folyamatban...")
                b = 0
                a = 0



button_2_state = I2.state()
while c:
    button_2_state_newState = I2.state()
    if button_2_state_newState != button_2_state and button_2_state_newState == 1:
        client.publish("Koho_event_log", "Korong kiadva kohóból")
        M1.setSpeed(0)
        O7.setLevel(0)      
        button_2_state = button_2_state_newState
        O6.setLevel(512)
        sleep(0.5)
        O5.setLevel(512)
        sleep(0.5)
        O6.setLevel(0)
        sleep(0.5)
        M2.setSpeed(512)
        sleep(15)
        c=0


   
