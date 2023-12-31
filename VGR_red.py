import ftrobopy
from time import sleep
import sys
import paho.mqtt.client as mqtt

txt = ftrobopy.ftrobopy('192.168.0.13', 65000)

M1 = txt.motor(1)
M2 = txt.motor(2)
M3 = txt.motor(3)
M4 = txt.motor(4)

I1 = txt.input(1)
I2 = txt.input(2)
I3 = txt.input(3)

O8 = txt.output(8)

client = mqtt.Client()
client.connect("localhost", 1883, 60)

M1.setSpeed(-512)
M1.setDistance(390)
client.publish("VGR_event_log", "Daru elindúlt piros korongért")
while not M1.finished():
   txt.updateWait()
   
M3.setSpeed(-512)
M3.setDistance(400)
while not M3.finished():
   txt.updateWait()


M2.setSpeed(-512)
M2.setDistance(780)
while not M2.finished():
   txt.updateWait()
   
M4.setSpeed(512)
O8.setLevel(512)
client.publish("VGR_event_log", "Piros korong megemelve!")


M2.setSpeed(512)
M2.setDistance(300)
while not M2.finished():
   txt.updateWait()


state = I3.state()
a = 1
M3.setSpeed(512)
M3.setDistance(2000)
while a:
   ns = I3.state()
   if ns != state:
      M3.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()
   
M3.setSpeed(-512)
M3.setDistance(30)
while not M3.finished():
   txt.updateWait()

state = I1.state()
a = 1
M1.setSpeed(512)
M1.setDistance(2000)
while a:
   ns = I1.state()
   if ns != state:
      M1.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()
   
M2.setSpeed(-512)
M2.setDistance(350)
while not M2.finished():
   txt.updateWait()
   
O8.setLevel(0)
M4.setSpeed(0)
sleep(1)
client.publish("VGR_event_log", "Piros korong elkészült!")

state = I2.state()
a = 1
M2.setSpeed(512)
M2.setDistance(5000)
while a:
   ns = I2.state()
   if ns != state:
      M2.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()

M2.setSpeed(-512)
M2.setDistance(30)
while not M2.finished():
   txt.updateWait()