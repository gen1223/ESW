import numpy as np

class Cannon:
    def __init__(self, pos):
        self.appearance = 'circle'
        self.state = None
        self.c = pos
        self.pos = np.array([pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10])
        self.angle = 45
        self.speed = 70
        self.outline = "#FFFFFF"

    def set(self, command = None):
        if command == 'up':
            self.angle += 0.3
        if command == 'down':
            self.angle -= 0.3
        if command == 'right':
            self.speed += 0.5
        if command == 'left':
            self.speed -= 0.5