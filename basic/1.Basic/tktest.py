from tkinter import *
import random
import time

def move():
    global x_speed, y_speed
    ball_coor = canvas.coords(ball)

    if ball_coor[0] <= 0 or ball_coor[2] >= W:
        x_speed = -x_speed
    if ball_coor[1] <= 0 or ball_coor[3] >= H:
        y_speed = -y_speed
    canvas.move(ball, x_speed, y_speed)

win = Tk()
win.title("Test")

W = 240
H = 240
canvas = Canvas(win, width=W, height=H)
canvas.pack()

ball = canvas.create_oval(10, 10, 50, 50, fill="pink")

x_speed = random.randint(3, 10)
y_speed = random.randint(3, 10)

while True:
    move()
    win.update()
    time.sleep(0.1)

win.mainloop()
