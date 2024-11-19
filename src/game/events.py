import pygame

from src.board_protocol import BoardProtocol, PieceProtocol
from src.bitboard_utils import activate_position
from src.constants import HEIGHT, SQUARE_SIZE, WIDTH


def select_piece(board: BoardProtocol):
    
    x, y = pygame.mouse.get_pos()
    if x > WIDTH or y > HEIGHT:
        return None,None # Outside clickable area
    
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    rank, file = 7-row, col  
    square = activate_position(0,rank*8+file)
    
    piece = board.get_piece(square)
    if piece is None:
        return None,None
    else:
        return (row, col), piece

    
def move_piece(board: BoardProtocol, selected_piece: PieceProtocol):
    start_square = selected_piece.location
    
    x, y = pygame.mouse.get_pos()
    rank, file = 7-y // SQUARE_SIZE, x // SQUARE_SIZE   # No need to check clickable area here, outside of board will be illegal move by default
    end_square = activate_position(0,rank*8+file)
    
    return end_square
    