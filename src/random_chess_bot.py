from src.chess_board import ChessBoard
import random

def play(game: ChessBoard):

    # Pick a move
    legal_moves = list[game.legal_moves[game.turn]]
    
    chosen_move = random.choice(legal_moves)
    
    return chosen_move

    