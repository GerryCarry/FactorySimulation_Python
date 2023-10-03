from time import sleep
import ftrobopy
import sys
import paho.mqtt.client as mqtt


txt = ftrobopy.ftrobopy('192.168.0.14', 65000)  

M1 = txt.motor(1)
M4 = txt.motor(4)

I1 = txt.input(1)
I3 = txt.input(3)

I6 = txt.input(6)
I7 = txt.input(7)
I8 = txt.input(8)

O5 = txt.output(5)
O6 = txt.output(6)
O7 = txt.output(7)

col = txt.colorsensor(2)

exitloop = 1
state_in = I1.state()
state_out = I3.state()
measureing = 0
colors = []
color = 0
button_pushed = 0;

state_blue = I6.state()
state_red = I7.state()
state_white = I8.state()

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while exitloop:
    ns_in = I1.state()
    ns_out = I3.state()
    state_blue_new = I6.state()
    state_red_new = I7.state()
    state_white_new = I8.state()    
    if ns_in != state_in: 
       client.publish("Sorter_event_log", "Korong a szortírozón!")
       state_in = ns_in
    if ns_in == 0:
       M1.setSpeed(-512)
       measureing = 1
       colors.clear()
    if ns_out != state_out:
        state_out = ns_out
        if state_out == 0:
            button_pushed = txt.getCurrentCounterValue(0); 
            measureing = 0
            colors.sort()
            color = colors[0]
            print(color)
            M4.setSpeed(-512)
            if color > 1340:
                if color > 1550:
                    client.publish("Sorter_event_log", "Kék korong")
                    sleep(0.7)
                    O5.setLevel(512)
                    sleep(0.5)
                    O5.setLevel(0)
                else:
                    client.publish("Sorter_event_log", "Piros korong")
                    sleep(2.4)
                    O6.setLevel(512)
                    sleep(0.5)
                    O6.setLevel(0)
            else:
                client.publish("Sorter_event_log", "Fehér korong")
                sleep(3.8)
                O7.setLevel(512)
                sleep(0.5)
                O7.setLevel(0)
            
    if state_blue != state_blue_new:
        M1.setSpeed(0)
        M4.setSpeed(0)
        client.publish("Sorter_event_log", "Kék korong a tárolóban!")
        exitloop=0
        
    if state_red != state_red_new:
        M1.setSpeed(0)
        M4.setSpeed(0)
        client.publish("Sorter_event_log", "Piros korong a tárolóban!")
        exitloop=0
        
    if state_white != state_white_new:
        M1.setSpeed(0)
        M4.setSpeed(0)
        client.publish("Sorter_event_log", "Fehér korong a tárolóban!")
        exitloop=0
         
    if measureing == 1:
        colval = col.value()
        colors.append(colval)
        sleep(0.01)

sys.exit(0)








