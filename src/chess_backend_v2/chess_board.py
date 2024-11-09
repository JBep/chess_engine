
from tracemalloc import start
from typing import List, Set

from chess_backend_v2 import move
from chess_backend_v2.bitboard_constants import KING_STARTING_POSITIONS, KINGSIDE_CASTLING, QUEENSIDE_CASTLING
from chess_backend_v2.bitboard_utils import activate_position
from chess_backend_v2.board import ChessBoard
from chess_backend_v2.get_moves import get_psuedo_legal_moves
from chess_backend_v2.move import Move
from constants import WHITE
from src.chess_backend_v2.piece import ColorEnum, Piece, PieceTypeEnum, initialize_pieces


class ChessBoard_V2(ChessBoard):
    
    def __init__(self, pieces: dict[int,Piece]):
        if pieces == None:
            self.white_bitboard = 65535 # Bits in position 0-15 are active. 
            self.black_bitboard = 18446462598732840960 # Bits in position 48-63 are active.
            self.pieces: dict[int, Piece] = initialize_pieces()
            
            self.turn = 0 # 0 is white, 1 is black
            self.enpassant_bitboard = 0 # Holds the position for enpassant
            
            self.psuedo_legal_moves = {}
            for piece in pieces.values():
                self.psuedo_legal_moves[piece] = get_psuedo_legal_moves(
                    piece, 
                    self.white_bitboard, 
                    self.black_bitboard, 
                    self.enpassant_bitboard
                )
                
    def make_move(self,move:move):
        # Get the piece
        piece = self.pieces.pop(move.start_bitboard)
        
        if piece.color == ColorEnum.WHITE:
            own_color_bitboard = self.white_bitboard
            opposing_color_bitboard = self.black_bitboard
        else:
            own_color_bitboard = self.black_bitboard
            opposing_color_bitboard = self.white_bitboard
            
        # check if there's a piece on the intended target square and if so, remove it
        if move.end_bitboard & opposing_color_bitboard != 0:
            captured_piece = self.pieces.pop(move.end_bitboard)
            opposing_color_bitboard = opposing_color_bitboard ^ move.end_bitboard
        
        # Move the piece
        piece.placement_bitboard = move.end_bitboard
        piece.has_moved = True
        self.pieces[move.end_bitboard]
        
        # Update color bitboards
        own_color_bitboard = own_color_bitboard & ~move.start_bitboard | move.end_bitboard
        
        if piece.color == ColorEnum.WHITE:
            self.white_bitboard = own_color_bitboard
            self.black_bitboard = opposing_color_bitboard
        else:
            self.white_bitboard = opposing_color_bitboard
            self.black_bitboard = own_color_bitboard
        
        # Check if it was a move generating enpassant
        if piece.type != PieceTypeEnum.PAWN:
            self.enpassant_bitboard = 0
        else:
            if piece.color == ColorEnum.WHITE:
                if move.start_bitboard << 16 == move.end_bitboard:
                    self.enpassant_bitboard = move.start_bitboard << 8
                else:
                    self.enpassant_bitboard
            else:
                if move.start_bitboard >> 16 == move.end_bitboard:
                    self.enpassant_bitboard = move.start_bitboard >> 8
                else:
                    self.enpassant_bitboard
                    
        # Check if is was a castling move
        if (move.start_bitboard & KING_STARTING_POSITIONS) != 0:
            if (move.end_bitboard & KINGSIDE_CASTLING) != 0:
                if piece.color == ColorEnum.WHITE:
                    rook = self.pieces.pop(move.end_bitboard>>1)
                    rook.placement_bitboard = move.end_bitboard<<1
                    self.pieces[move.end_bitboard<<1] = rook
                else:
                    rook = self.pieces.pop(move.end_bitboard>>1)
                    rook.placement_bitboard = move.end_bitboard>>1
                    self.pieces[move.end_bitboard<<1] = rook
                    
            elif (move.end_bitboard & QUEENSIDE_CASTLING) != 0:    
                if piece.color == ColorEnum.WHITE:
                    rook = self.pieces.pop(move.end_bitboard<<2)
                    rook.placement_bitboard = move.end_bitboard>>1
                    self.pieces[move.end_bitboard<<1] = rook
                else:
                    rook = self.pieces.pop(move.end_bitboard>>2)
                    rook.placement_bitboard = move.end_bitboard<<1
                    self.pieces[move.end_bitboard<<1] = rook
            
            rook.has_moved = True
            
        # TODO check if it's check
        self.turn = -1*self.turn + 1 # cycles between 0 and 1
    
    def unmake_move():
        pass
            
    def get_piece(self,rank:int, file:int):
        bit_position = rank*8+file
        bitboard = activate_position(0,bit_position)
        return self.pieces.get(bitboard, None)
            