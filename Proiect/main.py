import pygame
import math
from func import scale
from func import blit_rotate

# Initialize pygame
pygame.init()

# Load assets
LOGGO = pygame.image.load('images/loggo.JPG')
ORANGE_CAR = scale(pygame.image.load('images/orange_car.png'), 0.5)
BLUE_CAR = scale(pygame.image.load('images/blue_car.png'), 0.5)
RED_CAR = scale(pygame.image.load('images/red_car.png'), 0.5)
TRACK = scale(pygame.image.load('images/track.png'), 1.5)
TRACK_LIMITS = scale(pygame.image.load('images/track_limits.png'), 1.5)
TRACK_LIMITS_MASK = pygame.mask.from_surface(TRACK_LIMITS)
DECO = scale(pygame.image.load('images/decoration.png'), 1.5)
DECO_MASK = pygame.mask.from_surface(DECO)
CIRCUIT = scale(pygame.image.load('images/circuit.png'), 1.5)
WALLS = scale(pygame.image.load('images/walls.png'), 1.2)
WALLS_MASK = pygame.mask.from_surface(WALLS)
FINISH = scale(pygame.image.load('images/finish.png'), 1.5)
FINISH_MASK = pygame.mask.from_surface(FINISH)
TITLE = scale(pygame.image.load('images/title.jpg'), 2)
FINISH_POSITION = (800, 290)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Draw reset button
def draw_reset_button(WIN):
    font = pygame.font.Font(None, 36)
    text = font.render('Reset', True, WHITE)
    pygame.draw.rect(WIN, RED, [10, 10, 100, 50])
    WIN.blit(text, (20, 20))

# Reset game
def reset_game():
    global player_car  # Ensure player_car is accessed correctly
    player_car.vel = 0  # Reset velocity
    player_car.x, player_car.y = player_car.START_POS  # Reset position
    update_background(WIN)

