import pygame
import random
import math

BG_COLOR = (0, 0, 0)
#FG_COLOR = (114, 222, 194)
FG_COLOR = (255, 255, 255)
WIDTH = 800
HEIGHT = WIDTH
RES = 10
COLS = WIDTH // RES
ROWS = HEIGHT // RES
FPS = 24

random.seed(random.random())
pygame.init()

class Game:
    def __init__(self, width, height, cols, rows) -> None:
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.grid = self.init_grid()

        self.bg_color = BG_COLOR
        self.fg_color = FG_COLOR
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(BG_COLOR)
        pygame.display.set_caption('Golpy')
        
        self.debug = True
    
    def init_grid(self):
        foo = [[0] * self.cols for i in range(self.rows)]
        return foo

    def randomize_grid(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.grid[i][j] = math.floor(random.randrange(2))

        #print(self.grid)
        return self.grid
    
    def count(self, x, y):
        sum = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                sum += self.grid[(x + i + self.cols) % self.rows][(y + j + self.cols) % self.rows]

        sum -= self.grid[x][y]
        return sum

    def update_grid(self):
        next = self.init_grid()
        for i in range(self.cols):
            for j in range(self.rows):
                neighbors = self.count(i, j)
                state = self.grid[i][j]

                if state == 0 and neighbors == 3:
                    next[i][j] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    next[i][j] = 0
                else:
                    next[i][j] = state

        self.grid = next

    def draw_grid(self):
        for i in range(self.cols):
            for j in range(self.rows):
                x = j * RES
                y = i * RES

                #self.fg_color = (255 % int(math.sin(i)) + 1, 255 % int(math.sin(i)) + 1, 255 % int(math.sin(i)) + 1)

                if (self.grid[i][j] == 1):
                    pygame.draw.rect(self.screen, self.fg_color, ((x, y), (RES, RES)))
                elif (self.grid[i][j] == 0):
                    pygame.draw.rect(self.screen, self.bg_color, ((x, y), (RES, RES)))

        if (self.debug):
            font = pygame.font.SysFont('roboto', 30)
            bar_text = font.render(f"Generation: {gen}", False, (0, 0, 0), self.fg_color)
            text_rect = pygame.Rect(0, 30, self.width, self.height)
            text_rect.center = (0, self.height - 25)

            self.screen.blit(bar_text, text_rect)
        
clock = pygame.time.Clock()

board = Game(WIDTH, HEIGHT, COLS, ROWS)
grid = board.randomize_grid()
gen = 0

if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    board.debug = not(board.debug)
        
        board.draw_grid()
        board.update_grid()

        print(f"Generation: {gen}", end = "\r")
        gen += 1

        pygame.display.update()
        
        clock.tick(FPS)