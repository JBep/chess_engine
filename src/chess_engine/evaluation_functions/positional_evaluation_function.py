
import logging
import time

import yaml
from src.log import log_execution
from src.bitboard_utils import get_active_positions
from src.board_protocol import BoardProtocol

# Function to evaluate the position
class PositionalEvaluation:
    
    def __init__(self, path_white_position_board: str = None, path_black_position_board: str = None):
        if path_white_position_board is None:
            path_white_position_board = 'src/chess_engine/evaluation_functions/position_boards/white/naive.yaml'
        if path_black_position_board is None: 
            path_black_position_board = 'src/chess_engine/evaluation_functions/position_boards/white/naive.yaml' 
            
        self.position_board_white = read_position_board(path_white_position_board)
        self.position_board_black = read_position_board(path_black_position_board)
    
    @log_execution
    def evaluate(self,board:BoardProtocol):
        score = 0
        if board.game_is_over:
            score += (2*board.winner.color_index-1)*1000
            
        for piece in board.pieces:
            position = get_active_positions(piece.location)[0]
            idx = abs(piece.piece_type_id)
            if piece.color.color_index == 1:
                score += self.position_board_white[idx][position]
            else:
                score -= self.position_board_black[idx][position]
                
            if abs(idx) != 1:
                idx = abs(idx)

        return score
    
    def save_position_board(self,id: int, color: str, dir: str = 'src/chess_engine/evaluation_functions/position_boards'):
        if color == "white":
            data = self.position_board_white
        else:
            data = self.position_board_black
            
        path = f'{dir}/{color}/{id}'
        with open(path,'w') as file:
            yaml.safe_dump(data, file)
        
def read_position_board(path):
    with open(path,'r') as file:
        data = yaml.safe_load(file)
    return data
    