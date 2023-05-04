import pygame
import random
import time
import math

pygame.init()

# Define constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define variables
block_size = 20
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Load high score from file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0

# Define classes
class Snake:
    def __init__(self):
        self.segments = [(6, 5), (5, 5), (4, 5)]
        self.direction = "right"
        self.next_direction = "right"

    def move(self):
        head = self.segments[0]
        if self.direction == "right":
            new_head = (head[0] + 1, head[1])
        elif self.direction == "left":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "down":
            new_head = (head[0], head[1] + 1)
        self.segments.insert(0, new_head)
        self.segments.pop()

    def change_direction(self, new_direction):
        if new_direction == "right" and self.direction != "left":
            self.next_direction = "right"
        elif new_direction == "left" and self.direction != "right":
            self.next_direction = "left"
        elif new_direction == "up" and self.direction != "down":
            self.next_direction = "up"
        elif new_direction == "down" and self.direction != "up":
            self.next_direction = "down"

    def add_segment(self):
        tail = self.segments[-1]
        if self.direction == "right":
            new_segment = (tail[0] - 1, tail[1])
        elif self.direction == "left":
            new_segment = (tail[0] + 1, tail[1])
        elif self.direction == "up":
            new_segment = (tail[0], tail[1] + 1)
        elif self.direction == "down":
            new_segment = (tail[0], tail[1] - 1)
        self.segments.append(new_segment)

    def check_collision(self):
        head = self.segments[0]
        if head[0] < 0 or head[0] >= WIDTH/block_size or head[1] < 0 or head[1] >= HEIGHT/block_size:
            return True
        for segment in self.segments[1:]:
            if head == segment:
                return True
        return False

    def check_food(self, food):
        head = self.segments[0]
        if head == food:
            return True
        return False

class Food:
    def __init__(self):
        self.pos = (0, 0)
        self.spawn()

    def spawn(self):
        self.pos = (random.randint(0, WIDTH/block_size-1), random.randint(0, HEIGHT/block_size-1))

class Particle:
    def __init__(self, x, y, color=None, size=5, lifespan=20):
        self.x = x
        self.y = y
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        self.size = size
        self.lifespan = lifespan
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 10)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

        # Add checks for screen boundaries
        if self.x - self.size < 0 or self.x + self.size > WIDTH:
            self.vx = -self.vx
        if self.y - self.size < 0 or self.y + self.size > HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)



class ParticleGroup:
    def __init__(self):
        self.particles = []

    def add(self, particle):
        self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)





# Define functions
def draw_snake(snake, enlarge_head=False):
    for idx, segment in enumerate(snake.segments):
        x = segment[0] * block_size
        y = segment[1] * block_size
        if idx == 0 and enlarge_head:
            pygame.draw.rect(screen, GREEN, (x - block_size, y - block_size, block_size * 3, block_size * 3))
        else:
            pygame.draw.rect(screen, GREEN, (x, y, block_size, block_size))


def draw_food(food):
    x = food.pos[0] * block_size
    y = food.pos[1] * block_size
    pygame.draw.rect(screen, RED, (x, y, block_size, block_size))

def update_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH-120, 10))

def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 10))

def update_time(start_time):
    elapsed_time = round(time.time() - start_time)
    time_text = font.render("Time: " + str(elapsed_time) + "s", True, WHITE)
    screen.blit(time_text, (WIDTH-120, HEIGHT-30))

def end_of_game(score):
    font = pygame.font.SysFont(None, 100)
    score_font = pygame.font.SysFont(None, 70)
    game_over_text = font.render("You Lost!", True, WHITE)
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    score_size = score_font.size("Score: " + str(score))
    screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2 - 50))
    screen.blit(score_text, (WIDTH/2 - score_size[0]/2, HEIGHT/2 - score_size[1]/2 + 50))
    if score > high_score:
        for i in range(10):
            high_score_text = font.render("New High Score!", True, YELLOW)
            screen.blit(high_score_text, (WIDTH/2 - high_score_text.get_width()/2, HEIGHT/2 - high_score_text.get_height()/2 + 150))
            pygame.display.update()
            pygame.time.wait(200)
            screen.fill(BLACK)
            pygame.display.update()
            pygame.time.wait(200)

    pygame.display.update()



# Initialize game
snake = Snake()
food = Food()
score = 0
start_time = time.time()
particle_group = ParticleGroup()
game_over = False
particles = []
enlarge_head = False

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction("right")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("left")
            elif event.key == pygame.K_UP:
                snake.change_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("down")

    # Update snake
    if snake.direction != snake.next_direction:
        snake.direction = snake.next_direction
    snake.move()
    if snake.check_collision():
        game_over = True
        score = 0
        snake = Snake()
        food = Food()
        start_time = time.time()
    if snake.check_food(food.pos):
        score += 10
        snake.add_segment()
        food.spawn()
        head_x, head_y = snake.segments[0]
        for _ in range(30):  # Increase the number of particles
            particle_x = (head_x * block_size) + (block_size // 2)
            particle_y = (head_y * block_size) + (block_size // 2)
            particle_group.add(Particle(particle_x, particle_y))  # Add the particle to the group
        enlarge_head = True





    # Draw screen
    screen.fill(BLACK)
    draw_snake(snake, enlarge_head=enlarge_head)
    draw_food(food)
    update_score(score)
    update_high_score(score)
    update_time(start_time)
    # Update and draw particles
    particle_group.update()
    particle_group.draw(screen)


    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        if particle.lifespan <= 0:
            particles.remove(particle)
        else:
            particle.draw(screen)

    if game_over:
        end_of_game(score)
        pygame.time.wait(2000)  # Add a 2-second delay before resetting the game
        game_over = False
        score = 0
        snake = Snake()
        food = Food()
        start_time = time.time()
    pygame.display.update()

    # Limit FPS
    clock.tick(10)
    enlarge_head = False
