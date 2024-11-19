


from turtle import update
from typing import Callable
import pygame, sys

from src.log import print_function_stats
from src.file_utils import read_json, write_json
from src.chess_engine.chess_engine import play
from src.constants import GAME_TITLE, HEIGHT, TOTAL_WIDTH, BOT_EVALUATION_DEPTH
from src.game.draw_chessboard import animate_moving_piece, draw_board, draw_debug_screen, draw_notepad, draw_pieces
import src.game.events as events
from src.board_protocol import BoardProtocol
from src.game.drawing_utils import load_background_image, load_notepad_background_image, load_piece_images



def run_game(board:BoardProtocol, bot:bool, bot_color:int, evaluation_object: Callable, visualize_bot: bool = False, debug: bool = False, grid = None):
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    piece_images = load_piece_images()
    background_image = load_background_image()
    notepad_background_image = load_notepad_background_image()
    
    selected_square = None
    selected_piece = None
    
    # Initial drawing
    draw_board(screen, board, background_image,False, True, True, selected_square)
    draw_pieces(screen, board, piece_images)         
    draw_notepad(screen, board, notepad_background_image, evaluation_object)
            
    running = True
    while running:
        update_required = False
        # Bots turn
        if bot and not board.game_is_over and board.turn.color_index == bot_color:
            pygame.time.delay(150)
            end_square, piece, positions = play(
                board=board, 
                evaluation_object=evaluation_object, 
                depth=BOT_EVALUATION_DEPTH, 
                color=bot_color, 
                visualize=visualize_bot, 
                screen=screen, 
                piece_images = piece_images,
                background_image=background_image
                )
            animate_moving_piece(screen, board, background_image, piece, piece_images, piece.location, end_square)
            piece = board.get_piece(piece.location)
            board.play_turn(piece.color, piece.location, end_square, piece) # TODO, fix this
            update_required = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_square is None:
                    print("selecting")
                    selected_square, selected_piece = events.select_piece(board)
                else:
                    print("moving")
                    if selected_piece:
                        end_square = events.move_piece(board, selected_piece)
                        animate_moving_piece(screen, board, background_image, selected_piece, piece_images,selected_piece.location, end_square)
                        board.play_turn(
                            color=selected_piece.color,
                            start_square=selected_piece.location,
                            end_square=end_square,
                            piece = selected_piece
                            )
                    selected_piece = None
                    selected_square = None
                update_required = True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    print("\nGame State \n-----------------------------------------")
                    for key, val in board.__dict__.items():
                        print(key, val)
                
                if event.key == pygame.K_t:
                    for piece in board.pieces:
                        board.get_legal_moves(piece)   
                            
                if event.key == pygame.K_v:
                    visualize_bot = not visualize_bot
                    
                if event.key == pygame.K_h:
                    print("\nHistory \n-----------------------------------------")
                    for move_record in board.history:
                        print(move_record)
                    
                if event.key == pygame.K_BACKSPACE:
                    board.unplay_turn()
                    update_required = True
                    
                if event.key == pygame.K_b:
                    bot = not bot
                    
                if event.key == pygame.K_p:
                    print_function_stats()
                
                if event.key == pygame.K_i:
                    print(f"Positions analyzed: {len(positions)}")
                    with open("positions.txt",'w') as file:
                        lines= "\n".join([f"{key}: {value}" for key, value in positions.items()])
                        file.writelines(lines)
                
                if event.key == pygame.K_r:
                    board.reset()
                    update_required = True
                
                if event.key == pygame.K_s:
                    #Quicksave
                    write_json(board.to_json(), "quicksave", "saved_games")
                if event.key == pygame.K_l:
                    #Quickload
                    board = board.from_json(read_json("quicksave","saved_games"))
                    update_required = True
                    
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    if keys[pygame.K_s]:
                        # TODO implement save method
                        pass
                        
                    if keys[pygame.K_l]:
                        # TODO implement load method.
                        pass
        
        if update_required:
            draw_board(screen, board, background_image, False, True, True, selected_square)
            draw_pieces(screen, board, piece_images)         
            draw_notepad(screen, board, notepad_background_image, evaluation_object)
            
        if debug:
            draw_debug_screen(screen, board, evaluation_object=evaluation_object)
        
        pygame.display.flip()
        
           
    pygame.quit()
    sys.exit()
            
        