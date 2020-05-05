#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame


#TODO: Set Global Constants
BACKGROUND = (0,0,0) #BLACK
WIDTH = 600
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
GRID_WIDTH = 300
GRID_HEIGHT = 600


#TODO: Create Classes: Game (Tetris?), Block, LeftBlock, RightBlock, TBlock, BlockBlock, FlatBlock


# Create Game class:
class Game():
    """Represents the game itself and the playing loop """
    def __init__(self):
        # pygame.init()
        pygame.init()
        # Create display surface
        pygame.display.set_mode(SIZE) 
        pygame.display.set_caption('Tetris')
        self.filled_blocks = {}
        # Draw grid outline
        self.grid = self.make_grid(self.filled_blocks)
        #TODO: finish init

        self.clock = pygame.time.Clock()

    def make_grid(self, filled_blocks = {}):
        grid = [[BACKGROUND for _ in range(10)] for _ in range(20)]
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if (i, j) in filled_blocks:                    
                    grid[j][i] = filled_blocks[(i, j)]
        return grid

    # define functions:
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

   
    


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
