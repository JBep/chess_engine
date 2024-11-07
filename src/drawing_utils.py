
from src.constants import BOARD_START_IDX, SQUARE_SIZE


def square_to_position(square):
    row,col = square
    x = SQUARE_SIZE * col + SQUARE_SIZE//2
    y = SQUARE_SIZE * row + SQUARE_SIZE//2
    
    return x,y
    
def position_to_square(position):
    x,y = position
    row, col = BOARD_START_IDX + y // SQUARE_SIZE, BOARD_START_IDX + x // SQUARE_SIZE
    
    return row, col

def screen_square_to_chess_square(square):
    row, col = square
    return row + BOARD_START_IDX, col + BOARD_START_IDX


def chess_square_to_screen_square(square):
    row, col = square
    return row-BOARD_START_IDX, col - BOARD_START_IDX