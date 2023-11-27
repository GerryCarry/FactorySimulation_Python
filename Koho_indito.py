from time import sleep
import ftrobopy 
import paho.mqtt.client as mqtt

txt = ftrobopy.ftrobopy('192.168.0.10', 65000) 

I5 = txt.input(5)

client = mqtt.Client()
client.connect("localhost", 1883, 60)


a = 1
light_sensor_state = I5.state()
while a:
    light_sensor_new_state = I5.state()
    if light_sensor_new_state != light_sensor_state:
        print("Megjött!")
        client.publish("control", "Koho_start")
        client.publish("visszarak", "go")
        a = 0
        
print("Koho start Leáll!")