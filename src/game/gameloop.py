


import pygame, sys
from src.file_utils import read_from_json, save_as_json
from src.chess_engine.chess_engine import play
from src.chess_engine.evaluation_functions.evaluation_function import naive_evaluation_function, elaborate_evaluation_function
from src.chess_engine.evaluation_functions import position_evaluation
from src.constants import GAME_TITLE, HEIGHT, TOTAL_WIDTH, BOT_COLOR, BOT_EVALUATION_DEPTH, VISUALIZE
from src.game.draw_chessboard import animate_holding_piece, animate_moving_piece, draw_board, draw_notepad, draw_pieces
import src.game.events as events
from src.chess_backend.chess_board import ChessBoard
from src.game.drawing_utils import load_background_image, load_notepad_background_image, load_piece_images


BOT_EVALUATION_FUNCTION = position_evaluation.evaluate_position


def run_game(bot:bool, grid = None):
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    piece_images = load_piece_images()
    background_image = load_background_image()
    notepad_background_image = load_notepad_background_image()
    
    
    board = ChessBoard(grid)
    selected_square = None
    
    running = True
    while running:
        
        # Bots turn
        if bot and not board.game_state.game_is_over and board.game_state.turn == BOT_COLOR:
            pygame.time.delay(150)
            move, positions = play(board, BOT_EVALUATION_FUNCTION, BOT_EVALUATION_DEPTH, BOT_COLOR, VISUALIZE, screen, piece_images,background_image)
            animate_moving_piece(screen, board, background_image,piece_images, move.start_square, move.end_square)
            board.move_piece(move)
            pygame.time.delay(150)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_square = events.mousebuttondown()
                
            elif event.type == pygame.MOUSEBUTTONUP and selected_square is not None:
                events.mousebuttonup(board, selected_square)
                selected_square = None
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("\nGrid \n-----------------------------------------")
                    for rank in board.grid:
                        print(rank)
                    
                    print("\nGame State \n-----------------------------------------")
                    for key, val in board.game_state.__dict__.items():
                        if key not in ["grid", "legal_moves"]:
                            print(key, val)
                            
                    print("\nLegal moves \n-----------------------------------------")
                    print(sorted([str(move) for move in board.legal_moves]))
                        
                if event.key == pygame.K_h:
                    print("\nHistory \n-----------------------------------------")
                    for move_record in board.history:
                        print(move_record.move, move_record.game_state)
                    
                if event.key == pygame.K_BACKSPACE:
                    board.undo_move()
                    
                if event.key == pygame.K_b:
                    bot = not bot
                    
                if event.key == pygame.K_p:
                    if positions:
                        with open("positions.txt", "w") as file:
                            for key, value in positions.items():
                                file.write(f"{key}: {value}\n")
                    
                if event.key == pygame.K_r:
                    board = ChessBoard()
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    if keys[pygame.K_s]:
                        game_id = save_as_json(board, "saved_games")
                        
                    if keys[pygame.K_l]:
                        read_from_json("saved_games", game_id)
        
        draw_board(screen, board, background_image,True, True, selected_square)
        draw_notepad(screen, board, notepad_background_image, BOT_EVALUATION_FUNCTION)
        draw_pieces(screen, board, piece_images, selected_square)         
        if selected_square is not None:
            animate_holding_piece(screen, board, piece_images, selected_square)
        pygame.display.flip()
        
           
    pygame.quit()
    sys.exit()
            
        