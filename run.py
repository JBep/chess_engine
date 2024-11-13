import logging
from src.chess_engine.evaluation_functions.positional_evaluation_function import positional_evaluation_function
from src.chess_engine.evaluation_functions.naive_evaluation_function import naive_evaluation_function
from src.chess_backend_v2.piece import PieceTypeEnum
from src.bitboard_utils import activate_position, activate_positions
from src.chess_backend_v2.chess_board import ChessBoard_V2
from src.log import setup_log
from src.game.gameloop import run_game

   

    
def test_promotion(board):
    pieces_to_remove = []
    for piece in board.pieces:
        if piece.location & activate_positions(0,[62,54]):
            pieces_to_remove.append(piece)
            board.black_occupied_squares ^= piece.location
            
        elif piece.location & activate_position(0,14):
            board.white_occupied_squares ^= piece.location
            piece.location = activate_position(0,54)
            board.white_occupied_squares |= piece.location
            piece.move_counter = 4
            
    for piece in pieces_to_remove:
        board.pieces.remove(piece) 
   
def test_dead_position(board):
    pieces_to_remove = []
    for piece in board.pieces:
        if piece.type not in [PieceTypeEnum.KING, PieceTypeEnum.BISHOP, PieceTypeEnum.KNIGHT, PieceTypeEnum.QUEEN]:
            pieces_to_remove.append(piece)

    for piece in pieces_to_remove:
        board.pieces.remove(piece)
        
    board.white_occupied_squares = activate_positions(0,[1,2,4,5,6])
    board.black_occupied_squares = activate_positions(0,[57,58,60,61,62])
    
def main():
    setup_log(logging.DEBUG)
    board = ChessBoard_V2()
    
    run_game(
        board,
        bot = False,
        bot_color=0, 
        bot_evaluation_function=positional_evaluation_function, 
        visualize_bot = False,
        debug = True
        )
    
if __name__ == "__main__":
    main() 
 