# Abstract car class
class AbstractCar:
    IMG = None
    START_POS = (0, 0)

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.x, self.y = self.START_POS
        self.acceleration = 1

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
        self.vel = max(self.vel - self.acceleration, -self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def brake (self):
        self.vel = max(self.vel - self.acceleration, 0)

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration * 0.1, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration * 0.1, 0)
        self.move()

    def reduce_speed_limits(self):
        if(self.vel > self.max_vel/2):
            if self.vel > 0:
                self.vel = max(self.vel - self.acceleration * 0.5, 0)
            elif self.vel < 0:
                self.vel = min(self.vel + self.acceleration * 0.5, 0)

    def reduce_speed_deco(self):
        if(self.vel > 1):
            if self.vel > 0:
                self.vel = max(self.vel - self.acceleration * 2, 0)
            elif self.vel < 0:
                self.vel = min(self.vel + self.acceleration * 2, 0)

    def position(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

# Player car class
class RedCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (815, 350)

class BlueCar(AbstractCar):
    IMG = BLUE_CAR
    START_POS = (815, 350)

class OrangeCar(AbstractCar):
    IMG = ORANGE_CAR
    START_POS = (815, 350)

# Dicționar pentru mașinile din joc
cars = {
    "red_car": {
        "class": RedCar,
        "color": "red",
        "max_vel": 6,
        "rotation_vel": 4,
        "start_pos": (820, 350)
    },
    "blue_car": {
        "class": BlueCar,
        "color": "blue",
        "max_vel": 5,
        "rotation_vel": 2,
        "start_pos": (820, 350)
    },
    "orange_car": {
        "class": OrangeCar,
        "color": "orange",
        "max_vel": 4,
        "rotation_vel": 2,
        "start_pos": (820, 350)
    }
}

# Funcție pentru schimbarea mașinii
def change_car(car_type):
    global player_car
    car_info = cars.get(car_type)
    if car_info:
        player_car = car_info["class"](car_info["max_vel"], car_info["rotation_vel"])
        player_car.x, player_car.y = car_info["start_pos"]  # Setează poziția de start
    reset_game()

# Update background
def update_background(WIN):
    WIN.blit(FINISH, (795, 398))
    WIN.blit(CIRCUIT, (0, 0))
    draw_reset_button(WIN)
    player_car.draw(WIN)
    pygame.display.update()

def draw_speed(WIN, speed, lap_time=None):
    font = pygame.font.Font(None, 36)
    speed_text = font.render(f'Viteza: {int(speed) * 50} km/h', True, WHITE)
    WIN.blit(speed_text, (10, 70))  # Poziționează viteza

    if lap_time is not None:
        lap_time_text = font.render(f'Timp tur: {lap_time:.2f} secunde', True, WHITE)
        WIN.blit(lap_time_text, (10, 110))  # Poziționează timpul


# Game loop
HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 game")
pygame.display.set_icon(LOGGO)
clock = pygame.time.Clock()
screen_state = 0
def draw_main_menu(WIN):
    font = pygame.font.Font(None, 74)
    title = font.render("F1 Racing Game", True, WHITE)
    WIN.blit(title, (WIDTH // 4, HEIGHT // 4))

    font = pygame.font.Font(None, 36)
    text = font.render("Press 1 for Red Car", True, WHITE)
    WIN.blit(text, (WIDTH // 4, HEIGHT // 2 - 40))
    text = font.render("Press 2 for Blue Car", True, WHITE)
    WIN.blit(text, (WIDTH // 4, HEIGHT // 2))
    text = font.render("Press 3 for Orange Car", True, WHITE)
    WIN.blit(text, (WIDTH // 4, HEIGHT // 2 + 40))
    text = font.render("Press ESC to exit", True, WHITE)
    WIN.blit(text, (WIDTH // 4, HEIGHT // 2 + 80))

# Main game loop
running = True
player_car = RedCar(6, 3)
start_time = 0
lap_time = 0
is_racing = False

while running:
    WIN.blit(TITLE, (0, 0))  # Clear the screen
    moved = False
    if screen_state == 0:
        draw_main_menu(WIN)  # Draw main menu
    elif screen_state == 1:
        update_background(WIN)  # Draw game screen
        draw_speed(WIN, player_car.vel, lap_time)  # Include lap time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if 10 <= mouse_pos[0] <= 110 and 10 <= mouse_pos[1] <= 60:
                reset_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                change_car("red_car")
                screen_state = 1  # Ensure we stay on game screen after car selection
            elif event.key == pygame.K_2:
                change_car("blue_car")
                screen_state = 1  # Ensure we stay on game screen after car selection
            elif event.key == pygame.K_3:
                change_car("orange_car")
                screen_state = 1  # Ensure we stay on game screen after car selection
            elif event.key == pygame.K_ESCAPE and screen_state == 0:
                running = False

    if screen_state == 1:  # Game screen logic
        command = pygame.key.get_pressed()
        if command[pygame.K_a]:
            player_car.rotate(left=True)
        if command[pygame.K_d]:
            player_car.rotate(right=True)
        if command[pygame.K_ESCAPE]:
            screen_state = 0
        if command[pygame.K_w]:
            moved = True
            player_car.move_forward()
            if player_car.position(TRACK_LIMITS_MASK):
                player_car.reduce_speed_limits()
            elif player_car.position(DECO_MASK):
                player_car.reduce_speed_deco()
        if command[pygame.K_s]:
            if(player_car.vel > 0):
                player_car.brake()
            else:
                moved = True
                player_car.move_backward()
                if player_car.position(TRACK_LIMITS_MASK):
                    player_car.reduce_speed_limits()
                elif player_car.position(DECO_MASK):
                    player_car.reduce_speed_deco()

        if player_car.position(TRACK_LIMITS_MASK):
            player_car.reduce_speed_limits()

        if player_car.position(WALLS_MASK):
            reset_game()

        if not moved:
            player_car.reduce_speed()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
