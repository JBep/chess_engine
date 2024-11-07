import pygame
from src.constants import BOARD_START_IDX, SQUARE_SIZE, IMAGE_DIR, TEXT_AREA_WIDTH, HEIGHT, WIDTH


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