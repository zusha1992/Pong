import pygame
import random

WIDTH, HEIGHT = 600, 600
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
VEL = 8
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 10
FPS = 60
pygame.font.init()

main_font = pygame.font.SysFont("comicsans", 50)


class Paddle:
    def __init__(self, x, y, color, up_key, down_key, score_title, score_position):
        self.x = x
        self.y = y
        self.color = color
        self.up_key = up_key
        self.down_key = down_key
        self.score = 0
        self.score_title = score_title
        self.score_position = score_position

    def draw(self, color):
        pygame.draw.rect(WIN, color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT),
                         border_radius=int(PADDLE_WIDTH / 2))
        points = main_font.render(self.score_title + str(self.score), 1, WHITE)
        WIN.blit(points, self.score_position)

    def update_score(self):
        self.score += 1

    def move(self, keys):
        if keys[self.up_key] and self.y > VEL:
            self.y -= VEL
        if keys[self.down_key] and self.y + PADDLE_HEIGHT < HEIGHT - VEL:
            self.y += VEL
        self.draw(self.color)


class Ball:
    def __init__(self, color):
        self.x = 0
        self.y = 0
        self.color = color
        self.direction_x = 0
        self.direction_y = 0
        self.reset()

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), 10)

    def detect_collision(self, paddle):
        horizontal_detection = paddle.x - BALL_SIZE <= self.x <= paddle.x + PADDLE_WIDTH + BALL_SIZE
        vertical_detection = paddle.y <= self.y <= paddle.y + PADDLE_HEIGHT
        return horizontal_detection and vertical_detection

    def reset(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.direction_x = random.choice([-5, -4, -3, 3, 4, 5])
        self.direction_y = random.choice([-5, -4, -3, 3, 4, 5])
        self.draw()

    def update_speed(self, velocity):
        self.direction_x *= velocity
        self.direction_y *= velocity

    def move(self, paddle1, paddle2):
        self.y += self.direction_y
        self.x += self.direction_x
        if self.y - BALL_SIZE < 0 or self.y >= HEIGHT - BALL_SIZE:
            self.direction_y = -self.direction_y
        collision_paddle_1 = self.detect_collision(paddle1)
        collision_paddle_2 = self.detect_collision(paddle2)
        if collision_paddle_1 or collision_paddle_2:
            self.direction_x = -self.direction_x
            self.update_speed(1.1)
        if collision_paddle_1:
            paddle1.draw(WHITE)
        if collision_paddle_2:
            paddle2.draw(WHITE)
        self.draw()

    def is_game_over(self, paddle1, paddle2):
        if self.x < 0:
            paddle2.update_score()
            self.reset()
        if self.x > WIDTH:
            paddle1.update_score()
            self.reset()


def clean_screen():
    pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, HEIGHT))


def game_over_massage(paddle1, paddle2):
    color = ""
    if paddle1.score >= 5:
        color = "Blue "
    elif paddle2.score >= 5:
        color = "Red "
    if color:
        end_massage = main_font.render("Game over!" + color + "is a looser!.", 1, WHITE)
        origin_x = WIDTH / 2 - end_massage.get_width() / 2
        origin_y = HEIGHT / 2
        WIN.blit(end_massage, (origin_x, origin_y, end_massage.get_width(),end_massage.get_height()))

def main():
    run = True
    clock = pygame.time.Clock()
    paddle1 = Paddle(5, 10, BLUE, pygame.K_a, pygame.K_d, "Blue: ", (20, 10, 10, 10))
    paddle2 = Paddle(WIDTH - PADDLE_WIDTH - 5, 10, RED, pygame.K_RIGHT, pygame.K_LEFT, "Red: ",
                     (WIDTH - 127, 10, 10, 10))
    ball = Ball(GREEN)
    lost_count = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clean_screen()
        keys = pygame.key.get_pressed()
        if paddle1.score < 5 and paddle2.score < 5:
            paddle1.move(keys)
            paddle2.move(keys)
            ball.move(paddle1, paddle2)
            ball.is_game_over(paddle1, paddle2)
        else:
            paddle1.draw(paddle1.color)
            paddle2.draw(paddle2.color)
            game_over_massage(paddle1, paddle2)
            lost_count += 1
            if lost_count > FPS * 3:
                run = False

        pygame.display.update()


main()
