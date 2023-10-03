import ftrobopy
from time import sleep

txt = ftrobopy.ftrobopy('192.168.0.13', 65000)

M1 = txt.motor(1)
M2 = txt.motor(2)
M3 = txt.motor(3)
I3 = txt.input(3)





I2 = txt.input(2)
state = I2.state()
a = 1
M2.setSpeed(512)
while a:
   ns = I2.state()
   if ns != state:
      print("state(), getCurrentInput():", ns, txt.getCurrentInput(0))
      M2.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()

M2.setSpeed(-512)
sleep(0.5)
M2.setSpeed(0)



state = I3.state()
a = 1
M3.setSpeed(512)
while a:
   ns = I3.state()
   if ns != state:
      print("state(), getCurrentInput():", ns, txt.getCurrentInput(0))
      M3.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()

M3.setSpeed(-512)
M3.setDistance(30)
while not M3.finished():
   txt.updateWait()


I1 = txt.input(1)
state = I1.state()
a = 1
M1.setSpeed(512)
while a:
   ns = I1.state()
   if ns != state:
      print("state(), getCurrentInput():", ns, txt.getCurrentInput(0))
      M1.setSpeed(0)
      a = 0
      state = ns
   txt.updateWait()





