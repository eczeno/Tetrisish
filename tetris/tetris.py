#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame
import random


# Set Global Constants
WIDTH = 600
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_PX_WIDTH = 300
GRID_PX_HEIGHT = 600
BLOCK_SIZE = GRID_PX_HEIGHT // GRID_HEIGHT
TOP_LEFT_X = (WIDTH - GRID_PX_WIDTH) // 2
TOP_LEFT_Y = HEIGHT - GRID_PX_HEIGHT
# Colors:
BACKGROUND = (0,0,0) #BLACK
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 200)
RED = (255, 0, 0)
LGRAY = (30, 30, 30)
DGRAY = (185, 185, 185)
WHITE = (255, 255, 255)

# Piece Shapes and Colors
O = [[(0,0), (1,0), (0,1), (1,1)]]
Z = [[(0,0), (1,0), (1,1), (2,1)], [(1,0), (0,1), (1,1), (0,2)]]

SHAPES = [O, Z]
SHAPE_COLORS = [YELLOW, RED]


#TODO: Create Classes: Piece
class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.orientation = 0
        

# Create Game class:
class Game():
    """Represents the game itself and the playing loop """
    def __init__(self):
        # pygame.init()
        pygame.init()
        # Create display surface
        self.window = pygame.display.set_mode(SIZE) 
        pygame.display.set_caption('Tetris')
        self.current_piece = Piece(5, 0, random.choice(SHAPES))
        self.next_piece = Piece(5, 0, random.choice(SHAPES))
        self.filled_blocks = {}
        # Draw grid outline
        self.grid = self.make_grid(self.filled_blocks)
        #TODO: finish init

        self.clock = pygame.time.Clock()

    
    def draw_grid(self, window, grid):
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        
        for i in range(len(grid)):
            pygame.draw.line(window, LGRAY, (sx, sy + i*BLOCK_SIZE), (sx + GRID_PX_WIDTH, sy + i*BLOCK_SIZE))
            for j in range(len(grid[i])+1):
                pygame.draw.line(window, LGRAY, (sx + j*BLOCK_SIZE, sy), (sx + j*BLOCK_SIZE, sy + GRID_PX_HEIGHT))


    def make_grid(self, filled_blocks = {}):
        grid = [[BACKGROUND for _ in range(10)] for _ in range(20)]
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if (i, j) in filled_blocks:                    
                    grid[j][i] = filled_blocks[(i, j)]
        return grid


    def draw_window(self, window, grid):
        pygame.draw.rect(window, RED, (TOP_LEFT_X, TOP_LEFT_Y, GRID_PX_WIDTH, GRID_PX_HEIGHT), 5)
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    window, 
                    grid[i][j], 
                    (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                    )
        
        self.draw_grid(window, grid)



    def terminate(self):
        pygame.quit()

    
    def play(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            # Put piece into grid
            for block in self.current_piece.shape[self.current_piece.orientation]:
                x = self.current_piece.x + block[0]
                y = self.current_piece.y + block[1]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color

       
            self.clock.tick(30)

            self.draw_window(self.window, self.grid)
            pygame.display.update()


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
