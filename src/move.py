
from dataclasses import dataclass
from enum import Enum
from tracemalloc import start
from typing import List, Optional, Tuple

class MoveTypeEnum(Enum):
    NORMAL = 1
    PAWN_DOUBLE_STEP = 2
    KINGSIDE_CASTLING = 3
    QUEENSIDE_CASTLING = 4
    ENPASSANT = 5
    PAWN_PROMOTION = 6
    

@dataclass
class Move:
    start_square: Tuple[int]
    end_square: Tuple[int]
    piece: int
    move_type: MoveTypeEnum
    pawn_promotion_piece: Optional[int] = 0
    
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

    def to_json(self):
        data = {
            "start_square": self. start_square,
            "end_square": self.end_square,
            "piece": self.piece,
            "move_type": self.move_type.value,
            "pawn_promotion_piece": self.pawn_promotion_piece
        }
        return data
    
    @staticmethod
    def from_json(data) -> "Move":
        move = Move(
            start_square = data["start_square"],
            end_square = data["end_square"],
            piece = data["piece"],
            move_type_enum = MoveTypeEnum(data["move_type"]),
            pawn_promotion_piece = data["pawn_promotion_piece"],
        )
        return move

@dataclass
class MoveRecord:
    move: Move
    captured_piece: int
    check: bool
    checkmate: bool

    kingside_castling_possible_before_move: List[bool]
    queenside_castling_possible_before_move: List[bool]
    enpassant_position_before_move: List[Tuple[int]|None]
    
    def to_json(self):
        data = {
            "move": self.move.to_json(),
            "captured_piece": self.captured_piece,
            "check": self.check,
            "kingside_castling_possible_before_move": self.kingside_castling_possible_before_move,
            "queenside_castling_possible_before_move": self.queenside_castling_possible_before_move,
            "enpassant_position_before_move": self.enpassant_position_before_move
        }
    
    @staticmethod
    def from_json(data) -> "MoveRecord":
        record = MoveRecord(
            move = Move.from_json(data["move"]),
            captured_piece = data["captured_piece"],
            check = data["check"],
            checkmate = data["checkmate"],
            kingside_castling_possible_before_move = data["kingside_castling_possible_before_move"],
            queenside_castling_possible_before_move = data["queenside_castling_possible_before_move"],
            enpassant_position_before_move = data["enpassant_position_before_move"]
        )