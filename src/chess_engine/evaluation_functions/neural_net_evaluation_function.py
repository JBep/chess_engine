


from typing import List
from src.chess_backend.chess_board import ChessBoard
import numpy as np


def neural_net_evaluation_function(board:ChessBoard):
    grid_flattened = np.array(flatten_grid(board.grid))
    np. 

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    
def flatten_grid(grid: List[List[int]]):
    flat_grid = []
    for rank in grid:
        for piece in rank:
            if piece != 99:
                flat_grid.append(piece)