from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set
from src.bitboard_utils import activate_position

class ColorEnum(Enum):
    WHITE = 1
    BLACK = 2

    @property
    def color_index(self) -> int:
        if self == ColorEnum.WHITE:
            return 1
        else:
            return 0

    def opposite_color(self) -> "ColorEnum":
        if self == ColorEnum.WHITE:
            return ColorEnum.BLACK
        else:
            return ColorEnum.WHITE
    

class PieceTypeEnum(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    KINGSIDE_ROOK = 41
    QUEENSIDE_ROOK = 42
    QUEEN = 5
    KING = 6
    
    def __repr__(self) -> str:
        if self.value in [41,42]:
            return "Rook"
        else:
            s = self.name.lower()
            s = s[0].upper() + s[1:]
            return s
        
@dataclass(eq = True, unsafe_hash= True)
class Piece:
    color: ColorEnum
    location: int 
    type: PieceTypeEnum
    
    legal_moves: Optional[int] = 0
    move_counter: Optional[bool] = 0
    psuedo_legal_moves: Optional[int] = 0
    
    @property
    def image_id(self) -> int:
        type_image_id = int(str(self.type.value)[0])
        color_id = -2*self.color.value+3
        return color_id*type_image_id
    
    @property
    def has_moved(self):
        return self.move_counter != 0
    
    @property
    def piece_type(self) -> str:
        return str(self.type)
    
    @property
    def piece_type_id(self) -> str:
        return int(str(self.type.value)[0])
    
def initialize_pieces() -> dict[int,Piece]:
    white_pawns = []
    for i in range(8,16):
        white_pawns.append(
            Piece(
                type = PieceTypeEnum.PAWN,
                color = ColorEnum.WHITE,
                location = activate_position(bitboard = 0, position = i)
            )
        )
    
    black_pawns = []
    for i in range(48,56):
        black_pawns.append(
            Piece(
                type = PieceTypeEnum.PAWN,
                color = ColorEnum.BLACK,
                location = activate_position(bitboard = 0, position = i)
            )
        )
    other_pieces = []
    other_pieces.extend([
        Piece(
            type = PieceTypeEnum.KINGSIDE_ROOK,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 0)
        ),
        Piece(
            type = PieceTypeEnum.QUEENSIDE_ROOK,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 7)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 1)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 6)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 2)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 5)
        ),
        Piece(
            type = PieceTypeEnum.KING,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 4)
        ),
        Piece(
            type = PieceTypeEnum.QUEEN,
            color = ColorEnum.WHITE,
            location = activate_position(bitboard = 0, position = 3)
        ),
        
        # BLACK PIECES
        Piece(
            type = PieceTypeEnum.KINGSIDE_ROOK,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 56)
        ),
        Piece(
            type = PieceTypeEnum.QUEENSIDE_ROOK,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 63)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 57)
        ),
        Piece(
            type = PieceTypeEnum.KNIGHT,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 62)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 58)
        ),
        Piece(
            type = PieceTypeEnum.BISHOP,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 61)
        ),
        Piece(
            type = PieceTypeEnum.KING,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 60)
        ),
        Piece(
            type = PieceTypeEnum.QUEEN,
            color = ColorEnum.BLACK,
            location = activate_position(bitboard = 0, position = 59)
        ) ]
    )
    pieces = []
    pieces.extend(white_pawns)
    pieces.extend(black_pawns)
    pieces.extend(other_pieces)
    return pieces