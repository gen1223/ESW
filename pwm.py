import RPi.GPIO as g
import time

f = [261, 294, 329, 349, 392, 440, 493, 523]
n = [0,0,4,4,5,5,4,3,3,2,2,1,1,0]
d = [0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

g.setmode(g.BCM)
g.setup(18, g.OUT)
p = g.PWM(18, 1000)

p.start(90)
for i in range(len(n)):
    p.ChangeDutyCycle(90)
    p.ChangeFrequency(f[n[i]])
    time.sleep(d[i])
    p.ChangeDutyCycle(0)
    time.sleep(d[i])
p.stop()
g.cleanup()

