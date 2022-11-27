# blink test

import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(17, g.OUT, initial=0)
g.setup(18, g.IN, pull_up_down=g.PUD_UP)

while 1:
    g.output(17, not g.input(18))

g.cleanup()

