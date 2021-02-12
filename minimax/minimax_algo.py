import pygame
from copy import deepcopy # make a copy of the board
# any modification made here will directly impact the original board object

WHITE = (255, 255, 255)
YELLOW = (179, 135, 0)

def minimax(position, depth, max_player, game):
    '''
    position is the current board configuration
    based on the given board, this function will tell us which is the best possible board
    that we should move into
    depth of the decision_tree (how far we will see in order to make our move decision)
    max_player: bool (do we have to maximise or minimize the score)
    game stands for the current game object, passed for visualization purposes
    '''
    if depth == 0 or position.winner() != None:
        # if we are on the root node or in case we already have a winner (no need to continue evaluation)
        # return the current position and its final score
        return position.evaluate(), position
        
    if max_player:
        # if we are not on the root node
        # and in case it is the maximum player, we want to maximize the score (for WHITE player)
        max_eval = float('-inf')
        # whenever we check a new position, we're going to determine which one is the best.
        # and if we haven't check anything yet, then, currently, the best that we've seen is -inf.
        # meaning since we haven't seen anything else (= a score higher than > -inf) we will consider
        # this max_eval as the best until something else comes along and beats it
        best_move = None
        # this will store the best move that we can make
        for move in get_all_moves(position, WHITE, game):
            # for every single move that we can make, we evaluate that move
            # so minimax is called here
            # we evaluate each move, see if it is going to maximize the score, and redo that
            # until we reach depth == 0
            evaluation = minimax(move, depth-1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move # in this case, we found our best move
                
        return max_eval, best_move
    
    else:
        # if we are not on the root node and we want to minimize the score (for YELLOW player)
        min_eval = float('inf')
        best_move = None
        # this will store the best move that we can make
        for move in get_all_moves(position, YELLOW, game):
            # for every single move that we can make, we evaluate that move
            # so minimax is called here
            # we evaluate each move, see if it is going to maximize the score, and redo that
            # until we reach depth == 0
            evaluation = minimax(move, depth-1, True, game)[0]
            # takes True this time for max_player to flip the WHITE player when the minimax function
            # will be recalled (it's a flip flop between WHITE and YELLOW players to compare scores
            # for both sides)
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move # in this case, we found our best move
                
        return min_eval, best_move
    # we want to minimize it otherwise
    
def simulate_move(piece, move, board, game, skip):
    row, col = move[0], move[1]
    board.move(piece, row, col)
    
    if skip:
        board.remove(skip)
        
    return board

def get_all_moves(board, color, game):
    # this function will take all the possible moves from the current position
    moves = [] # this will look like [board, new_board]
    
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
        # skip is to consider any piece that will be removed as a consequence of a given move
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            # the temp_board on which we are going to make all the move trials
            # we make a compy of the actual board, this will not affect its original config
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            # this will take the piece, the move we want to make, the temp_board
            # and then make that move on it, and return to us the new_board
            moves.append(new_board)
            
    return moves

def draw_moves(game, board, piece):
    # this function will draw all the valid moves for a given piece
    valid_moves = board.get_valid_moves(piece) # get all valid moves for this piece
    board.draw(game.window) # redraws the board on the game window
    pygame.draw.circle(game.window, (0, 255, 0), (piece.x, piece.y), 50, 5)
    # draws green circles around the piece with a radius of 50 and a thickness line of 6
    game.draw_valid_moves(valid_moves.keys())
    # draws all the valid moves. Why keys() because valid_moves looks like this {(row,col): [Piece()]}
    pygame.display.update()
    pygame.time.delay(100) # to make the game a little bit slower