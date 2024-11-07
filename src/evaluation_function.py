import math
from src.check import count_attackers, get_king_pos, king_in_check
from src.constants import BOARD_START_IDX
from src.chess_board import ChessBoard
from src.utils import compute_material_score, get_king_squares

# material
BASE_MATERIAL_SCORE = [0,2,12,13,25,45,0]
CENTRAL_SQUARES = [(5,5),(5,6),(6,6),(6,5),(5,7),(6,7),(5,4),(6,4)]

def naive_evaluation_function(board: ChessBoard):
    score = 0
    if board.game_is_over:
        score += board.winner*1000
    score += compute_material_score(board.grid, 1) - compute_material_score(board.grid, -1)
    return score
    
def elaborate_evaluation_function(board: ChessBoard):
    score = 0
    if board.game_is_over:
        score += board.winner*1000
        return score
    
    # Calculate material score and add activity modifier
    score += evaluate_material(board, BASE_MATERIAL_SCORE)
    
    # Evaluate pawn structure
    score += evaluate_pawn_structure(board)
    
    # Evaluate king safety
    score += evaluate_king_safety(board)
    
    return score

def evaluate_material(board: ChessBoard, material_score):
    """Evaluate material score with an activity modifier."""
    score = 0
    for row,rank in enumerate(board.grid):
        for col, piece in enumerate(rank):
            if piece not in [99,0]:
                piece_type = abs(piece)
                color = piece//piece_type
                
                score += color * material_score[piece_type]

                activity_bonus = 0
                if piece_type in {2,3,4,5}:
                    if 4 <= row <= 7 and 4 <= col <= 7:  # center squares
                        activity_bonus = 1
                
                score += color*activity_bonus
    return score
    
    # available_moves = {}
    # for color in [1,-1]:
    #     for move in board.legal_moves[color]:
    #         if move.start_square in available_moves:
    #             available_moves[move.start_square] +=1
    #         else:
    #             available_moves[move.start_square] = 1    
            
    #         if move.end_square in CENTRAL_SQUARES:
    #             score += 0.5*color
        
        
    for row,rank in enumerate(board.grid):
        for col, piece in enumerate(rank):
            if piece not in [99,0]:
                piece_type = abs(piece)
                color = piece//piece_type
                
                # Central control
                if (row,col) in CENTRAL_SQUARES:
                    score += 0.25*color
                
                # Piece activity and score
                if piece_type == 6:
                    defending_units = 0
                    # attacking_units = 0
                    # for square in get_king_squares((row,col)):
                    #     s_row,s_col = square
                    #     if board.grid[s_row][s_col]*color > 0:
                    #         defending_units += 1
                    #     if board.grid[s_row][s_col]*color > 0:
                    #         attacking_units += 1
                    
                    # score += (defending_units/1.5)*color              
                    # score += (attacking_units/1.5)*color*-1              
                else:
                    base_score = BASE_MATERIAL_SCORE[piece_type]
                    #active_multiplier = 1+ math.tanh(available_moves.get((row,col),0))
                    
                    defenders = count_attackers(board.grid, (row,col), color)
                    defender_multipler = 1+ math.tanh(defenders)
                    #score += base_score*color*defender_multipler#*active_multiplier
                    
    return score

def evaluate_pawn_structure(board):
    score = 0
    file_counts = [[0] * 8,[0] * 8,[0] * 8]
    for row,rank in enumerate(board.grid):
        for col, piece in enumerate(rank):
            if abs(piece) == 1:
                color = piece//abs(piece)
                file_counts[color][col-BOARD_START_IDX] += 1

            # Penalties for doubled pawns
    
    for color in [1,-1]:
        doubled_penalty = sum((count - 1) * 3 for count in file_counts[color] if count > 1)
        score -= doubled_penalty*color

    #Penalties for isolated pawns (pawns with no friendly pawns in adjacent files)
    for color in [1,-1]:
        isolated_penalty = 2
        for file in range(8):
            if file_counts[color][file] == 1:  # Check if there's exactly one pawn in this file
                left_file = file - 1
                right_file = file + 1
                if (left_file < 0 or file_counts[color][left_file] == 0) and (right_file > 7 or file_counts[color][right_file] == 0):
                    score -= isolated_penalty*color
    
    return score

def evaluate_king_safety(board):            
    score = 0
    for color in [1,-1]:
        if king_in_check(board.grid, color):
            score -= 15*color
        king_square = get_king_pos(board.grid,color)
        row, col = king_square
        
        # Penalize if there are few pawns near the king
        pawn_protection_penalty = 5
        pawn_count = 0
        
        for neighbor_square in get_king_squares(king_square):
            row, col = neighbor_square
            if board.grid[row][col] == 1*color:
                pawn_count += 1
        
        if pawn_count < 2:
                score -= pawn_protection_penalty*color

    return score


def tanh(x):
    return math.tanh(x)

def get_active_multiplier(piece_type,available_moves):
    if piece_type == 1:
        return available_moves
    else:
        return available_moves/3
    
