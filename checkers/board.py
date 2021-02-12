import pygame
from .constants import BROWN, WHITE, YELLOW, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):      
        # define the pieces in a checkers board (if they are white, if they are red...)
        self.board = []
        # we can imagine, in case of a 3*3 checkers board, that self.board looks like this:
        #[[Piece(), 0, Piece()],  0 if there is nothing in that square
        # [0, Piece(), 0],
        # [0, 0, 0]]
        self.white_left = self.yellow_left = 12 # 
        # 12 because in a checkers game we have 12 pieces for both colors
        self.white_kings = self.yellow_kings = 0
        # (this syntax means if self.red_kings is equal to self.white_kings 
        # and if self.white_kings is equal to 0 
        # then self.red_kings is also equal to 0)
        self.create_board()
        
    def draw_squares(self, window):
        window.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # in each row, step by 2
                pygame.draw.rect(window, 
                                 WHITE, 
                                 (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE,
                                 SQUARE_SIZE,
                                 SQUARE_SIZE))
                # draw a white rectange in the brown window
                
    def evaluate(self): 
    # a method that will calculate the score of the actual board state
        return self.white_left - self.yellow_left + (self.white_kings * 0.5 - self.yellow_kings * 0.5) 
        # number of kings for both players are weighted by 0.5 so that they contribute more to the score than the numbers of normal pieces
        
    def get_all_pieces(self, color):
        # this method counts number of all pieces having the same color
        pieces = []
        
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
                    
        return pieces
    
    def move(self, piece, row, col): 
        # you tell this method the piece you want to move
        # and what row and column you want to move it to
        # to move a piece, we must delete it and change its position (new row and col)
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # this line means that the piece that is in the move, and the piece that is in the position we want to move to, we need to swap their values by simply reversing it like this
        piece.move(row, col) # so the piece move
        # and if it moves to a position that will makes it a king (when it reaches the last row or the first row of the board), 
        # then we make this piece a king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.yellow_kings += 1
                
    def get_piece(self, row, col):
        # this method allows to give the board a certain row and column
        # and the board will give you back a piece object
        return self.board[row][col]
        
    def create_board(self):
        for row in range(ROWS):
            self.board.append([]) # to represent what each row will have inside of it
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2): 
                # to verify where to draw the pieces! 
                # row=0 and col=0 mean that we are on the first line of our board.
                # In our board, the first square (row=0, col=0), which is in brown color, will be skipped.
                # The next square (0, 1) is white, so it must contain a brown piece. 
                # Then the next square (0, 2) is brown, it does not contain any piece. 
                # Then the next square (0, 3) is white, we fill it with a brown piece, and so one. 
                # We then go the second row, starting from the first square at this row (1, 0) and so on...
                    if row < 3:
                    # because, for our board, we want to draw brown pieces only in the first 3 rows of our board
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                    # starting from the fifth row, we start drawing white pieces
                        self.board[row].append(Piece(row, col, YELLOW))
                    else:
                        # the middle squares of the board do not contain any piece
                        self.board[row].append(0)
                else:
                    # when the square do not contain any piece
                    self.board[row].append(0)
                    
    def draw(self, window): # this method will draw the pieces in all the squares
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0: # if the square allowed to contain a piece
                    piece.draw(window) # then draw it on the board
                    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == YELLOW:
                    self.yellow_left -= 1 # update the number of yellow pieces
                else:
                    self.white_left -= 1
                    
    def winner(self):
        if self.yellow_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return YELLOW
        
        return None # in case no one won
                    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        if piece.color == YELLOW or piece.king: # how we are going to move based on the color and the "role" of the piece
            moves.update(self._go_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._go_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            # to exlain this line (_go_left attributes):
            # row-1 because yellow pieces have to go up on the board (= start)
            # max(row-3,-1) we only look at the next 3 rows maximum! Otherwise we go outside the box (= stop)
            # -1 (= step)
            # the piece color (= color) and the direction (= left) to deplace the piece 
        
        if piece.color == WHITE or piece.king:
            moves.update(self._go_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._go_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
            # for white pieces we will go down so the start, stop and step will change here
        
        return moves
        
    def _go_left(self, start, stop, step, color, left, skipped=[]):
        # step is to know how we are moving through the board rows (do we go up or down on the right or left diagonals)
        # skipped: have we skipped any pieces yet?
        moves = {} 
        last = []
        for r in range(start, stop, step):
            if left < 0: # we are going outside of the board (not possible!)
                break # so we break, the piece can no longer go left
            
            current = self.board[r][left] 
            # left will take the col number of where we want to go
            if current == 0: 
            # if at our left it is an empty square
                if skipped and not last:
                    break # no double jump, only one
                elif skipped: 
                # in case find a second piece to eat after the first jump, we can double jump (eat two adversary pieces!!)
                    moves[(r, left)] = last + skipped 
                    # the moves include the last piece (the first one eaten) and the skipped piece (the new one found and to be eaten after the first jump)
                else: # if the square is empty and everything is ok
                    moves[(r, left)] = last 
                    # we add this jump as a valid move
                    # last is the row and col where the adversary piece is
                    
                if last: # if last exists (we have an adversary piece to eat!!)
                    # check if we can make a double jump or a triple jump
                    if step == -1:
                        row = max(r - 3, 0) # define the stop row
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._go_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._go_right(r+step, row, step, color, left+1, skipped=last))
                break
                        
            elif current.color == color: # if at our left it's a piece with the same color
                break # we can't jump through it
            else: # if it's an adversary piece, we can jump through it assuming that it is an empty square next
                last = [current] # we memorize this and we go again in the loop (to gow to the next row and move left) to see if the next square is empty
                
            left -= 1 # left decreases because we are going from COLS to 0 on the board
            
        return moves
            
    def _go_right(self, start, stop, step, color, right, skipped=[]):
        moves = {} 
        last = []
        for r in range(start, stop, step):
            if right >= COLS: # we are going outside of the board (not possible!)
                break # so we break, the piece can no longer go right
            current = self.board[r][right]
            if current == 0: # if at our right it is an empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                    
                if last: # if last exists (we have an adversary piece to eat!!)
                    # check if we can make a double jump or a triple jump
                    if step == -1:
                        row = max(r - 3, 0) # define the stop row
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._go_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._go_right(r+step, row, step, color, right+1, skipped=last))
                break
                        
            elif current.color == color: # if at our right it's a piece with the same color
                break
            else:
                last = [current]
                
            right += 1 # right increases because we are going from 0 to COLS on the board
            
        return moves