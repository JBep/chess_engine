
from typing import Iterable
from src.board_protocol import BoardProtocol, PieceProtocol
MATERIAL_SCORES = {1:1, 2:3, 3:3, 4:5, 5:9, 6:0}

def naive_evaluation_function(board: BoardProtocol):
    score = 0
    if board.game_is_over:
        score += (2*board.winner.color_index-1)*1000
    score += compute_material_score(board.pieces)
    return score
    
def compute_material_score(pieces: Iterable[PieceProtocol]):
    score = 0
    for piece in pieces:
        color = 2*piece.color.color_index-1 # 1 for white, -1 for black
        score += color * MATERIAL_SCORES[piece.piece_type_id]
        
    return score