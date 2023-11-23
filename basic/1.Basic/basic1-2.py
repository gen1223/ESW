import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
# from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# for LCD View on PC
from tkinter import *
# from PIL import ImageTk
from PIL import Image, ImageDraw, ImageFont, ImageTk
win = Tk()
win.title("LCD View")
can = Canvas(win, width=240, height=240)
can.pack()

class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        self.width = self.disp.width
        self.height = self.disp.height

joystick = Joystick()

my_image = Image.new("RGB", (joystick.width, joystick.height))
my_draw = ImageDraw.Draw(my_image)

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))

joystick.disp.image(my_image)

# for LCD View on PC
tk_img = ImageTk.PhotoImage(my_image, master=win)
can.create_image(0,0, anchor='nw', image=tk_img)
win.update()

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
my_draw.ellipse((100, 50, 140, 90), outline = "#FFFFFF", fill = (0, 0, 0))
#좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
joystick.disp.image(my_image)

# for LCD View on PC
tk_img = ImageTk.PhotoImage(my_image, master=win)
can.create_image(0,0, anchor='nw', image=tk_img)
win.update()

import numpy as np
class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        self.outline = "#FFFFFF"

    def move(self, command = None):
        if command == None:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command == 'up_pressed':
                self.position[1] -= 5
                self.position[3] -= 5

            elif command == 'down_pressed':
                self.position[1] += 5
                self.position[3] += 5

            elif command == 'left_pressed':
                self.position[0] -= 5
                self.position[2] -= 5
                
            elif command == 'right_pressed':
                self.position[0] += 5
                self.position[2] += 5

my_circle = Character(joystick.width, joystick.height)
my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
while True:
    command = None
    if not joystick.button_U.value:  # up pressed
        command = 'up_pressed'

    elif not joystick.button_D.value:  # down pressed
        command = 'down_pressed'

    elif not joystick.button_L.value:  # left pressed
        command = 'left_pressed'

    elif not joystick.button_R.value:  # right pressed
        command = 'right_pressed'
        
    else:
        command = None

    my_circle.move(command)

    my_draw.ellipse(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
#좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
    joystick.disp.image(my_image)

    # for LCD View on PC
    tk_img = ImageTk.PhotoImage(my_image, master=win)
    can.create_image(0,0, anchor='nw', image=tk_img)
    win.update()

win.mainloop()
