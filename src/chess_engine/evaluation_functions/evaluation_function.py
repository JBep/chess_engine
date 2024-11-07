import math
from src.constants import BOARD_START_IDX
from src.chess_backend.chess_board import ChessBoard
from src.chess_backend.chess_utils import compute_material_score, get_king_squares,count_attackers, get_king_pos, king_in_check

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
    if board.game_state.game_is_over:
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
    
