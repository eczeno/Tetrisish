#!/home/zeno/Desktop/tetris/.tetris/bin/python


import pygame
import random
import sys
from pathlib import Path


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
MOVE_SPEED = 0.1
NEXT_TOP_LEFT_X = 490
NEXT_TOP_LEFT_Y = 150
CYCLES_TO_INCREASE_LEVEL = 10000

SCORE_REFERENCE = {'1': 40, '2': 100, '3': 300, '4': 1200}

scores_PATH = Path('data/scores.txt') 

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
        pygame.display.set_caption('Tetrisish')
        #Generate pieces
        self.current_piece = Piece(4, -2, random.choice(SHAPES))
        self.next_piece = Piece(4, -2, random.choice(SHAPES))
        # Establish grid and filled_blocks dict
        self.filled_blocks = {}
        self.grid = self.make_grid()
        # Adjust starting position of 'I' pieces
        if self.current_piece.name == 'I':
            self.current_piece.x -= 1
        if self.next_piece.name == 'I':
            self.next_piece.x -= 1         
        # Initialize score
        self.score = 0
        # Initialize level
        self.level = 1
        # Load previous scores
        self.scores = self.load_scores()
        self.max_score = max(self.scores['player1'])   
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


    def remove_line(self, i, row):
        for j in range(len(row)):
            self.filled_blocks.pop((j, i))
        move_down = []        
        for x, y in [*self.filled_blocks]:
            if y < i:
                move_down.append((x, y))
        new_blocks = {}
        for x, y in move_down:
            new_blocks[(x, y+1)] = self.filled_blocks.pop((x, y))
        self.filled_blocks.update(new_blocks)
                
    
    def check_lost(self):
        answer = False
        for (x,y) in [*self.filled_blocks]:
            if y < 0:
                answer = True
        return answer

       
    def lock_piece(self):
        coords = [ (self.current_piece.x + block[0], self.current_piece.y + block[1]) 
                   for block in self.current_piece.shape[self.current_piece.orientation] ]
        color = self.current_piece.color
        for block in coords:
            self.filled_blocks[block] = color
        self.current_piece = self.next_piece
        self.next_piece = Piece(4, -2, random.choice(SHAPES))
        if self.next_piece.name == 'I':
            self.next_piece.x -= 1
        # Check for lines to remove:
        remove_count = 0
        for i, row in enumerate(self.grid):
            remove = True
            if BACKGROUND in row:
                remove = False
            if remove:
                self.remove_line(i, row)
                remove_count += 1
        if remove_count:
            self.score += SCORE_REFERENCE[str(remove_count)]
        
        if self.check_lost():
            self.lose_game()
            
    
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

        # Draw header
        pygame.font.init()
        header_font = pygame.font.SysFont('comicsans', 50)
        header = header_font.render('Tetrisish', 1, PURPLE, BACKGROUND)
        self.window.blit(header, ((TOP_LEFT_X + GRID_PX_WIDTH // 2 - header.get_width() // 2), 10))

        # Draw next piece label
        next_font = pygame.font.SysFont('comicsans', 30)
        next_label = next_font.render('Next Piece', 1, GREEN, BACKGROUND)
        self.window.blit(next_label, (NEXT_TOP_LEFT_X - 20, NEXT_TOP_LEFT_Y - 50))

        # Draw current score
        score_font = pygame.font.SysFont('comicsans', 30)
        score_label = score_font.render(f'Score: {self.score}', 1, BLUE)
        self.window.blit(score_label, (TOP_LEFT_X - 130, TOP_LEFT_Y + 130))

        # Draw max score
        max_font = pygame.font.SysFont('comicsans', 25)
        max_label = max_font.render(f'Max Score: {self.max_score}', 1, RED)
        self.window.blit(max_label, (TOP_LEFT_X - 145, TOP_LEFT_Y + 250))

        level_font = pygame.font.SysFont('comicsans', 25)
        level_label = level_font.render(f'Level: {self.level}', 1, CYAN)
        self.window.blit(level_label, (TOP_LEFT_X - 140, TOP_LEFT_Y + 350))

        # Draw next_piece
        for block in self.next_piece.shape[0]:

            pygame.draw.rect(self.window, 
                             self.next_piece.color, 
                             (NEXT_TOP_LEFT_X + block[0]*BLOCK_SIZE, NEXT_TOP_LEFT_Y + block[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                             0
                            )

        # Draw red outline
        pygame.draw.rect(self.window, RED, (TOP_LEFT_X, TOP_LEFT_Y, GRID_PX_WIDTH, GRID_PX_HEIGHT), 5)
        
        # Draw the grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):

                pygame.draw.rect(self.window, 
                                 self.grid[i][j], 
                                 (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                                 0
                                )
        
        # Draw grid lines
        self.draw_grid_lines(self.window, self.grid)


    def lose_game(self):
        
        if 'player1' in self.scores.keys():
            self.scores['player1'].append(self.score)
        else:
            self.scores['player1'] = [self.score]
        self.save_scores()

        self.terminate()


    def terminate(self):        
        pygame.quit()
        sys.exit()


    def save_scores(self):
        with open(scores_PATH, 'w') as scores_file:
            scores_file.write(str(self.scores))

    
    def load_scores(self):
        with open(scores_PATH, 'r') as scores_file:
            return eval(scores_file.read())

    
    def move_left(self):
        self.current_piece.x -= 1                  
        if not self.is_valid_space():
            self.current_piece.x += 1


    def move_right(self):
        self.current_piece.x += 1                     
        if not self.is_valid_space():
            self.current_piece.x -= 1


    def move_down(self):
        self.current_piece.y += 1
        if not self.is_valid_space():
            self.current_piece.y -= 1
            self.lock_piece()

    
    def play(self):
        fall_time = 0
        fall_speed = INIT_FALL_SPEED
        move_time = 0
        cycle_count = 0
        moving_down = False
        moving_left = False
        moving_right = False
        
        
        running = True
        while running:
            fall_time += self.clock.get_rawtime()
            move_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.terminate()
                    elif event.key == pygame.K_RIGHT:
                        # self.move_right()
                        moving_right = True
                    elif event.key == pygame.K_LEFT:
                        # self.move_left()
                        moving_left = True
                    elif event.key == pygame.K_DOWN:
                        # self.move_down()
                        moving_down = True
                    elif event.key == pygame.K_UP:
                        self.current_piece.orientation = (self.current_piece.orientation + 1) % len(self.current_piece.shape)
                        if not self.is_valid_space():
                            self.current_piece.orientation = (self.current_piece.orientation -1) % len(self.current_piece.shape)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        moving_down = False
                    elif event.key == pygame.K_LEFT:
                        moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        moving_right = False
                    
            


            #Check for held down keys:
            if moving_down:
                if move_time/1000 > MOVE_SPEED:
                    self.move_down()
                    move_time = 0
            if moving_left:
                if move_time/1000 > MOVE_SPEED:
                    self.move_left()
                    move_time = 0
            elif moving_right:
                if move_time/1000 > MOVE_SPEED:
                    self.move_right()
                    move_time = 0
            

            # Put piece into grid
            self.grid = self.make_grid()
            if not self.is_valid_space():
                self.lose_game()
            
            for block in self.current_piece.shape[self.current_piece.orientation]:
                x = self.current_piece.x + block[0]
                y = self.current_piece.y + block[1]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color
            
            
            if fall_time/1000 > fall_speed:
                fall_time = 0
                self.move_down()
            
            self.draw_window()
            pygame.display.update()

            
            # Incriment cycle_count
            cycle_count += 1
            if cycle_count % CYCLES_TO_INCREASE_LEVEL == 0:
                self.level += 1
                fall_speed = INIT_FALL_SPEED / self.level



def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

    
