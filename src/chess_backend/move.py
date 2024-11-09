
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
from src.chess_backend.chess_utils import algebraic_move
from src.chess_backend.game_state import GameState

class MoveTypeEnum(Enum):
    NORMAL = 1
    CAPTURE = 2
    KINGSIDE_CASTLING = 3
    QUEENSIDE_CASTLING = 4
    PAWN_DOUBLE_STEP = 5
    ENPASSANT = 6
    PAWN_PROMOTION = 7
    

@dataclass
class Move:
    start_square: Tuple[int,int]
    end_square: Tuple[int,int]
    piece: int
    move_type: MoveTypeEnum
    
    captured_piece: Optional[int] = None
    enpassant_capture_square: Optional[Tuple[int,int]] = None # The square where the pawn captured by the enpassant is located.
    pawn_promotion_piece: Optional[int] = 0
    rook_start_square: Optional[Tuple[int,int]] = None
    rook_end_square: Optional[Tuple[int,int]] = None
    
   
    
    def __post_init__(self):
        if self.move_type == MoveTypeEnum.CAPTURE:
            if self.captured_piece is None:
                raise ValueError("Move is set to capture but no captured piece is provided.")
                
        elif self.move_type == MoveTypeEnum.KINGSIDE_CASTLING or self.move_type == MoveTypeEnum.QUEENSIDE_CASTLING:
            if self.rook_start_square is None or self.rook_end_square is None:
                raise ValueError("Move is set to castling but not squares for the rook is provided.")
            
        elif self.move_type == MoveTypeEnum.ENPASSANT:
            if self.enpassant_capture_square is None:
                raise ValueError("Move is set to enpassant but not enpassant square is provided.")
        
    
    def unpack(self):
        start_row, start_col = self.start_square
        end_row, end_col = self.end_square
        return start_row, start_col, end_row, end_col

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            if self.start_square == other.start_square and self.end_square == other.end_square:
                return True
        return False
    
    def __hash__(self) -> int:
        return hash((self.start_square, self.end_square, self.piece, self.move_type, self.pawn_promotion_piece))

    def __repr__(self) -> str:
        return algebraic_move(self)
        
    def to_json(self):
        data = {
            "start_square": self. start_square,
            "end_square": self.end_square,
            "piece": self.piece,
            "move_type": self.move_type.value,
            "captured_piece": self.captured_piece,
            "enpassant_capture_square": self.enpassant_capture_square,
            "pawn_promotion_piece": self.pawn_promotion_piece,
            "rook_start_square": self.rook_start_square,
            "rook_end_square": self.rook_end_square
        }
        return data
    
    @staticmethod
    def from_json(data) -> "Move":
        move = Move(
            start_square = data["start_square"],
            end_square = data["end_square"],
            piece = data["piece"],
            move_type = MoveTypeEnum(data["move_type"]),
            captured_piece = data["captured_piece"],
            enpassant_capture_square = data["enpassant_capture_square"],
            pawn_promotion_piece = data["pawn_promotion_piece"],
            rook_start_square = data["rook_start_square"],
            rook_end_square = data["rook_end_square"],
        )
        return move

@dataclass
class MoveRecord:
    move: Move
    game_state: GameState
    
    def to_json(self):
        data = {
            "move": self.move.to_json(),
            "game_state": self.game_state.to_json()
        }
        return data
    
    @staticmethod
    def from_json(data) -> "MoveRecord":
        record = MoveRecord(
            move = Move.from_json(data["move"]),
            game_state = data["game_state"],
        )
        return record