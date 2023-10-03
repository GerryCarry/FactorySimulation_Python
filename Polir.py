from time import sleep
import ftrobopy
import sys
import paho.mqtt.client as mqtt

txt = ftrobopy.ftrobopy('192.168.0.11', 65000)

M1 = txt.motor(1)
M2 = txt.motor(2)
M3 = txt.motor(3)
M4 = txt.motor(4)



I1 = txt.input(1)
I2 = txt.input(2)
I3 = txt.input(3)
I4 = txt.input(4)
I5 = txt.input(5)
I6 = txt.input(6)

O7 = txt.output(7)


client = mqtt.Client()
client.connect("localhost", 1883, 60)

M4.setSpeed(-512)

client.publish("control", "Polir_started")


###Várunk  a daru indulására
a = 1
button_5_state = I5.state()
while a:
  button_5_new_state = I5.state()
  if button_5_new_state != button_5_state:
     client.publish("Sindaru", "elindult")
     client.publish("Polir_event_log", "Síndaru elindult")
     a = 0


###Várunk daru érkezésére
a = 1
button_5_state = I5.state()
while a:
    button_5_new_state = I5.state()
    if button_5_state != button_5_new_state and button_5_new_state == 1:
        client.publish("Sindaru", "megerkezett")
        client.publish("Polir_event_log", "Síndaru megérkezett")
        a = 0
        
sleep(8)
M1.setSpeed(-512)
a = 1
button_2_state = I2.state()
while a:
    button_2_new_state = I2.state()
    if button_2_new_state  != button_2_state:
        client.publish("Polir_event_log", "Polírozás folyamatban...")
        M1.setSpeed(0)
        M2.setSpeed(512)
        sleep(5)
        client.publish("Polir_event_log", "Polírozás vége")
        M1.setSpeed(-512)
        M2.setSpeed(0)
        a = 0


###Polír vége, korong szalagra
a = 1
button_3_state = I3.state()
while a:
    button_3_new_state = I3.state()
    if button_3_new_state  != button_3_state:
        M1.setSpeed(0)
        O7.setLevel(512)
        sleep(0.5)
        O7.setLevel(0)
        client.publish("Polir_event_log", "Korong a futószallagon")
        client.publish("control", "Sortir_start")
        M3.setSpeed(-512)
        M1.setSpeed(512)
        M4.setSpeed(0)
        a = 0

a = 1
button_1_state = I1.state()
while a:
    button_1_new_state = I1.state()
    if button_1_new_state != button_1_state:
        M1.setSpeed(0)
        M3.setSpeed(0)
        a = 0
        sleep(0.5) #Ez azért kell hogy gyorsabban álljon le a motor, mert a program vége lelassítja a motorok leállítását...

client.publish("Polir_event_log", "Polírozó leáll!")

sys.exit(0)
                                     

                                    


