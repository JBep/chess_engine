
import logging
import time
from src.bitboard_utils import get_active_positions
from src.board_protocol import BoardProtocol

# Example position board for different pieces (a 8x8 grid where each value corresponds to a positional advantage)
position_boards = {
    1: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    -1: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [7, 7, 7, 7, 7, 7, 7, 7],
        [8, 8, 8, 8, 8, 8, 8, 8],
    ],
    2: [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 1, 1, 0, -2, -4],
        [-3, 0, 2, 3, 3, 2, 0, -3],
        [-3, 1, 3, 4, 4, 3, 1, -3],
        [-3, 1, 3, 4, 4, 3, 1, -3],
        [-3, 0, 2, 3, 3, 2, 0, -3],
        [-4, -2, 0, 1, 1, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5],
    ],
    3: [
        [-2, -1, 0, 1, 1, 0, -1, -2],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-2, -1, 0, 1, 1, 0, -1, -2],
    ],
    4: [
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 2, 2, 1, 1, 0],
        [0, 1, 1, 2, 2, 1, 1, 0],
        [1, 2, 2, 3, 3, 2, 2, 1],
        [1, 2, 2, 3, 3, 2, 2, 1],
        [0, 1, 1, 2, 2, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
    ],
    5: [
        [-2, -1, 0, 1, 1, 0, -1, -2],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-2, -1, 0, 1, 1, 0, -1, -2],
    ],
    6: [
    [10, 5, 5, 5, 5, 5, 5, 10],  # Row 8 (back rank)
    [5, 5, 5, 5, 5, 5, 5, 5],
    [5, 3, 3, 3, 3, 3, 3, 5],
    [5, 3, 0, -5, -5, 0, 3, 5],
    [5, 3, 0, -5, -5, 0, 3, 5],
    [5, 3, 3, 3, 3, 3, 3, 5],
    [5, 5, 5, 5, 5, 5, 5, 5],  # Row 1 (back rank)
    [10, 5, 5, 5, 5, 5, 5, 10],  # Row 1 (back rank)
]
}

# Function to evaluate the position
def positional_evaluation_function(board:BoardProtocol):
    score = 0
    if board.game_is_over:
        score += (2*board.winner.color_index-1)*1000
        
    for piece in board.pieces:
        idx = piece.piece_type_id
        if abs(idx) != 1:
            idx = abs(idx)
    
        position_score = position_boards[idx]
        position = get_active_positions(piece.location)[0]
    
        score += (2*piece.color.color_index-1)*position_score[position//8][position%8]
    return score
