
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from src.bitboard_utils import get_active_positions
from src.chess_backend_v2.piece import Piece, PieceTypeEnum

@dataclass
class Move:
    start_bitboard: int
    end_bitboard: int
    
class MoveTypeEnum(Enum):
    NORMAL = 1
    CAPTURE = 2
    ENPASSANT = 3
    CASTLING = 4
    PROMOTION = 5
    PROMOTION_CAPTURE = 6
    

@dataclass
class MoveRecord:
    start_bitboard: int
    end_bitboard: int
    move_type: MoveTypeEnum
    
    # For 50 move rule
    moved_piece_type: PieceTypeEnum
    
    # For enpassant
    enpassant_bitboard: int
    enpassant_capture_bitboard: int
    
    # For captures
    captured_piece: Optional[Piece] = None
    
    # For castling
    rook_start_bitboard: Optional[int] = None
    rook_end_bitboard: Optional[int] = None
    
    def __repr__(self) -> str:
        s = f"Start: {get_active_positions(self.start_bitboard)}"
        s += f", End: {get_active_positions(self.end_bitboard)}"
        s += f", Type: {self.move_type}"
        if self.captured_piece:
            s += f", Captured piece: {self.captured_piece}"
        if self.captured_piece:
            s += f", Enpassant: {get_active_positions(self.enpassant_bitboard)}"
        if self.captured_piece:
            s += f", Enpassant_capture: {get_active_positions(self.enpassant_capture_bitboard)}"
        if self.captured_piece:
            s += f", Rook start: {get_active_positions(self.rook_start_bitboard)}"
        if self.captured_piece:
            s += f", Rook end: {get_active_positions(self.rook_start_bitboard)}"
        return s
