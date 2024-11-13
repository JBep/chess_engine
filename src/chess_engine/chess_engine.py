from copy import deepcopy
import logging
import time
from typing import Callable

import pygame
from src.board_protocol import BoardProtocol
from src.log import log_execution_time
from src.game.draw_chessboard import draw_board, draw_pieces


@log_execution_time
def play(board: BoardProtocol, evaluation_function: Callable, depth: int, color:int, visualize: bool, screen, piece_images, background_image):    
    start = time.time()
    maximizing_player = (color == 1)
    positions = {}
    score, end_square, piece = minimax_evaluation(
        board = board, 
        evaluation_function = evaluation_function, 
        depth = depth,
        color = maximizing_player,
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
    
    return end_square, piece, positions

@log_execution_time
def minimax_evaluation(board: BoardProtocol, evaluation_function:Callable, depth:int, color:int, alpha:float, beta:float, visualize, screen, piece_images, positions:dict, node_id, background_image):
    if depth == 0 or board.game_is_over:
        # Base case: return the evaluation score of the current board
        score = evaluation_function(board)
        positions[(node_id)] = (score, alpha, beta)
        return score, None, None
    
    best_move = None
    selected_piece = None
    if color == 1: # white is maximizing player
        best_score = -10e12
    else:
        best_score = 10e12
    
    for piece in board.pieces:
        if piece.color.color_index != color:
            continue
        
        moves_temp = board.get_psuedo_legal_moves(piece)
        moves = []
        while moves_temp: # separating the bitboard into multiple.
            lsb = moves_temp & -moves_temp
            moves.append(lsb)
            moves_temp &= moves_temp -1
        
        for i, move in enumerate(moves):
            board.make_move(
                start_square=piece.location,
                end_square=move, 
                piece = piece)
            
            if board.king_is_in_check(piece.color):
                continue # this is an illegal move, skip it.
            
            if visualize:
                draw_board(
                    screen= screen, board = board, background_image=background_image, 
                    highlight_last_move=False, highlight_attack= False, visualize_color_bitboards = True,
                    selected_square= None)
                draw_pieces(screen, board, piece_images, None)
                pygame.display.flip()
                pygame.time.delay(50)
            
            # Recursively evaluate opponent's best response
            score, _, _ = minimax_evaluation(
                board = board, 
                evaluation_function = evaluation_function, 
                depth = depth - 1, 
                color = 1-color, 
                alpha = alpha, 
                beta = beta, 
                visualize = visualize, 
                screen = screen, 
                piece_images = piece_images, 
                positions = positions, 
                node_id= node_id + (i,),
                background_image=background_image)
            
            board.unmake_move() # Got undo move before potentially breaking the loop
            
            if color == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
                    selected_piece = piece
                    
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    selected_piece = piece
                
                beta = min(beta, score)
                if beta <= alpha:
                    break
        
        
    return best_score, best_move, selected_piece
    