import pygame

from src.drawing_utils import screen_square_to_chess_square
from src.move import Move
from src.chess_board import ChessBoard
from src.constants import BOARD_START_IDX, HEIGHT, SQUARE_SIZE, WIDTH


def mousebuttondown():
    
    x, y = pygame.mouse.get_pos()
    if x > WIDTH or y > HEIGHT:
        return None # Outside clickable area
    
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return row, col

    
def mousebuttonup(board: ChessBoard, selected_square):
    start_square = screen_square_to_chess_square(selected_square)
    x, y = pygame.mouse.get_pos()
    end_square = y // SQUARE_SIZE, x // SQUARE_SIZE   # No need to check clickable area here, outside of board will be illegal move by default
    end_square = screen_square_to_chess_square(end_square)
    
    selected_move = None
    for move in board.legal_moves[board.turn]:
        if move.start_square == start_square and move.end_square == end_square:
            selected_move = move

    if selected_move is not None:
        board.move_piece(selected_move)
    