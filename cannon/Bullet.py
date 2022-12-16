'''
포물선 bullet 구현 (s=vt, s=(1/2)gt^2, vx=cos(v0), vy=sin(v0))  
초기조건: (x0, y0)=시작점, v0=속도, rad=각도,  dt=interval, g=중력가속도(9.8)  
수평속도(vx): v0 * cos(rad), 수직속도(vy): v0 * sin(rad)  
bullet의 x 위치= x0 + vx * dt  
bullet의 y 위치= y0 + vy * dt - 0.5 * g * dt^2  
'''

import numpy as np
import math

BR = 3  # radius of bullet
BR2 = BR*2 
G = 9.8 # gravitational constant

class Bullet:

    def __init__(self, pos, angle, speed):
        self.appearance = 'circle'
        rad = math.radians(angle)
        self.vx = speed * math.cos(rad)
        self.vy = speed * math.sin(rad)
        self.damage = 10
        self.p = np.array([pos[0]-BR, pos[1]-BR, pos[0]+BR, pos[1]+BR])
        self.p0 = self.p
        self.c = pos
        self.c0 = self.c
        self.t = 0
        self.state = 'move'
        self.outline = "#0000FF"

    def move(self):
        dx = int(self.vx*self.t * 0.02)
        dy = int((self.vy*self.t - 0.5*G*self.t**2) * 0.02)
        self.p0 = self.p                            # save previous position
        self.p[0] += dx
        self.p[2] += dx
        self.p[1] -= dy
        self.p[3] -= dy
        self.c0 = self.c                            # save previous center
        self.c = np.array([(self.p[0] + self.p[2]) / 2, (self.p[1] + self.p[3]) / 2])
        self.t += 0.5

    def ground(self):
        ''' True if bullet is down on the ground '''
        return self.p[1] > 240
             
    def collision_check(self, enemys):
        for enemy in enemys:
            collision = False
            if enemy.state == 'alive':
                collision = self.overlap(enemy.position)
            if collision:
                enemy.state = 'die'
                self.state = 'hit'

    def overlap(self, other_p):
        ''' check if other_p is in the box of ego_p0 ~ ego_p
        return : True : if overlap
                False : if not overlap '''
        if (self.p[2]>other_p[0] and self.p[0]<other_p[2] and self.p[3]>other_p[1] and self.p[1]<other_p[3]):
            return True
        else:
            if (self.p[2] < other_p[0]): return False
            if (self.p[0] > other_p[2]): return False
            if (self.p[3] < other_p[1] and self.c0[0] < other_p[1]): return False
            if (self.p[1] > other_p[3] and self.c0[0] > other_p[3]): return False
            print ([self.c[0], self.c[1]], end=" ")

            ''' c0, c: bullet center, (e1, e2): enemy
            dx = (cx - c0x) / BR2
            dy = (cy - c0y) / BR2
            i = 1
            while (x = c0x + dx * i) < e2x
              y = c0y + dy * i
              if (e1x < x) && (x < e2x) && (e1y < y) && (y < e2y)
                return True
              i++
            return False
            '''
            dx = (self.c[0] - self.c0[0]) / BR2
            dy = (self.c[1] - self.c0[1]) / BR2
            i = 1
            x = self.c0[0] + dx
            while (x < other_p[2]):
                y = self.c0[1]+(dy*i)
            #    print ([x,y,dx,dy], end=" ")
                if (other_p[0]<x) and (other_p[2]>x) and (other_p[1]<y) and (other_p[3]>y):
                    return True
                i += 1
                x = self.c0[0]+(dx*i)
            return False