import pygame
from .constants import YELLOW, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

# The Game class will enable users to interact with the board and pieces
class Game:
    def __init__(self, window):
        self._init()
        self.window = window # the Game window on your device
        
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def _init(self):
        self.selected = None # which piece is selected
        self.board = Board() # the game will happen on the board so we initialize it inside the Game class
        self.turn = YELLOW # which player's turn
        self.valid_moves = {} # what the current valid moves are for whatever player is playing

    # to reinitialize the game
    def reset(self):
        self._init()
        
    def winner(self):
        return self.board.winner()
        
    def select(self, row, col): # this is a recursive method
        if self.selected: # in case user pressed on some piece
            result = self._move(row, col) 
            # move the selected piece from row and col of the select method to row and col of the move method
            if not result: # if the result is not valid (an empty square selected for example)
                self.selected = None # nothing is selected
                self.select(row, col) # user has to select a new piece (so this is to call the method again)
            
        piece = self.board.get_piece(row, col) # define the piece correspond to selected row and col
        if piece != 0 and piece.color == self.turn: 
        # if the selected piece exists and corresponds to the player's color:
            self.selected = piece # the piece is selected
            self.valid_moves = self.board.get_valid_moves(piece)
            return True # the selection is valid
            
        return False # the selected piece is not valid, try again
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: 
        #(piece == 0 to make sure that where we are going to move the piece is an empty square with no piece on it already!)
            self.board.move(self.selected, row, col) # move the valid selected piece
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped) # remove the eaten pieces from the board
            self.change_turn() # change turn so the second player can play
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move 
            # since moves is a dictionary of tuples (row, col)
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2,
                                                   row * SQUARE_SIZE + SQUARE_SIZE//2),
                                                   radius = 15)
            
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = YELLOW
        else:
            self.turn = WHITE
            
    def get_board(self):
    # just to take the actual board and perform the ai algorithm on it
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()