import ftrobopy
from time import sleep
import sys
import paho.mqtt.client as mqtt
import threading

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


def on_message(client, userdata, msg):
    visszarak()
    
def mqtt_listener(client):
    client.loop_forever()
    
client = mqtt.Client()
client.on_message = on_message
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
        client.publish("HBW_event_log", "Emelő kalibrálása folyamatban...")
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
      client.publish("HBW_event_log", "Emelő kalibrálása megtörtént!")
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
   txt.updateWait()
   
M2.setSpeed(-512)
M2.setDistance(1415)
client.publish("HBW_event_log", "Emelő úton az áruért...")
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
        client.publish("HBW_event_log", "Emelő áruért nyúl...")
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
        client.publish("HBW_event_log", "Emelő kiemeli az árút..")
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
      client.publish("HBW_event_log", "Emelő megérkezett az áruval!")
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
        client.publish("control", "VGR_start")
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
        sleep(0.2)
        M1.setSpeed(0)
        client.publish("HBW_event_log", "Áru kiadva a raktárból!")
        i = 0
    txt.updateWait()
    
    
    ###
    # Innen szedve
    ###



client.subscribe("visszarak")   
t1 = threading.Thread(target=mqtt_listener, args=(client,))
t1.daemon = False   
t1.start()



def visszarak():
    M1.setSpeed(512)
    
    state = I4.state()
    i = 1
    while i:
        ns = I4.state()
        if ns != state:
            M1.setSpeed(0)
            i = 0
            
            
    client.publish("HBW_event_log", "Tárolódoboz visszahelyezése folyamatban...")
    ###
    # Innen szedve
    ###
    
    state = I8.state()
    a = 1
    M4.setSpeed(512)
    M4.setDistance(2000)
    while a:
        ns = I8.state()
        if ns != state:
            M4.setSpeed(0)
            a = 0
            state = ns
        txt.updateWait()

    state = I6.state()
    d = 1
    M3.setSpeed(512)
    while d:
        ns = I6.state()
        if ns != state:
            M3.setSpeed(0)
            d = 0
            state = ns
        txt.updateWait()

    M2.setSpeed(-512)
    M2.setDistance(1375)
    while not M2.finished():
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
        txt.updateWait()

    M4.setSpeed(-512)
    M4.setDistance(150)
    while not M4.finished():
        txt.updateWait()
    
    client.publish("HBW_event_log", "Tárolódoboz visszahelyezve a raktárba!")
    
    state = I6.state()
    d = 1
    M3.setSpeed(512)
    while d:
        ns = I6.state()
        if ns != state:
            M3.setSpeed(0)
            d = 0
            state = ns
        txt.updateWait()
        
    M3.setSpeed(-512)
    sleep(0.5)
    M3.setSpeed(0)

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
            client.publish("HBW_event_log", "Tároló visszarakva a raktárba!")
        txt.updateWait()
   
    M2.setSpeed(-512)
    M2.setDistance(30)
    while not M2.finished():
        txt.updateWait()
    
    
    client.publish("HBW_event_log", "Emelő készenlétben!")
    sys.exit(0)


t1.join()


sys.exit(0)