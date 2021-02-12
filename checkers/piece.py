import pygame
from .constants import WHITE, YELLOW, SQUARE_SIZE, GREY, CROWN

class Piece:
    
    # define a class variable
    PADDING = 15
    OUTLINE = 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False # if it's a king piece, it can jump!       
        # the corrdinates of the piece
        self.x = 0
        self.y = 0
        
        # the position of the piece
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        # to make sure the piece is in the middle of the square, so x and y have to be in the middle of the square
        
    def make_king(self):
        self.king = True 
        # to make the piece a king when the occasion comes
        
    def draw(self, window):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)
        # draw a first big circle (it will represent a little shadow under the piece)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        # draw a smaller circle, the actual piece, which will overlap the bigger circle
        if self.king:
            # blit simply means put something on the screen
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
            # to position the image exactly on the piece in the center
    
    def move(self, row, col):
        self.row = row # update the row
        self.col = col # update the col
        self.calc_pos() # to calculate the new position
        
    def __repr__(self):
        return str(self.color)
        # to avoid the <object at x34I...>