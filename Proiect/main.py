import pygame
import time
import math
from func import scale
from func import blit_rotate

LOGGO = pygame.image.load('images/loggo.JPG')
BLUE_CAR = scale(pygame.image.load('images/blue_car.png'), 0.5)
RED_CAR = scale(pygame.image.load('images/red_car.png'), 0.5)
ORANGE_CAR = scale(pygame.image.load('images/orange_car.png'), 0.4)
TRACK = pygame.image.load('images/track.png')
TRACK_LIMITS = pygame.image.load('images/track_limits.png')
FINISH = pygame.image.load('images/finish.png')
DECO = pygame.image.load('images/decoration.png')
CIRCUIT = pygame.image.load('images/circuit.png')

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def move_backward(self):
        self.vel = min(self.vel - self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

class Car(AbstractCar):
    IMG = RED_CAR
    START_POS = (635, 250)

def update_backround(WIN, TRACK, TRACK_LIMITS, CIRCUIT, FINISH):
    WIN.blit(TRACK, (0, 0))
    WIN.blit(TRACK_LIMITS, (0, 0))
    WIN.blit(CIRCUIT, (0, 0))
    WIN.blit(FINISH, (631, 314))
    player_car.draw(WIN)
    pygame.display.update()


HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 game")
pygame.display.set_icon(LOGGO)
clock = pygame.time.Clock()

player_car = Car(4, 2)
update_backround(WIN, TRACK, TRACK_LIMITS, CIRCUIT, FINISH)
state = True
while(state):
    
    clock.tick(FPS)
    moved = False
    update_backround(WIN, TRACK, TRACK_LIMITS, CIRCUIT, FINISH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False
            break

    command = pygame.key.get_pressed()
    if command[pygame.K_a]:
        if(player_car.vel > 0):
            player_car.rotate(left=True)
    
    if command[pygame.K_d]:
        if(player_car.vel > 0):
            player_car.rotate(right=True)
            
    if command[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if command[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()
pygame.quit()
