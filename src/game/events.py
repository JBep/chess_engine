import pygame

from src.board_protocol import BoardProtocol, PieceProtocol
from src.bitboard_utils import activate_position
from src.constants import HEIGHT, SQUARE_SIZE, WIDTH


def mousebuttondown(board: BoardProtocol):
    
    x, y = pygame.mouse.get_pos()
    if x > WIDTH or y > HEIGHT:
        return None # Outside clickable area
    
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    rank, file = 7-row, col  
    square = activate_position(0,rank*8+file)
    
    piece = board.get_piece(square)
    return (row, col), piece

    
def mousebuttonup(board: BoardProtocol, selected_piece: PieceProtocol):
    if selected_piece is None:
        return
    
    start_square = selected_piece.location
    
    x, y = pygame.mouse.get_pos()
    rank, file = 7-y // SQUARE_SIZE, x // SQUARE_SIZE   # No need to check clickable area here, outside of board will be illegal move by default
    end_square = activate_position(0,rank*8+file)
    
    if start_square != end_square:
        
        board.play_turn(
            color=selected_piece.color,
            start_square=start_square,
            end_square=end_square,
            piece = selected_piece
            )
    