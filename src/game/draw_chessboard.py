

from typing import Callable, Tuple
import pygame

from src.bitboard_utils import activate_position, get_active_positions
from src.game.drawing_utils import bitboard_to_screen_squares, chess_square_to_screen_square, square_to_position
from src.board_protocol import BoardProtocol, PieceProtocol
from src.constants import BLUE, HEIGHT, RED, SELECTED_SQUARE_COLOR, TEXT_AREA_WIDTH, HIGHLIGHT, ROWS, COLS, SQUARE_SIZE, TEXT_COLOR, WHITE, WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR, DEBUG_AREA_COLOR, SQUARE_ALPHA, HIGHLIGHT_CAPTURE
from src.chess_backend.chess_utils import algebraic

def squares_attacked(board: BoardProtocol, selected_square: Tuple[int]) -> list:
    row,col = selected_square
    square = activate_position(0, (7-row)*8+col)
    squares = board.get_legal_moves(square)

    if squares == 0:
        return []
    
    positions = get_active_positions(squares)
    squares_attacked = []
    for pos in positions:
        rank, file = pos//8, pos%8
        squares_attacked.append((7-rank ,file))
    
    return squares_attacked

def draw_debug_screen(screen:pygame.Surface, board: BoardProtocol, evaluation_function: Callable):
    text_area_x = COLS * SQUARE_SIZE
    text_area_y = 0
    screen.fill(WHITE,(text_area_x, text_area_y, TEXT_AREA_WIDTH,HEIGHT))
    
    font = pygame.font.SysFont('Arial', 20)  # Use default font and size 36
    padding_x = 10
    padding_y = 10

    text = {}
    text["Position_score"] = evaluation_function(board)
    text["Turn"] = board.turn
    text["white_color_bitboard"] = get_active_positions(board.white_occupied_squares)
    text["black_color_bitboard"] = get_active_positions(board.black_occupied_squares)
    text["enpassant_bitboard"] = get_active_positions(board.enpassant_end_square)
    text["enpassant_capture_bitboard"] = get_active_positions(board.enpassant_capture_square)
    text["game_is_over"] = board.game_is_over
    if board.last_move is not None:
        text["last_move"] = f"{get_active_positions(board.last_move[0])} -> {get_active_positions(board.last_move[1])}"
    text["last_move_was_capture"] = board.last_move_was_capture

    for txt_key, txt_val in text.items():
        text_surface = font.render(f"{txt_key}: {txt_val}", True, DEBUG_AREA_COLOR)
        screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
        padding_y += 30
        
    white_pieces = {}
    black_pieces = {}
    id = 0
    for piece in board.pieces: 
        moves = get_active_positions(board.get_legal_moves(piece))
        
        key: str = f"{id}: {piece.color} {piece.piece_type} {piece.has_moved}"
        val = f"{get_active_positions(piece.location)} -> {moves}"
        if piece.color.color_index == 1:
            white_pieces[key] = val
        else:
            black_pieces[key] = val
        id += 1    
        
    pad_y_temp = padding_y
    for txt_key, txt_val in white_pieces.items():
        text_surface = font.render(f"{txt_key}: {txt_val}", True, DEBUG_AREA_COLOR)
        screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
        padding_y += 30
        
    padding_y = pad_y_temp
    for txt_key, txt_val in black_pieces.items():
        text_surface = font.render(f"{txt_key}: {txt_val}", True, DEBUG_AREA_COLOR)
        screen.blit(text_surface, (text_area_x + padding_x + 600, text_area_y + padding_y))  # Add some padding
        padding_y += 30

