
import logging
from tracemalloc import start
from typing import Iterable, List, Set, Tuple

from src.chess_backend_v2 import piece
from src.chess_backend_v2.bitboard_constants import RANK_1_BITBOARD, RANK_8_BITBOARD, WHITE_SQUARES
from src.log import log_execution_time
from src.chess_backend_v2.checking_logic import king_is_in_check
from src.chess_backend_v2.move_logic import compute_enpassant_position, compute_rook_move_if_castling, get_psuedo_legal_moves
from src.chess_backend_v2.move import Move, MoveRecord, MoveTypeEnum
from src.chess_backend_v2.piece import ColorEnum, Piece, PieceTypeEnum, initialize_pieces


class ChessBoard_V2:
    
    def __init__(self, pieces: dict[int,Piece] = None):
        if pieces is None:
            self.pieces: List[Piece] = initialize_pieces()
            self.turn = ColorEnum.WHITE # 0 is white, 1 is black
            
            self.black_occupied_squares = 18446462598732840960 # Bits in position 48-63 are active.
            self.white_occupied_squares = 65535 # Bits in position 0-15 are active. 
            
            self.enpassant_capture_square = 0 # Holds the position for enpassant
            self.enpassant_end_square = 0 # Holds the position for enpassant
            
            self.game_is_over = False
            self.history: List[MoveRecord] = []
            self.winner = None
            
            self.promotion_piece = PieceTypeEnum.QUEEN # Default to promote to queen.
    
    @property
    def dead_position(self) -> bool:
        if len(self.pieces) > 4:
            return False
        if len(self.pieces) == 2: # Only two kings
            return True 
        
        elif len(self.pieces) == 3: # Kings + bishop or knight
            types = [piece.type for piece in self.pieces]
            not_king = None
            for type in types:
                if type != PieceTypeEnum.KING:
                    not_king = type
            if not_king in [PieceTypeEnum.KNIGHT, PieceTypeEnum.BISHOP]:
                return True 
        
        elif len(self.pieces) == 4: # Two kings and same color bishop
            types = {piece.type:piece for piece in self.pieces}
            other_types = {}
            for type, piece in types.items():
                if type != PieceTypeEnum.KING:
                    other_types[type] =piece
            
            for type in other_types.keys():
                if type != PieceTypeEnum.BISHOP:
                    return False
            
            square_color_1 = None
            square_color_2 = None
            for piece in other_types:
                if piece.location & WHITE_SQUARES:
                    square_color_1 = ColorEnum.WHITE
                else:
                    square_color_1 = ColorEnum.BLACK
            
            if square_color_1 == square_color_2:
                return True
            
        return False
                
    
    @property
    def last_move(self) -> Tuple[int, int] | None:
        if self.history:
            lm = self.history[-1]
            return lm.start_bitboard, lm.end_bitboard
        else:
            return None
        
    @property
    def last_move_was_capture(self) -> Tuple[int, int] | None:
        if self.history:
            lm = self.history[-1]
            if lm.move_type == MoveTypeEnum.CAPTURE:
                return True
        return False
    
    @property
    def fifty_move_draw_count(self) -> int:
        counter = 0
        for move in self.history[::-1]:
            if move.moved_piece_type == PieceTypeEnum.PAWN or move.move_type == MoveTypeEnum.CAPTURE or move.move_type == MoveTypeEnum.PROMOTION_CAPTURE:
                return counter
            else:
                counter += 1
        return counter
    
    def set_promotion_piece(self,piece_type_id:int):
        if piece_type_id == 2:
            self.promotion_piece == PieceTypeEnum.KNIGHT
        elif piece_type_id == 3: 
            self.promotion_piece == PieceTypeEnum.BISHOP
        elif piece_type_id == 4: 
            self.promotion_piece == PieceTypeEnum.KINGSIDE_ROOK
        elif piece_type_id == 5:
            self.promotion_piece == PieceTypeEnum.QUEEN
        else:
            raise ValueError(f"{piece_type_id} is not a valid piece type id. Valid id's are 2 (knight), 3 (bishop), 4 (rook), 5 (queen).")
    
    def get_legal_moves(self,arg):
        if isinstance(arg, int):
            return self._get_legal_moves_square(arg)
        elif isinstance(arg, Piece):
            return self._get_legal_moves_piece(arg)
        else:
            raise TypeError(f"Argument should be int or Piece, not {type(arg)}.")
    
    def _get_legal_moves_square(self, square:int) -> int:
        for piece in self.pieces:
            if piece.location & square:
                self.update_legal_moves(piece)
                return piece.legal_moves
        
    def get_piece(self, square:int) -> Piece | None:
        for piece in self.pieces:
            if piece.location == square:
                return piece
        return None
        
    def _get_legal_moves_piece(self,piece: Piece):
        if piece.legal_moves == 0:
            self.update_legal_moves(piece)
        return piece.legal_moves
    
    def king_is_in_check(self, color: ColorEnum) -> bool:
        if king_is_in_check(self.pieces, color):
            return True
        else:
            return False
     
    def play_turn(self, color: ColorEnum, start_square:int, end_square:int, piece: Piece) -> bool:
        # Check game is over
        if self.game_is_over == True:
            print("Game is over, you cannot make any more moves!")
            return False
        
        # Check turn
        if color != self.turn:
            print("Not your turn.")
            return False
        
        self.update_legal_moves(piece)
        
        if end_square & piece.legal_moves == 0:
            "Illegal move"
            return False
        
        self.make_move(start_square, end_square, piece)
        
        # # Checkmate & stalemate
        # if self._is_checkmate(color.opposite_color()):
        #     print("Checkmate")
        #     self.game_is_over = True
        #     self.winner = color
        
        # elif self._is_stalemate(color.opposite_color()):
        #     print("Stalemate")
        #     self.game_is_over = True
        
        # # Draw by 50
        # elif self.fifty_move_draw_count >= 50:
        #     self.game_is_over = True
        
        # # Dead position
        # elif self.dead_position:
        #     self.game_is_over = True
        
        # TODO Three-fold repetition
        
        piece.legal_moves = 0
        self.turn = self.turn.opposite_color()
        return True
        
    def unplay_turn(self):
        if self.history:
            self.unmake_move()
            self.game_is_over = False
            self.winner = None
            self.turn = self.turn.opposite_color()
            
    def make_move(self,start_square: int, end_square:int, piece :Piece) -> bool:
        move_record = MoveRecord(
            start_bitboard= start_square,
            end_bitboard=end_square,
            move_type = MoveTypeEnum.NORMAL,
            moved_piece_type= piece.type,
            enpassant_bitboard=self.enpassant_end_square,
            enpassant_capture_bitboard=self.enpassant_capture_square
        )
        
        own_color_bitboard, opposing_color_bitboard = self._get_color_bitboards(piece.color)
        
        # check if there's a piece on the intended target square and if so, remove it
        if end_square & opposing_color_bitboard != 0:
            move_record.captured_piece = self.get_piece(end_square)
            self.pieces.remove(move_record.captured_piece)
            opposing_color_bitboard ^= end_square
            move_record.move_type = MoveTypeEnum.CAPTURE
        
        # Move the piece
        piece.location = end_square
        piece.move_counter += 1
        
        # Update color bitboards
        own_color_bitboard |= end_square
        own_color_bitboard ^= start_square
        
        # Handle enpassant
        if piece.type == PieceTypeEnum.PAWN and end_square & self.enpassant_end_square != 0:
            move_record.move_type = MoveTypeEnum.ENPASSANT
            logging.log(logging.DEBUG, f"Trying to pop at {self.enpassant_capture_square}")
            move_record.captured_piece = self.pieces.pop(self._get_piece_index(self.enpassant_capture_square))
            opposing_color_bitboard ^= self.enpassant_capture_square

        self.enpassant_end_square, self.enpassant_capture_square = compute_enpassant_position(
            start_bitboard = start_square,
            end_bitboard = end_square,
            piece_type = piece.type,
            color = piece.color
        )
        
        # Handle castling
        rook_move = compute_rook_move_if_castling(
            start_bitboard=start_square, 
            end_bitboard=end_square, 
            piece_type=piece.type, 
            color=piece.color)
        
        if rook_move is not None:
            rook_start_bitboard, rook_end_bitboard = rook_move
            move_record.move_type = MoveTypeEnum.CASTLING
            move_record.rook_start_bitboard = rook_start_bitboard
            move_record.rook_end_bitboard = rook_end_bitboard
            
            rook = self.pieces.pop(self._get_piece_index(rook_start_bitboard))        
            rook.location = rook_end_bitboard
            self.pieces[rook_end_bitboard] = rook    
            rook.move_counter += 1
            
            own_color_bitboard ^= rook_start_bitboard
            own_color_bitboard |= rook_end_bitboard
        
        # Handle pawn promotion
        if piece.type == PieceTypeEnum.PAWN:
            if end_square & (RANK_1_BITBOARD | RANK_8_BITBOARD):
                piece.type = self.promotion_piece
                if move_record.move_type == MoveTypeEnum.CAPTURE:
                    move_record.move_type = MoveTypeEnum.PROMOTION_CAPTURE
                else:
                    move_record.move_type = MoveTypeEnum.PROMOTION

        
        self._update_color_bitboards(color = piece.color, own_color_bitboard=own_color_bitboard, opposing_color_bitboard=opposing_color_bitboard)
        
        # record the move
        self.history.append(move_record)
        logging.log(logging.DEBUG, f"Last move: {move_record}")
        
    def unmake_move(self):
        # Get the move_record
        move_record = self.history.pop()
        
        piece = self.get_piece(move_record.end_bitboard) 
        own_color_bitboard, opposing_color_bitboard = self._get_color_bitboards(piece.color)
        
        # Move back the piece
        piece.location = move_record.start_bitboard
        piece.move_counter  -= 1
        
        # Reset enpassant boards
        self.enpassant_end_square = move_record.enpassant_bitboard
        self.enpassant_capture_square = move_record.enpassant_capture_bitboard
        
        # Update color bitboards
        own_color_bitboard = own_color_bitboard & ~move_record.end_bitboard | move_record.start_bitboard
        
        if move_record.move_type == MoveTypeEnum.CAPTURE:
            self.pieces.append(move_record.captured_piece)
            opposing_color_bitboard = opposing_color_bitboard | move_record.end_bitboard
        
        elif move_record.move_type == MoveTypeEnum.ENPASSANT:
            self.pieces.append(move_record.captured_piece)
            opposing_color_bitboard = opposing_color_bitboard | move_record.enpassant_capture_bitboard
        
        elif move_record.move_type == MoveTypeEnum.CASTLING:
            rook = self.pieces[self._get_piece_index(move_record.rook_end_bitboard)]
            rook.location = move_record.rook_start_bitboard
            rook.move_counter  -= 1
            own_color_bitboard &= ~(move_record.rook_end_bitboard)
            own_color_bitboard |= move_record.rook_start_bitboard
        
        elif move_record.move_type == MoveTypeEnum.PROMOTION:
            piece.type = PieceTypeEnum.PAWN    
        
        elif move_record.move_type == MoveTypeEnum.PROMOTION_CAPTURE:
            self.pieces.append(move_record.captured_piece)
            opposing_color_bitboard = opposing_color_bitboard | move_record.end_bitboard
            piece.type = PieceTypeEnum.PAWN    
            
        
        self._update_color_bitboards(color = piece.color, own_color_bitboard=own_color_bitboard, opposing_color_bitboard=opposing_color_bitboard)
     
    def reset(self) -> None:
        self.__init__()
     
    def get_psuedo_legal_moves(self, piece: Piece):
        self.update_psuedo_legal_moves(piece)
        return piece.psuedo_legal_moves
     
    @log_execution_time
    def update_psuedo_legal_moves(self, piece: Piece) -> None:
        piece.psuedo_legal_moves = get_psuedo_legal_moves(
            piece=piece, 
            pieces = self.pieces,
            white_bitboard=self.white_occupied_squares, 
            black_bitboard=self.black_occupied_squares, 
            enpassant_bitboard=self.enpassant_end_square
            )

    def update_legal_moves(self, piece: Piece) -> None:
        self.update_psuedo_legal_moves(piece)

        piece.legal_moves = 0
        psuedo_legal_bitboard= piece.psuedo_legal_moves
        while psuedo_legal_bitboard:
            lsb = psuedo_legal_bitboard & -psuedo_legal_bitboard  # Isolate the least significant bit (LSB)
            
            self.make_move(start_square= piece.location, end_square=lsb, piece = piece)
            if not king_is_in_check(self.pieces, piece.color):
                piece.legal_moves |= lsb
            self.unmake_move()
            
            psuedo_legal_bitboard &= psuedo_legal_bitboard-1  # Clear the least significant bit
    
    def  _get_color_bitboards(self, color: ColorEnum):
        if color == ColorEnum.WHITE:
            own_color_bitboard = self.white_occupied_squares
            opposing_color_bitboard = self.black_occupied_squares
        else:
            own_color_bitboard = self.black_occupied_squares
            opposing_color_bitboard = self.white_occupied_squares
        
        return own_color_bitboard, opposing_color_bitboard
    
    def _get_piece_index(self,square:int) -> int:
        for i,p in enumerate(self.pieces):
            if p.location == square:
                return i
        return None
    
    def _is_checkmate(self,color: ColorEnum):
        if not king_is_in_check(self.pieces,color):
            return False
        
        for piece in self.pieces:
            if piece.color == color:
                if self.get_legal_moves(piece):
                    return False
        return True
        
    def _is_stalemate(self,color: ColorEnum):
        if king_is_in_check(self.pieces,color):
            return False
        
        for piece in self.pieces:
            if piece.color == color:
                if self.get_legal_moves(piece):
                    return False
        return True
         
    def _update_color_bitboards(self, color: ColorEnum, own_color_bitboard:int, opposing_color_bitboard:int):
        if color == ColorEnum.WHITE:
            self.white_occupied_squares = own_color_bitboard
            self.black_occupied_squares = opposing_color_bitboard
        else:
            self.white_occupied_squares = opposing_color_bitboard
            self.black_occupied_squares = own_color_bitboard
        
    
    # def to_json(self):
        
    
    # @staticmethod
    # def from_json(self):
    #     pass