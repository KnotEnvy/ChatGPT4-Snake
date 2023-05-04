import pygame
import random

pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

snake_block_size = 10
snake_speed = 15

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WINDOW_WIDTH / 6, WINDOW_HEIGHT / 3])

def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, (0, 255, 0), [x[0], x[1], snake_block_size, snake_block_size])

def snake():
    snake_list = []
    length_of_snake = 1

    x = WINDOW_WIDTH / 2
    y = WINDOW_HEIGHT / 2

    x_change = 0
    y_change = 0

    foodx = round(random.randrange(0, WINDOW_WIDTH - snake_block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, WINDOW_HEIGHT - snake_block_size) / 10.0) * 10.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block_size
                    x_change = 0

        x += x_change
        y += y_change

        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            message("You lost!", (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            snake()
            # pygame.quit()
            # quit()

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), [foodx, foody, snake_block_size, snake_block_size])

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                message("You lost!", (255, 0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                snake()
                # pygame.quit()
                # quit()

        draw_snake(snake_block_size, snake_list)

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = round(random.randrange(0, WINDOW_WIDTH - snake_block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, WINDOW_HEIGHT - snake_block_size) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

snake()
