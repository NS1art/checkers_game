import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, YELLOW
from checkers.game import Game

FPS = 60 # in seconds

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE # (if the square size is 700 then we will get the row 7)
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    # define a clock if we want our game to run in a constant frame rate
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(FPS) # to make sure the main event loop does not run too fast or too slow
        
        if game.winner() != None:
            print(game.winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quitting game event
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # pressing buttons
                # when we click, pygame will take the position of our 'click'
                pos = pygame.mouse.get_pos()
                # take the row and column corresponding to this position
                row, col = get_row_col_from_mouse(pos)
                # the board will recognize the piece in these row and column
                game.select(row, col)
                
        game.update()
                
    pygame.quit()
    
main()