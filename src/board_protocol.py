


from sys import int_info
from typing import Iterable, List, Protocol, Tuple

# Using a protocol for the color allows the implementation freedom for
# their internal representation of color instead of restricting it 
# to 1 and 0.
class ColorProtocol(Protocol):
    @property
    def color_index(self) -> int:
        """Returns 1 for white, 0 for black"""
        pass

class PieceProtocol(Protocol):
    @property
    def color(self) -> ColorProtocol:
        """Return an object conforming to the ColorProtocol"""
        pass
    
    @property
    def image_id(self) -> int:
        """Return [1,2,3,4,5,6] for [Pawn, Knight, Bishop, Rook, Queen, King] respectively, 
        positive integers for white, negative for black."""
        pass
    
    @property
    def location(self) -> int:
        """Returns a bitboard of the piece's location"""
        pass
    
    
    @property
    def piece_type(self) -> str:
        """Returns the piece type as a string"""
        
    @property
    def piece_type_id(self) -> int:
        """Returns the piece type as an int: [1,2,3,4,5,6] for [pawn, knight, bishop, rook, queen, king] respectively
        If it's a black piece, return the negative integer instead."""

    
    
class BoardProtocol(Protocol):
    
    @property
    def black_occupied_squares(self) -> int:
        pass
    
    @property
    def enpassant_capture_square(self) -> int:
        pass
    
    @property
    def enpassant_end_square(self) -> int:
        pass
    
    @property
    def game_is_over(self) -> bool:
        pass
    
    @property
    def history(self) -> Iterable:
        """Dict with printable move information.
        """
    
    @property
    def last_move(self) -> Tuple[int,int]|None:
        """Returns bitboards with the start and end of the last move"""
        pass
    
    @property
    def last_move_was_capture(self) -> bool:
        pass
    
    @property
    def pieces(self) -> Iterable[PieceProtocol]:
        pass
    
    @property
    def turn(self) -> ColorProtocol:
        pass
    
    @property
    def white_occupied_squares(self) -> int:
        pass
    
    @property
    def winner(self) -> ColorProtocol:
        pass
    
    def from_json(data) -> "BoardProtocol":
        pass    
    
    def get_color(self,color: int) -> int:
        """Takes 1 (for white) or 0 (for black) as input, returns a bitboard
        where active bits depict piece location"""
    
    def get_legal_moves(self,arg:int|PieceProtocol) -> int:
        """Takes a bitboard with the square location, or a piece,
        returns a bitboard with all legal moves from that square.
        If no legal moves are available, returns an empty bitboard (0)"""
        
    def get_piece(self,square:int) -> PieceProtocol | None:
        """Expects a bitboard with a square location, 
        returns an object conforming to the PieceProtocol located in square, 
        or None if square is empty."""
        
    def get_psuedo_legal_moves(self, piece:PieceProtocol):
        """Returns psuedo legal moves (psuedo-legal means that moves which leaves king in check is included)"""
    
    def king_is_in_check(self, color: ColorProtocol) -> bool:
        pass
    
    def play_turn(self,color: ColorProtocol, start_square:int, end_square:int, piece: PieceProtocol):
        """Plays the turn, ends with checks for game ending positions (stalemate, checkmate, draw) as well as changing the turn"""
    
    def make_move(self, start_square:int, end_square:int, piece: PieceProtocol): 
        """Makes a move"""
    
    def unmake_move(self):
        """Unmakes the most recent move"""
    
    def reset(self) -> None:
        """Resets the game"""
        
    def set_promotion_piece(self, piece_id:int):
        """Sets the promotion piece, expects 2 (knight), 3 (bishop), 4 (rook), 5 (queen)."""
    
    def to_json(self) -> dict:
        pass
    
    def unplay_turn(self) -> None:
        "Unmakes the last turn played" 
    
    
    
    
    
    
    
    
    
    
    
    
    
    