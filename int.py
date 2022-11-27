import RPi.GPIO as g
import time

# Interrupt Service Callback
def sPressed(channel):
    print("Button Pressed on Channel ", channel)

g.setmode(g.BCM)
g.setup(18, g.IN, pull_up_down=g.PUD_UP)
g.add_event_detect(18, g.RISING, callback=sPressed, bouncetime=100) # bouncetime=50~200

while 1:
    print('.', end='', flush=True)
    time.sleep(0.5)

g.cleanup()
