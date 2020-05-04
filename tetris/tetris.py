#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame


#TODO: Set Global Constants

#TODO: Create Classes: Game (Tetris?), Block, LeftBlock, RightBlock, TBlock, BlockBlock, FlatBlock


#TODO: Within Game class:
class Game():
    """Represents the game itself and the playing loop """
    def __init__(self):
        # pygame.init()
        pygame.init()
        # Create display surface
        pygame.display.set_mode((400,500)) #TODO: set global variables
        pygame.display.set_caption('Tetris')
        #TODO: finish init

        self.clock = pygame.time.Clock()

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
    # Close the game: TODO: change this
    


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
