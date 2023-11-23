'''
 Cannon Game
'''

# for LCD View on PC
from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
win = Tk()
win.title("LCD View")
can = Canvas(win, width=240, height=240)
can.pack()

import random
import math
# from PIL import Image, ImageDraw, ImageFont
from Enemy import Enemy
from Bullet import Bullet
from Cannon import Cannon
from Joystick import Joystick

def main():
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height)) #도화지!
    my_draw = ImageDraw.Draw(my_image) #그리는 도구!
    my_cannon = Cannon((20, 220))
    # my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))

    #rx = random.randrange(180, 240)
    #ry = random.randrange(180, 240)
    #enemy = Enemy((rx, ry))
    enemys_list = []

    bullet = None
    while True:
        command = None
    
        if not joystick.button_U.value:     # up pressed
            command = 'up'
        if not joystick.button_D.value:     # down pressed
            command = 'down'
        if not joystick.button_L.value:     # left pressed
            command = 'left'
        if not joystick.button_R.value:     # right pressed
            command = 'right'
        if not joystick.button_A.value:     # A pressed
            bullet = Bullet(my_cannon.c, my_cannon.angle, my_cannon.speed)
        if not joystick.button_B.value:     # B pressed
            rx = random.randrange(120, 240)
            ry = random.randrange(120, 240)
            enemy = Enemy((rx, ry))
            enemys_list.append(enemy)

        my_cannon.set(command)
        if bullet != None:
            bullet.collision_check(enemys_list)
            bullet.move()
    #        print(bullet.c[0], bullet.c[1])
                    
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
        my_draw.ellipse(tuple(my_cannon.pos), outline = my_cannon.outline, fill = (0, 0, 0))

        dx = int(my_cannon.speed * math.cos(math.radians(my_cannon.angle))/2)
        dy = int(my_cannon.speed * math.sin(math.radians(my_cannon.angle))/2)
        my_draw.line((my_cannon.c[0], my_cannon.c[1], my_cannon.c[0]+dx, my_cannon.c[1]-dy), fill=(0,0,230), width=2)
        
        for enemy in enemys_list:
            if enemy.state == 'alive':
                my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0))
            elif enemy.state == 'die':
                enemys_list.remove(enemy)

        #   for bullet in bullets:
        if bullet != None:
            if (bullet.state == 'move') and (not bullet.ground()):
                my_draw.ellipse(tuple(bullet.p), outline = bullet.outline, fill = (0, 0, 255))
            else:
            #    bullets.remove(bullet)
                bullet = None
        

        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image)
        # for LCD View on PC choi++231110
        tk_img = ImageTk.PhotoImage(my_image, master=win)
        can.create_image(0,0, anchor='nw', image=tk_img)
        win.update()

if __name__ == '__main__':
    main()
    win.mainloop()