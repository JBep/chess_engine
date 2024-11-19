import logging
from src.chess_engine.evaluation_functions.positional_evaluation_function import PositionalEvaluation
from src.chess_engine.evaluation_functions.naive_evaluation_function import naive_evaluation_function
from src.chess_backend_v2.piece import PieceTypeEnum
from src.bitboard_utils import activate_position, activate_positions
from src.chess_backend_v2.chess_board import ChessBoard_V2
from src.log import setup_log
from src.game.gameloop import run_game

    
def main():
    setup_log(logging.DEBUG)
    board = ChessBoard_V2()
    
    run_game(
        board,
        bot = False,
        bot_color=0, 
        evaluation_object=PositionalEvaluation(), 
        visualize_bot = False,
        debug = False
        )
    
if __name__ == "__main__":
    main() 
 