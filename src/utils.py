from typing import List, Tuple
import pygame
from src.move import MoveRecord
from src.constants import BOARD_START_IDX, HEIGHT, SQUARE_SIZE, TEXT_AREA_WIDTH, WIDTH, IMAGE_DIR

def algebraic(move_record:MoveRecord):
    move = coord_to_algebraic(move_record.move.start_square)
    piece = piece_to_algebraic(move_record.move.piece)

    if move_record.captured_piece:
        capture = 'x'
    else:
        capture = ''

    if move_record.check:
        suffix = "+"
    if move_record.checkmate:
        suffix = "#"
    else:
        suffix = ""
    note = f"{piece}{capture}{move}{suffix}"
    return note

def load_notepad_background_image():
    image = pygame.image.load(f"{IMAGE_DIR}/notepad.png")
    resized_image = pygame.transform.scale(image, (TEXT_AREA_WIDTH, HEIGHT))
    return resized_image

def load_background_image():
    image = pygame.image.load(f"{IMAGE_DIR}/background.png")
    resized_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    return resized_image

def load_piece_images():
    piece_images = {}
    pieces = pygame.image.load(f"{IMAGE_DIR}/pieces.png")
    width, height = pieces.get_size()
    piece_width, piece_height = width/6, height/2
    new_width, new_height = SQUARE_SIZE, SQUARE_SIZE
    piece_ids = [6,5,3,2,4,1]
    for i in range(6):
        for j in range(2):
            rect = pygame.Rect(i*piece_width, j*piece_height,piece_width, piece_height)
            image = pieces.subsurface(rect)
            resized_image = pygame.transform.scale(image, (new_width, new_height))
            piece_id = piece_ids[i]*(-2*j +1)
            piece_images[piece_id] = resized_image
    return piece_images

def coord_to_algebraic(square) -> str:
    """Assumes a 8x8 grid, i.e., (0,0) -> a8 """
    row, col = square
    row, col = row-BOARD_START_IDX, col-BOARD_START_IDX
    files =     ['a','b','c','d','e','f','g','h']
    file = files[col]
    rank = 8-row
    return f"{file}{rank}"

def algebraic_to_coord(algebraic) -> Tuple[int]:
    """Assumes a 8x8 grid, i.e., a8 -> (0,0) """
    file, rank = algebraic
    files =     ['a','b','c','d','e','f','g','h']
    col = files.index(file)
    row = 8-int(rank)
    return row, col
    
def piece_to_algebraic(piece:int) -> str:
    notation = ['','N','B','R','Q','K']
    return notation[abs(piece)-1]

def compute_material_score(board, color:int):
    scores = [0,1,3,3,5,9,0] # King is 0
    score = 0
    for rank in board:
        for piece in rank:
            if piece != 99 and piece*color > 0:
                score += scores[piece*color]
    return score

def square_within_board(square):
    row, col = square
    return all([row >= 0, row <=7,col >= 0, col <=7])

def get_knight_squares(square: Tuple[int]) -> List[Tuple[int]]:
    row, col = square
    return {
        (-1+row,2+col),
        (-1+row,-2+col),
        (1+row,2+col),
        (1+row,-2+col),
        (2+row,1+col),
        (2+row,-1+col),
        (-2+row,1+col),
        (-2+row,-1+col)
    }

def get_king_squares(square: Tuple[int]):
    squares = []
    start_row, start_col = square
    for i in [1, -1]:
        squares.extend([
            (start_row + i, start_col),
            (start_row + i, start_col + i),
            (start_row + i, start_col - i),
            (start_row, start_col + i)
        ]) 
    return squares