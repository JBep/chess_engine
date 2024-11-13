


from typing import Callable
import pygame, sys
from src.file_utils import read_from_json, save_as_json
from src.chess_engine.chess_engine import play
from src.constants import GAME_TITLE, HEIGHT, TOTAL_WIDTH, BOT_COLOR, BOT_EVALUATION_DEPTH, VISUALIZE
from src.game.draw_chessboard import animate_holding_piece, animate_moving_piece, draw_board, draw_debug_screen, draw_notepad, draw_pieces
import src.game.events as events
from src.board_protocol import BoardProtocol
from src.game.drawing_utils import load_background_image, load_notepad_background_image, load_piece_images



def run_game(board:BoardProtocol, bot:bool, bot_color:bool, bot_evaluation_function: Callable, visualize_bot: bool = False, debug: bool = False, grid = None):
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    piece_images = load_piece_images()
    background_image = load_background_image()
    notepad_background_image = load_notepad_background_image()
    
    selected_square = None
    selected_piece = None
    
    running = True
    while running:
        
        # Bots turn
        if bot and not board.game_is_over and board.turn.color_index == bot_color:
            pygame.time.delay(150)
            end_square, piece, positions = play(board, bot_evaluation_function, BOT_EVALUATION_DEPTH, bot_color, visualize_bot, screen, piece_images,background_image)
            animate_moving_piece(screen, board, background_image, piece_images, piece.location, end_square)
            piece = board.get_piece(piece.location)
            board.play_turn(piece.color, piece.location, end_square, piece) # TODO, fix this
            pygame.time.delay(150)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_square, selected_piece = events.mousebuttondown(board)
                
            elif event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                events.mousebuttonup(board, selected_piece)
                selected_square = None
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    print("\nGame State \n-----------------------------------------")
                    for key, val in board.__dict__.items():
                        print(key, val)
                
                if event.key == pygame.K_t:
                    for piece in board.pieces:
                        board.get_legal_moves(piece)   
                            
                if event.key == pygame.K_h:
                    print("\nHistory \n-----------------------------------------")
                    for move_record in board.history:
                        print(move_record)
                    
                if event.key == pygame.K_BACKSPACE:
                    board.unplay_turn()
                    
                if event.key == pygame.K_b:
                    bot = not bot
                    
                if event.key == pygame.K_p:
                    if positions:
                        with open("positions.txt", "w") as file:
                            for key, value in positions.items():
                                file.write(f"{key}: {value}\n")
                    
                if event.key == pygame.K_r:
                    board.reset()
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    if keys[pygame.K_s]:
                        game_id = save_as_json(board, "saved_games")
                        
                    if keys[pygame.K_l]:
                        read_from_json("saved_games", game_id)
        
        draw_board(screen, board, background_image,False, True, True, selected_square)
        if debug:
            draw_debug_screen(screen, board, evaluation_function=bot_evaluation_function)
        else:
            draw_notepad(screen, board, notepad_background_image, bot_evaluation_function)
        draw_pieces(screen, board, piece_images, selected_square)         
        if selected_square is not None:
            animate_holding_piece(screen, board, piece_images, selected_square)
        pygame.display.flip()
        
           
    pygame.quit()
    sys.exit()
            
        