import pygame
import math
from func import scale
from func import blit_rotate
import time

# Inițializarea modulului pygame
pygame.init()

# Încărcarea resurselor grafice
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
FINISH_POSITION = (795, 398)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Funcție pentru desenarea butonului de resetare
def draw_reset_button(WIN):
    font = pygame.font.Font(None, 36)
    text = font.render('Reset', True, WHITE)
    pygame.draw.rect(WIN, RED, [10, 10, 100, 50])
    WIN.blit(text, (20, 20))

# Funcție pentru resetarea jocului
def reset_game():
    global player_car, lap_start_time, finish_crossed, laps_completed
    player_car.vel = 0
    player_car.x, player_car.y = player_car.START_POS
    player_car.angle = 180  # Resetare unghi mașină
    lap_start_time = time.time()
    finish_crossed = False
    laps_completed = 0
    update_background(WIN)

# Funcție pentru afișarea timpului ultimei ture
def render_lap_time(screen, time):
    if laps_completed > 1:
        font = pygame.font.Font(None, 36)
        lap_time_text = font.render(f"Last Lap: {time:.2f} seconds", True, (255, 255, 255))
        screen.blit(lap_time_text, (160, 10))
# Funcție pentru afișarea timpului curent al turei
def render_current_lap_time(screen, lap_start_time):
    """Afișează timpul curent al turului pe ecran."""
    current_time = time.time() - lap_start_time
    font = pygame.font.Font(None, 36)
    current_lap_time_text = font.render(f"Current Lap: {current_time:.2f} seconds", True, (255, 255, 255))
    screen.blit(current_lap_time_text, (160, 40))


# Clasa abstractă pentru mașini
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

    # Funcție pentru rotația mașinii
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    # Funcție pentru desenarea mașinii pe ecran
    def draw(self, win):
        blit_rotate(win, self.img, (self.x, self.y), self.angle)

    # Funcții pentru deplasarea mașinii
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

    # Funcție pentru frânare
    def brake(self):
        self.vel = max(self.vel - self.acceleration, 0)

    # Reducerea vitezei în condiții normale
    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration * 0.1, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration * 0.1, 0)
        self.move()

    # Reducerea vitezei la limitele pistei
    def reduce_speed_limits(self):
        if self.vel > self.max_vel / 2:
            self.vel = max(self.vel - self.acceleration * 0.5, 0)

    # Reducerea vitezei la decor
    def reduce_speed_deco(self):
        if self.vel > 1:
            self.vel = max(self.vel - self.acceleration * 2, 0)

    # Determinarea poziției mașinii pe pistă folosind masca
    def position(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

# Clase pentru diferite tipuri de mașini
class RedCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (815, 350)

class BlueCar(AbstractCar):
    IMG = BLUE_CAR
    START_POS = (815, 350)

class OrangeCar(AbstractCar):
    IMG = ORANGE_CAR
    START_POS = (815, 350)

# Dicționar pentru stocarea caracteristicilor mașinilor
cars = {
    "red_car": {"class": RedCar, "max_vel": 6, "rotation_vel": 4, "start_pos": (820, 350)},
    "blue_car": {"class": BlueCar, "max_vel": 5, "rotation_vel": 2, "start_pos": (820, 350)},
    "orange_car": {"class": OrangeCar, "max_vel": 4, "rotation_vel": 2, "start_pos": (820, 350)}
}

# Funcție pentru schimbarea mașinii
def change_car(car_type):
    global player_car
    car_info = cars.get(car_type)
    if car_info:
        player_car = car_info["class"](car_info["max_vel"], car_info["rotation_vel"])
        player_car.x, player_car.y = car_info["start_pos"]
    reset_game()

# Funcție pentru actualizarea fundalului
def update_background(WIN):
    WIN.blit(FINISH, (795, 398))
    WIN.blit(CIRCUIT, (0, 0))
    draw_reset_button(WIN)
    player_car.draw(WIN)
    pygame.display.update()

# Funcție pentru afișarea vitezei
def draw_speed(WIN, speed):
    font = pygame.font.Font(None, 36)
    speed_text = font.render(f'Viteza: {int(speed) * 50} km/h', True, WHITE)
    WIN.blit(speed_text, (10, 70))

# Setări generale pentru joc
HEIGHT = TRACK.get_height()
WIDTH = TRACK.get_width()
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 game")
pygame.display.set_icon(LOGGO)
clock = pygame.time.Clock()
screen_state = 0

# Variabile pentru gestionarea turelor
lap_start_time = time.time()
lap_times = []
finish_crossed = False
previous_lap_time = 0
laps_completed = 0

# Funcție pentru desenarea meniului principal
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

# Bucle principal al jocului
running = True
player_car = RedCar(6, 3)

while running:
    WIN.blit(TITLE, (0, 0))
    moved = False

    if screen_state == 0:
        draw_main_menu(WIN)
    elif screen_state == 1:
        update_background(WIN)
        draw_speed(WIN, player_car.vel)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if 10 <= mouse_pos[0] <= 110 and 10 <= mouse_pos[1] <= 60:
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                change_car("red_car")
                screen_state = 1
            elif event.key == pygame.K_2:
                change_car("blue_car")
                screen_state = 1
            elif event.key == pygame.K_3:
                change_car("orange_car")
                screen_state = 1
            elif event.key == pygame.K_ESCAPE and screen_state == 0:
                running = False

    if screen_state == 1:
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
            if player_car.vel > 0:
                player_car.brake()
            else:
                moved = True
                player_car.move_backward()
                if player_car.position(TRACK_LIMITS_MASK):
                    player_car.reduce_speed_limits()
                elif player_car.position(DECO_MASK):
                    player_car.reduce_speed_deco()
        if player_car.position(WALLS_MASK):
            reset_game()

        if player_car.position(FINISH_MASK):
            if not finish_crossed:
                lap_end_time = time.time()
                lap_time = lap_end_time - lap_start_time
                lap_start_time = lap_end_time
                laps_completed += 1  # Incrementăm turele complete doar dacă linia este traversată
                if laps_completed > 1:  # Afișăm timpul doar după ce s-au realizat cel puțin 2 ture
                    lap_times.append(lap_time)
                    previous_lap_time = lap_time
                finish_crossed = True
        else:
            finish_crossed = False

        if not moved:
            player_car.reduce_speed()
        render_current_lap_time(WIN, lap_start_time)
        render_lap_time(WIN, previous_lap_time)
    pygame.display.flip()
    clock.tick(FPS)

# Afișarea turelor în consolă
j = 1
for i, lap_time in enumerate(lap_times):
    if lap_time > 7:
        print(f"Lap {j}: {lap_time:.2f} seconds")
        j += 1

pygame.quit()
