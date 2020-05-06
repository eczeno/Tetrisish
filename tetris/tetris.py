#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame
import random
import sys


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
INIT_FALL_SPEED = 1

# Colors:
BACKGROUND = (0, 0, 0) #BLACK
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

Z = [[(0,0), (1,0), (1,1), (2,1)], 
     [(1,0), (0,1), (1,1), (0,2)]]

S = [[(0,0), (0,1), (1,1), (1,2)], 
     [(1,0), (2,0), (0,1), (1,1)]]

I = [[(0,0), (1,0), (2,0), (3,0)], 
     [(0,0), (0,1), (0,2), (0,3)]]

T = [[(0,0), (1,0), (2,0), (1,1)], 
     [(1,0), (0,1), (1,1), (1,2)], 
     [(1,0), (0,1), (1,1), (2,1)], 
     [(0,0), (0,1), (1,1), (0,2)]]

L = [[(0,0), (0,1), (0,2), (1,2)],
     [(0,0), (1,0), (2,0), (0,1)],
     [(0,0), (1,0), (1,1), (1,2)],
     [(2,0), (0,1), (1,1), (2,1)]]

J = [[(1,0), (1,1), (0,2), (1,2)],
     [(0,0), (0,1), (1,1), (2,1)],
     [(0,0), (1,0), (0,1), (0,2)],
     [(0,0), (1,0), (2,0), (2,1)]]

SHAPES = [O, Z, S, J, L, T, I]
SHAPE_COLORS = [YELLOW, RED, BLUE, GREEN, CYAN, PURPLE, ORANGE]
SHAPE_NAMES = ['O', 'Z', 'S', 'J', 'L', 'T', 'I']


# Create Classes: Piece
class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.name = SHAPE_NAMES[SHAPES.index(shape)]
        self.orientation = 0
    
    def __repr__(self):
        return f'{name} at ({self.x}, {self.y})'
        

# Create Game class:
class Game():
    """Represents the game itself and the playing loop """
    def __init__(self):
        # pygame.init()
        pygame.init()
        # Create display surface
        self.window = pygame.display.set_mode(SIZE) 
        pygame.display.set_caption('Tetris')
        #Generate pieces
        self.current_piece = Piece(4, 0, random.choice(SHAPES))
        self.next_piece = Piece(4, 0, random.choice(SHAPES))
        # Establish grid and filled_blocks dict
        self.filled_blocks = {}
        self.grid = self.make_grid()
        # Adjust starting position of 'I' pieces
        if self.current_piece.name == 'I':
            self.current_piece.x -= 1
        if self.next_piece.name == 'I':
            self.next_piece.x -= 1       
        # Set clock
        self.clock = pygame.time.Clock()
    

    def is_valid_space(self):
        coords = [ (self.current_piece.x + block[0], self.current_piece.y + block[1]) 
                   for block in self.current_piece.shape[self.current_piece.orientation] ]
        answer = True
        for block in coords:
            x = block[0]
            y = block[1]
            if block in self.filled_blocks:
                answer = False
            elif x < 0 or x > 9:
                answer = False
            elif y > 19:
                answer = False
            
        return answer


    def lock_piece(self):
        coords = [ (self.current_piece.x + block[0], self.current_piece.y + block[1]) 
                   for block in self.current_piece.shape[self.current_piece.orientation] ]
        color = self.current_piece.color
        for block in coords:
            self.filled_blocks[block] = color
        self.current_piece = self.next_piece
        self.next_piece = Piece(4, 0, random.choice(SHAPES))
        if self.next_piece.name == 'I':
            self.next_piece.x -= 1


    def drop_piece(self):
        self.current_piece.y += 1
        if not self.is_valid_space():
            self.current_piece.y -= 1
            self.lock_piece()
        
    
    def draw_grid_lines(self, window, grid):
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        
        for i in range(len(grid)):
            pygame.draw.line(window, LGRAY, (sx, sy + i*BLOCK_SIZE), (sx + GRID_PX_WIDTH, sy + i*BLOCK_SIZE))
            for j in range(len(grid[i])+1):
                pygame.draw.line(window, LGRAY, (sx + j*BLOCK_SIZE, sy), (sx + j*BLOCK_SIZE, sy + GRID_PX_HEIGHT))


    def make_grid(self):
        grid = [[BACKGROUND for _ in range(10)] for _ in range(20)]
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if (i, j) in self.filled_blocks:                    
                    grid[j][i] = self.filled_blocks[(i, j)]
        return grid


    def draw_window(self):
        self.window.fill(BACKGROUND)

        pygame.draw.rect(self.window, RED, (TOP_LEFT_X, TOP_LEFT_Y, GRID_PX_WIDTH, GRID_PX_HEIGHT), 5)
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(
                    self.window, 
                    self.grid[i][j], 
                    (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                    )
        
        self.draw_grid_lines(self.window, self.grid)


    def lose_game(self):
        pass


    def terminate(self):
        pygame.quit()
        sys.exit()

    
    def play(self):
        fall_time = 0
        fall_speed = INIT_FALL_SPEED
        moving_down = False
        moving_left = False
        moving_right = False
        
        running = True
        while running:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.terminate()
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        # moving_right = True                       
                        if not self.is_valid_space():
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        # moving_left = True
                        if not self.is_valid_space():
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        # moving_down = True
                        if not self.is_valid_space():
                            self.current_piece.y -= 1
                            self.lock_piece()
                    elif event.key == pygame.K_UP:
                        self.current_piece.orientation = (self.current_piece.orientation + 1) % len(self.current_piece.shape)
                        if not self.is_valid_space():
                            self.current_piece.orientation = (self.current_piece.orientation -1) % len(self.current_piece.shape)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
                    elif event.key == pygame.K_LEFT:
                        moving_left = False
                    elif event.key == pygame.K_DOWN:
                        moving_down == False
                    

            #Check for held down keys:
            if moving_down:
                self.current_piece.y +=1
                if not self.is_valid_space():
                    self.current_piece.y -= 1
                    moving_down = False
                    self.lock_piece()
            elif moving_left:
                self.current_piece.x -= 1
                if not self.is_valid_space():
                    self.current_piece.x += 1
            elif moving_right:
                self.current_piece.x += 1
                if not self.is_valid_space():
                    self.current_piece.x -= 1
            

            # Put piece into grid
            self.grid = self.make_grid()
            if not self.is_valid_space():
                self.lose_game()
            
            for block in self.current_piece.shape[self.current_piece.orientation]:
                x = self.current_piece.x + block[0]
                y = self.current_piece.y + block[1]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color
            


            
            self.window.fill(BACKGROUND)
            self.draw_window()
            pygame.display.update()

            if fall_time/1000 > fall_speed:
                fall_time = 0
                self.drop_piece()



def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