# Draw the chess board
def draw_notepad(screen, board: BoardProtocol, notes_background_image, evaluation_object):
    text_area_x = COLS * SQUARE_SIZE
    text_area_y = 0
    screen.blit(notes_background_image, (text_area_x,text_area_y))
    
    font = pygame.font.SysFont('Arial', 36)  # Use default font and size 36
    padding_x = 100
    padding_y = 100

    text_surface = font.render(f"Current evaluation: {evaluation_object.evaluate(board)}", True, DEBUG_AREA_COLOR)
    screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
    padding_y += 45
    
    # for move_record in board.history:
    #     text_surface = font.render(f"{algebraic(move_record)}", True, TEXT_COLOR)
    #     screen.blit(text_surface, (text_area_x + padding_x, text_area_y + padding_y))  # Add some padding
    #     padding_y += 45
    
def draw_board(screen, board: BoardProtocol, background_image: pygame.Surface, highlight_last_move: bool, highlight_attack: bool, visualize_color_bitboards:bool, selected_square):
    smallfont = pygame.font.SysFont('Arial', 14)  # Use default font and size 36
    colors = [WHITE_SQUARE_COLOR, BLACK_SQUARE_COLOR]
    
    screen.blit(background_image, (0,0))
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            if (row, col) == selected_square:
                color = tuple([sum(x)//2 for x in zip(color,SELECTED_SQUARE_COLOR)])
            
            if highlight_last_move and board.last_move:
                start_square, end_square = board.last_move

                if activate_position(0,(7-row)*8+col) == start_square:
                    highlight_color = HIGHLIGHT
                    color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
                elif (row, col) == end_square:
                    if board.last_move_was_capture:
                        highlight_color = HIGHLIGHT_CAPTURE
                    else:
                        highlight_color = HIGHLIGHT
                    color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
                
            if highlight_attack and selected_square is not None and (row,col) in squares_attacked(board,selected_square):
                highlight_color = HIGHLIGHT
                color = tuple([sum(x)//2 for x in zip(color,highlight_color)])
            
            if visualize_color_bitboards:
                if (row, col) in bitboard_to_screen_squares(board.white_occupied_squares):
                    color = tuple([sum(x)//2 for x in zip(color,BLUE)])
                elif (row, col) in bitboard_to_screen_squares(board.black_occupied_squares):
                    color = tuple([sum(x)//2 for x in zip(color,RED)])
                    
            temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            temp_surface.set_alpha(SQUARE_ALPHA)  # Set opacity
            temp_surface.fill(color)         # Fill with color
            screen.blit(temp_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            
            txt = smallfont.render(f"{(7-row)*8+col}", True, colors[(row + col + 1) % 2])
            screen.blit(txt, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
# Draw pieces on the board
def draw_pieces(screen, board:BoardProtocol, piece_images, skipped_piece: PieceProtocol = None):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(activate_position(0,(7-row)*8+col))  
            if piece is not None and piece != skipped_piece:
                screen.blit(piece_images[piece.image_id], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def animate_moving_piece(screen, board: BoardProtocol, background_image, piece:PieceProtocol, piece_images, start_square, end_square):
    start_index = get_active_positions(start_square)[0]
    start_row, start_col = 7-start_index//8, start_index%8
    start_y, start_x = start_row * SQUARE_SIZE+SQUARE_SIZE//2, start_col * SQUARE_SIZE+SQUARE_SIZE//2
    end_index = get_active_positions(end_square)[0]
    end_row, end_col = 7-end_index//8, end_index%8
    end_y, end_x = end_row * SQUARE_SIZE+SQUARE_SIZE//2, end_col * SQUARE_SIZE+SQUARE_SIZE//2

    
    duration = 0.1
    frames = duration * 60  # Assuming 60 frames per second
    frame_count = 0
 
    piece_image = piece_images[piece.image_id]
    
    while frame_count <= frames:
        # Calculate the current position of the piece
        progress = frame_count / frames
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        # Draw the board and the piece
        draw_board(screen, board, background_image, True, False, True,start_square)
        draw_pieces(screen, board, piece_images,piece)
        screen.blit(piece_image, (current_x- piece_image.get_width() // 2, current_y- piece_image.get_height() // 2))
        pygame.display.flip()

        frame_count += 1
        pygame.time.delay(1000 // 60)

 
