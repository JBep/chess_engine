import logging
import time
from typing import Callable

import pygame
from src.log import log_execution_time
from src.game.draw_chessboard import draw_board, draw_pieces
from src.chess_backend.chess_board import ChessBoard

@log_execution_time
def play(board: ChessBoard, evaluation_function: Callable, depth: int, color:int, visualize: bool, screen, piece_images, background_image):    
    start = time.time()
    maximizing_player = (color == 1)
    positions = {}
    score, chosen_move = minimax_evaluation(
        board = board, 
        evaluation_function = evaluation_function, 
        depth = depth,
        maximizing_player = maximizing_player,
        alpha = -10e12,
        beta = 10e12,
        visualize = visualize, 
        screen = screen, 
        piece_images = piece_images,
        positions = positions,
        node_id = (1,),
        background_image=background_image
        )
    end = time.time()
    print(f"Evaluated {len(positions.keys())} positions in {end-start} seconds.")
    print(f"Chosen move score: {score}")
    
    return chosen_move, positions

@log_execution_time
def minimax_evaluation(board: ChessBoard, evaluation_function:Callable, depth:int, maximizing_player:bool, alpha:float, beta:float, visualize, screen, piece_images, positions:dict, node_id, background_image):
    if depth == 0 or board.game_state.game_is_over:
        # Base case: return the evaluation score of the current board
        score = evaluation_function(board)
        positions[(node_id)] = (score, alpha, beta)
        return score, None
    
    available_moves = board.legal_moves
    best_move = None

    if maximizing_player:
        best_score = -10e12
    else:
        best_score = 10e12
        
    for i, move in enumerate(available_moves):
        start = time.time()
        end = time.time()
        logging.log(logging.DEBUG, f"Copying board took {end-start} seconds.")
        board.move_piece(move)
        if visualize:
            draw_board(screen, board, background_image, False, False, None)
            draw_pieces(screen, board, piece_images, None)
            pygame.display.flip()
        
        # Recursively evaluate opponent's best response
        score, _ = minimax_evaluation(
            board = board, 
            evaluation_function = evaluation_function, 
            depth = depth - 1, 
            maximizing_player = not maximizing_player, 
            alpha = alpha, 
            beta = beta, 
            visualize = visualize, 
            screen = screen, 
            piece_images = piece_images, 
            positions = positions, 
            node_id= node_id + (i,),
            background_image=background_image)
        
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        else:
            if score < best_score:
                best_score = score
                best_move = move
            
            beta = min(beta, score)
            if beta <= alpha:
                break
        
        board.undo_move()
        
    return best_score, best_move
    
def flatten_moves(legal_moves):
    moves = []
    for key, move_set in legal_moves.items():
        if move_set:
            for move in move_set:
                moves.append((key,move))
    return moves


