import ftrobopy
from time import sleep
import sys
import paho.mqtt.client as mqtt

txt = ftrobopy.ftrobopy('192.168.0.12', 65000) 

M1 = txt.motor(1)
M2 = txt.motor(2)
M3 = txt.motor(3)
M4 = txt.motor(4)

I1 = txt.input(1)
I4 = txt.input(4)
I5 = txt.input(5)
I6 = txt.input(6)
I7 = txt.input(7)
I8 = txt.input(8)

client = mqtt.Client()
client.connect("localhost", 1883, 60)

state = I6.state()
d = 1
M3.setSpeed(512)
while d:
    ns = I6.state()
    if ns != state:
        M3.setSpeed(0)
        d = 0
        state = ns
        client.publish("HBW_event_log", "Emelő nyelv kalibrálása!")
    txt.updateWait()
    
M3.setSpeed(-512)
sleep(0.5)
M3.setSpeed(0)

state = I8.state()
a = 1
M4.setSpeed(512)
while a:
   ns = I8.state()
   if ns != state:
      M4.setSpeed(0)
      a = 0
      state = ns
      client.publish("HBW_event_log", "Emelő magasba emelése megtörtént!")
   txt.updateWait()

M4.setSpeed(-512)
M4.setDistance(50)
while not M4.finished():
   txt.updateWait()

state = I5.state()
b = 1
M2.setSpeed(512)
while b:
   ns = I5.state()
   if ns != state:
      M2.setSpeed(0)
      b = 0
      state = ns
      client.publish("HBW_event_log", "Emelő elindúlt az áruért!")
   txt.updateWait()
   
M2.setSpeed(-512)
M2.setDistance(815)
while not M2.finished():
   txt.updateWait()
   

M4.setSpeed(-512)
M4.setDistance(50)
while not M4.finished():
   txt.updateWait()
   
state = I7.state()
c = 1
M3.setSpeed(-512)
while c:
    ns = I7.state()
    if ns != state:
        M3.setSpeed(0)
        c = 0
        state = ns
        client.publish("HBW_event_log", "Emelő nyelve elérte az árút!")
    txt.updateWait()
    
M4.setSpeed(512)
M4.setDistance(50)
while not M4.finished():
   txt.updateWait()
   
state = I6.state()
e = 1
M3.setSpeed(512)
while e:
    ns = I6.state()
    if ns != state:
        M3.setSpeed(0)
        e = 0
        state = ns
        client.publish("HBW_event_log", "Emelő nyelve visszahúzva!")
    txt.updateWait()
    
M3.setSpeed(-512)
sleep(0.5)
M3.setSpeed(0)
M2.setSpeed(512)


state = I5.state()
f = 1
M2.setSpeed(512)
M2.setDistance(5000)
while f:
   ns = I5.state()
   if ns != state:
      M2.setSpeed(0)
      f = 0
      state = ns
      client.publish("HBW_event_log", "Emelő visszaérkezett!")
   txt.updateWait()
   
M2.setSpeed(-512)
M2.setDistance(30)
while not M2.finished():
   txt.updateWait()
   
state = I7.state()
g = 1
M3.setSpeed(-512)
while g:
    ns = I7.state()
    if ns != state:
        M3.setSpeed(0)
        g = 0
        state = ns
    txt.updateWait()
   
M4.setSpeed(-512)
M4.setDistance(700)

state = I4.state()
h = 1
while h:
    ns = I4.state()
    if ns != state:
        M1.setSpeed(-512)
        h = 0
    txt.updateWait()
        
        
        
state = I1.state()
i = 1
while i:
    ns = I1.state()
    if ns != state:
        M1.setSpeed(0)
        client.publish("HBW_event_log", "Áru kiadva a raktárból")
        client.publish("control", "VGR_start")
        i = 0
    txt.updateWait()
    
    
state = I6.state()
j = 1
M3.setSpeed(512)
while j:
    ns = I6.state()
    if ns != state:
        M3.setSpeed(0)
        j = 0
        state = ns
        client.publish("HBW_event_log", "Emelő nyelve visszahúzva")
    txt.updateWait()
    
M3.setSpeed(-512)
sleep(0.5)
M3.setSpeed(0)


client.disconnect()
client.loop_stop()

sys.exit(0)