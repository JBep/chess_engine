
from board_protocol import BoardProtocol

MATERIAL_SCORES = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 0}

def compute_material_score(board: BoardProtocol):
    score = 0
    for piece in board.pieces:
        color = 2*piece.color.color_index-1 # 1 for white, -1 for black
        score += color * MATERIAL_SCORES[piece.piece_type_id]
        
    return score