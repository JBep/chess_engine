from typing import Tuple
import pygame

from src.chess_backend.move import MoveRecord, MoveTypeEnum
from src.game.drawing_utils import chess_square_to_screen_square, screen_square_to_chess_square, square_to_position
from src.chess_backend.chess_board import ChessBoard
from src.constants import BOARD_START_IDX, TEXT_AREA_WIDTH, HIGHLIGHT, ROWS, COLS, SQUARE_SIZE, TEXT_COLOR, WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR, DEBUG_AREA_COLOR, SQUARE_ALPHA, HIGHLIGHT_CAPTURE
from src.chess_backend.chess_utils import algebraic

def squares_attacked(board: ChessBoard, selected_square: Tuple[int]):
    squares = set()
    selected_chess_square = screen_square_to_chess_square(selected_square)
    for move in board.legal_moves:
        if move.start_square == selected_chess_square:
            squares.add(chess_square_to_screen_square(move.end_square))
            
    return squares 

# Draw the chess board
def draw_notepad(screen, board: ChessBoard, notes_background_image, evaluation_function):
    text_area_x = COLS * SQUARE_SIZE
    text_area_y = 0
    screen.blit(notes_background_image, (text_area_x,text_area_y))
    
    font = pygame.font.SysFont('Arial', 36)  # Use default font and size 36
    padding_x = 100
    padding_y = 100

    text_surface = font.render(f"Current evaluation: {evaluation_function(board)}", True, DEBUG_AREA_COLOR)
    screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
    padding_y += 45
    
    for move_record in board.history:
        text_surface = font.render(f"{algebraic(move_record)}", True, TEXT_COLOR)
        screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
        padding_y += 45
    
    

def draw_board(screen, board: ChessBoard, background_image: pygame.Surface, highlight_last_move: bool, highlight_attack: bool, selected_square):
    smallfont = pygame.font.SysFont('Arial', 10)  # Use default font and size 36
    colors = [WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR]
    
    screen.blit(background_image, (0,0))
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            
            if highlight_last_move and board.history:
                last_move_record: MoveRecord = board.history[-1]
                start_square = chess_square_to_screen_square(last_move_record.move.start_square)
                end_square = chess_square_to_screen_square(last_move_record.move.end_square)

                if (row, col) == start_square:
                    highlight_color = HIGHLIGHT
                    color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
                elif (row, col) == end_square:
                    if last_move_record.move.move_type == MoveTypeEnum.CAPTURE:
                        highlight_color = HIGHLIGHT_CAPTURE
                    else:
                        highlight_color = HIGHLIGHT
                    color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
                
            if highlight_attack and selected_square is not None and (row,col) in squares_attacked(board,selected_square):
                chess_row, chess_col = screen_square_to_chess_square((row,col))
                if board.grid[chess_row][chess_col]*board.game_state.turn < 0:
                    highlight_color = HIGHLIGHT_CAPTURE
                else:
                    highlight_color = HIGHLIGHT
                color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
                
            temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            temp_surface.set_alpha(SQUARE_ALPHA)  # Set opacity
            temp_surface.fill(color)         # Fill with color
            screen.blit(temp_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            
            txt = smallfont.render(f"{screen_square_to_chess_square((row,col))}", True, colors[(row + col + 1) % 2])
            screen.blit(txt, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(screen, board:ChessBoard, piece_images, selected_square):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.grid[BOARD_START_IDX+row][BOARD_START_IDX+col]
            if piece != 0 and (row, col) != selected_square:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def animate_holding_piece(screen, board:ChessBoard, piece_images, selected_square):
    x,y = pygame.mouse.get_pos()
    row, col = selected_square
    piece = board.grid[BOARD_START_IDX+row][BOARD_START_IDX+col]
    if piece != 0:
        piece_image = piece_images[piece]
        screen.blit(piece_image, (x - piece_image.get_width() // 2, y - piece_image.get_height() // 2))
            
def animate_moving_piece(screen, board: ChessBoard, background_image,piece_images, start_square, end_square):
    start_x, start_y = square_to_position(chess_square_to_screen_square(start_square))
    end_x, end_y = square_to_position(chess_square_to_screen_square(end_square))
    
    duration = 0.1
    frames = duration * 60  # Assuming 60 frames per second
    frame_count = 0
    piece = board.grid[start_square[0]][start_square[1]]
    piece_image = piece_images[piece]
    
    while frame_count < frames:
        # Calculate the current position of the piece
        progress = frame_count / frames
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        # Draw the board and the piece
        draw_board(screen, board, background_image, True, False, start_square)
        draw_pieces(screen, board, piece_images, start_square)
        screen.blit(piece_image, (current_x- piece_image.get_width() // 2, current_y- piece_image.get_height() // 2))
        pygame.display.flip()

        frame_count += 1
        pygame.time.delay(1000 // 60)

 
