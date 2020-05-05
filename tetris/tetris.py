#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame


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


#TODO: Create Classes: Piece
class Piece():
    pass


# Create Game class:
class Game():
    """Represents the game itself and the playing loop """
    def __init__(self):
        # pygame.init()
        pygame.init()
        # Create display surface
        self.window = pygame.display.set_mode(SIZE) 
        pygame.display.set_caption('Tetris')
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
        self.draw_grid(window, grid)


    def terminate(self):
        pygame.quit()

    
    def play(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
        # _check_collision()
        # play()
            # event loop
                #clock.tick(30)
            # update

            # Define frame rate
            self.clock.tick(30)

            self.draw_window(self.window, self.grid)
            pygame.display.update()


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
