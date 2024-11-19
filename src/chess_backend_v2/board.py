
from abc import ABC, abstractmethod
from typing import Iterable, Set, Tuple

from src.game.piece_image_id_enum import PieceImageIdEnum
from src.chess_backend_v2.move import Move
from src.chess_backend_v2.piece import Piece


class ChessBoard(ABC):
    
    # @abstractmethod
    # def get_legal_moves(lazy:bool) -> Set[Move]:
    #     pass
    
    @abstractmethod
    def make_move(self,move:Move):
        pass
    
    @abstractmethod
    def unmake_move(self):
        pass
    
    # For drawing
    @abstractmethod
    def get_piece_image_id(self,rank:int, file:int) -> PieceImageIdEnum | None:
        pass
    
    @abstractmethod
    def get_legal_moves_for_drawing(self, rank, file) -> None | list[Tuple[int,int]]:
        pass
    
    @abstractmethod
    def get_pieces() -> Iterable[Piece]:
        pass    