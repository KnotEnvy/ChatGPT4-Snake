import pygame
import random
import sys
pygame.init()

# Define constants

block_size = 40

# Initialize the num_rows, num_cols, and num_mines variables
num_rows, num_cols, num_mines = 10, 10, 10
# Temporary screen for difficulty selection
temp_screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("KnotzSweep - Choose Difficulty")
# Call difficulty_selection_screen() before setting up the display


# Set up the display
WIDTH = num_cols * block_size
HEIGHT = num_rows * block_size + 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KnotzSweep")



WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)







class Button:
    def __init__(self, text, x, y, width, height, color, font_size):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font_size = font_size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(None, self.font_size)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height



# Define classes
def choose_difficulty():
    difficulties = {
        'easy': (10, 10, 10),
        'medium': (15, 15, 40),
        'hard': (20, 20, 100),
    }
    
    print("Select a difficulty level:")
    for level in difficulties:
        print(f"- {level.capitalize()}")
        
    choice = ""
    while choice.lower() not in difficulties:
        choice = input("Enter your choice: ").lower()
        
    num_rows, num_cols, num_mines = difficulties[choice]
    return num_rows, num_cols, num_mines

def difficulty_selection_screen():
    difficulties = {
        'easy': (10, 10, 10),
        'medium': (15, 15, 40),
        'hard': (20, 20, 100),
    }

    buttons = []
    button_width, button_height = 150, 50
    button_y = HEIGHT // 2 - button_height // 2

    for idx, level in enumerate(difficulties):
        button_x = (WIDTH // (len(difficulties) + 1)) * (idx + 1) - button_width // 2
        button = Button(level.capitalize(), button_x, button_y, button_width, button_height, GREY, 24)
        buttons.append(button)

    selected_difficulty = None
    while selected_difficulty is None:
        screen.fill(WHITE)
        for button in buttons:
            button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(event.pos):
                            selected_difficulty = list(difficulties.values())[idx]
                            break

    return selected_difficulty


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
        self.revealed = [[False for _ in range(num_cols)] for _ in range(num_rows)]
        self.flagged = [[False for _ in range(num_cols)] for _ in range(num_rows)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        positions = random.sample(range(num_rows*num_cols), num_mines)
        for pos in positions:
            row = pos // num_cols
            col = pos % num_cols
            self.grid[row][col] = -1

    def calculate_numbers(self):
        for y in range(num_rows):
            for x in range(num_cols):
                if self.grid[y][x] == -1:
                    continue
                for i in range(max(0, y-1), min(num_rows, y+2)):
                    for j in range(max(0, x-1), min(num_cols, x+2)):
                        if self.grid[i][j] == -1:
                            self.grid[y][x] += 1

    def reveal(self, x, y):
        self.revealed[y][x] = True
        if self.grid[y][x] == -1:
            return False
        if self.grid[y][x] == 0:
            for i in range(max(0, y-1), min(num_rows, y+2)):
                for j in range(max(0, x-1), min(num_cols, x+2)):
                    if not self.revealed[i][j]:
                        self.reveal(j, i)
        return True

    def flag(self, x, y):
        self.flagged[y][x] = not self.flagged[y][x]

    def check_win(self):
        for y in range(num_rows):
            for x in range(num_cols):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

def handle_events(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = (y - 100) // block_size
            col = x // block_size
            if event.button == 1:
                if not board.revealed[row][col]:
                    if not board.reveal(col, row):
                        # Game over
                        draw_board(board)
                        font = pygame.font.SysFont(None, 50)
                        text = font.render("Game Over", True, RED)
                        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        pygame.quit()
                        sys.exit()
                    elif board.check_win():
                        # Game won
                        draw_board(board)
                        font = pygame.font.SysFont(None, 50)
                        text = font.render("You Win!", True, RED)
                        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        pygame.quit()
                        sys.exit()
            elif event.button == 3:
                board.flag(col, row)
            draw_board(board)

def draw_board(board):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 100))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Knotzsweep", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, text_rect)
    for y in range(num_rows):
        for x in range(num_cols):
            rect = pygame.Rect(x * block_size, y * block_size + 100, block_size, block_size)
            pygame.draw.rect(screen, WHITE if board.revealed[y][x] else GREY, rect)

            if board.revealed[y][x]:
                if board.grid[y][x] == -1:
                    pygame.draw.circle(screen, RED, rect.center, block_size // 4)
                elif board.grid[y][x] > 0:
                    font = pygame.font.SysFont(None, block_size // 2)
                    text = font.render(str(board.grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            elif board.flagged[y][x]:
                font = pygame.font.SysFont(None, block_size // 2)
                text = font.render("F", True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    # Draw grid lines
    for i in range(1, num_rows):
        pygame.draw.line(screen, BLACK, (0, i * block_size + 100), (WIDTH, i * block_size + 100))
    for i in range(1, num_cols):
        pygame.draw.line(screen, BLACK, (i * block_size, 100), (i * block_size, HEIGHT))
    pygame.display.update()




num_rows, num_cols, num_mines = difficulty_selection_screen()
board = Board()
draw_board(board)

while True:
    
    handle_events(board)
