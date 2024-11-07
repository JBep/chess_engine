
import src.chess_engine
from src.chess_engine import play
from src.chess_board import ChessBoard
import time

from src.evaluation_function import elaborate_evaluation_function


grid = [
        [99]*12,
        [99]*12,
        [99, 99,-4, 0, -3, -5, -6, -3, -2, -4, 99,99],
        [99, 99, -1, -1, -1, 0, 0, -1, -1, -1, 99, 99],
        [99, 99, 0, 0, -2, 0, 0, -1, 0, 0, 99, 99],
        [99, 99, 0, 0, 0, 0, -1, 0, 0, 0, 99, 99],
        [99, 99, 0, 0, 0, 0, 1, 0, 0, 0, 99, 99],
        [99, 99, 0, 0, 2, 1, 0, 2, 0, 0, 99, 99],
        [99, 99, 1, 1, 1, 1, 0, 1, 1, 1, 99, 99],
        [99, 99, 4, 2, 3, 5, 6, 3, 2, 4, 99, 99],
        [99]*12,
        [99]*12
    ]
board = ChessBoard(grid)
move = list(board.legal_moves[board.turn])[0]
src.chess_engine.play(board, elaborate_evaluation_function, 5,1,False, None, None)

play(board, evaluate,1,1)