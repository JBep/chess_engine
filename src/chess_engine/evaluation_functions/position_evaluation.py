
import logging
import time
from src.chess_backend.chess_board import ChessBoard
from src.constants import BOARD_START_IDX, COL_RANGE, ROW_RANGE

# Material values for the pieces
material_values = {
    1: 1,
    2: 3,
    3: 3,
    4: 5,
    5: 9,
    6: 1 
}

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
def evaluate_position(board:ChessBoard):
    start = time.time()
    total_score = 0

    # Iterate over the board squares
    for i in ROW_RANGE:
        for j in COL_RANGE:
            piece = board.grid[i][j]
            if piece != 99 and piece != 0:
                piece_type = abs(piece)
                color = piece//piece_type
                # Material score for the piece
                material_score = material_values[piece_type]
                
                # Positional score for the piece
                positional_score = position_boards[piece_type][i-BOARD_START_IDX][j-BOARD_START_IDX]
                
                # Combine material score and positional score
                total_score += (material_score + positional_score)*color
    
    end = time.time()
    return total_score