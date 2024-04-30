import pygame as pg
import numpy as np
from math import *

#상수
WIDTH = 640
HEIGHT = 400
FPS = 30
K = 0.2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
R = 3
N = 100
IR = 0
W = 0.05

def get_dist(x1, y1, z1, x2, y2, z2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

def get_size(vec):
    return np.sum(vec**2)

class Dot:
    def __init__(self, x, y, z=0):
        self.pos = np.array([x, y, z], dtype='float')
        self.pos_0 = np.array([x, y, z], dtype='float')
        self.fixed = [False, False, False]
        self.vel = np.array([0, 0, 0], dtype='float')
        self.acc = np.array([0, 0, 0], dtype='float')
        self.connected = []
        self.mass = 1

    def set_acc(self, acc):
        self.acc = np.array(acc, dtype='float')
    
    def set_vel(self, vel):
        self.vel = np.array(vel, dtype='float')
    
    def set_pos(self, pos):
        self.pos = np.array(pos, dtype='float')
    
    def set_mass(self, m):
        self.mass = m
    
    def get_acc(self):
        acc = np.array([0, 0, 0], dtype='float')
        for dot in self.connected:
            r = dot.pos - self.pos
            acc += K * (get_size(r) - get_size(dot.pos_0 - self.pos_0) * IR) * r / get_size(r) / self.mass
        return acc

    def connect(self, lst):
        self.connected += list(lst)
    
    def acceleration(self):
        self.vel += self.acc

    def move(self):
        self.pos += self.vel
        for i in range(3):
            if self.fixed[i]:
                self.pos[i] = self.pos_0[i]
    
    def draw(self, screen):
        pg.draw.circle(screen, BLUE, self.pos[:2], sqrt(self.mass) * 3)
    
    def make_pulse(self, a, w, start_time=0):
        self.set_pos(self.pos + np.array([0, a * sin(max(0, min(pg.time.get_ticks() / FPS * w - start_time, pi))) ** 2, 0]))
    
    def make_sin_wave(self, a, w, start_time=0):
        self.set_pos(self.pos + np.array([0, a * sin(max(pg.time.get_ticks() / FPS * w - start_time, 0)), 0]))


class DotArray:
    def __init__(self, n, sx, sy, ex, ey):
        self.len = n
        self.dots = [Dot(x, y) for x, y in zip(np.linspace(sx, ex, n), np.linspace(sy, ey, n))]
        for i in range(n):
            lst = []
            if(i - 1 >= 0):
                lst.append(self.dots[i - 1])
            if(i + 1 < n):
                lst.append(self.dots[i + 1])
            self.dots[i].connect(lst)
    
    def set_mass(self, start, end, m):
        for i in range(start, end):
            self.dots[i].set_mass(m)
    
    def set_acc(self):
        for dot in self.dots:
            dot.set_acc(dot.get_acc())
    
    def acceleration(self):
        for dot in self.dots:
            dot.acceleration()
    
    def move(self):
        for dot in self.dots:
            dot.move()
    
    def draw(self, screen):
        for dot in self.dots:
            dot.draw(screen)


#pygame 실행
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('string sim.')
clock = pg.time.Clock()
running = True
string = DotArray(N, WIDTH/2 - 300, HEIGHT/2, WIDTH/2 + 300, HEIGHT/2)
#string.dots[0].set_vel([0, 2, 0])
#for dot in string.dots:
#    dot.fixed = [True, False, False]
string.dots[0].fixed = [True, False, False]
string.dots[N - 1].fixed = [True, False, False]

#(1) 자유단 반사

#(2) 고정단 반사
#string.dots[N - 1].fixed = [True, True, False]

#(3) 중첩

#(4) 중첩(상쇄)

#(5) 다른 질량의 줄
#string.set_mass(N//2, N, 3)

while running:
    clock.tick(FPS)
    #event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #update
    #string.dots[0].make_pulse(30, W, 20)
    string.dots[0].make_sin_wave(10, W * 2, 30)
    #(3) 중첩
    #string.dots[N - 1].make_pulse(30, W, 1)
    #(4) 상쇄
    #string.dots[N - 1].make_pulse(-30, W, 1)
    string.set_acc()
    string.acceleration()
    string.move()

    #draw
    string.draw(screen)
    pg.display.update()
    screen.fill(BLACK)