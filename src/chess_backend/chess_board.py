

import logging
from typing import List

from src.log import log_execution_time
from src.constants import BOARD_START_IDX, COL_RANGE, ROW_RANGE
from src.chess_backend.legal_moves import legal_moves_bishop, legal_moves_king, legal_moves_knight, legal_moves_pawn, legal_moves_queen, legal_moves_rook
from src.chess_backend.move import Move, MoveRecord, MoveTypeEnum
from src.chess_backend.chess_utils import count_attackers, get_king_pos, king_in_check
from src.chess_backend.game_state import GameState


class ChessBoard:
    def __init__(self, grid = None, update_legal_moves: bool = True):
        # Initialize grid, two padding rows of "99" for ability to access indexes outside of playable area
        if grid is None:
            self.grid = [
                [99]*12,
                [99]*12,
                [99, 99,-4, -2, -3, -5, -6, -3, -2, -4, 99,99],
                [99, 99,-1, -1, -1, -1, -1, -1, -1, -1, 99,99],
                [99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99],
                [99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99],
                [99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99],
                [99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99],
                [99, 99, 1, 1, 1, 1, 1, 1, 1, 1, 99, 99],
                [99, 99, 4, 2, 3, 5, 6, 3, 2, 4, 99, 99],
                [99]*12,
                [99]*12
            ]
        else:
            self.grid = grid
        
        # initialize game state
        self.game_state = self._init_game_state()
        # Tracking move history
        self.history: List[MoveRecord] = []
        
        # Initialize legal moves
        if update_legal_moves:
            self.update_legal_moves()
        
    def _init_game_state(self):
        gs = GameState(
            turn = 1,
            game_is_over= False,
            winner=0,
            king_in_check=[False,False,False],
            enpassant_end_square=[None,None,None],
            kingside_castling_possible=[True,True,True],
            queenside_castling_possible=[True,True,True],
        )
        return gs

    @log_execution_time
    def update_legal_moves(self):
        # While all moves for the player who's not in turn are illegal per se, the set of legal moves is also used for board evaluation (e.g. seeing how many squares are attacked.) thus we iterate through both colors.
        moves = set()
        for row in ROW_RANGE:
            for col in COL_RANGE:
                piece = self.grid[row][col]
                if piece*self.game_state.turn > 0:
                    color = piece//abs(piece)
                    moves = moves.union(self._get_legal_moves((row,col), piece, color))
        
        self.legal_moves = set()
        for move in moves:
            self.move_piece(move, override_rules = True, update_legal_moves= False)
            if not self.game_state.king_in_check[self.game_state.turn*-1]:
                self.legal_moves.add(move)
            self.undo_move(update_legal_moves = False) 
    
    def _get_legal_moves(self, start_square, piece:int, color:int):  
        piece_type = abs(piece)
        if piece_type == 1:
            enpassant_end_square = self.game_state.enpassant_end_square[color]
            legal_moves =  legal_moves_pawn(self.grid, color, start_square, enpassant_end_square)
            
        elif piece_type == 2:
            legal_moves = legal_moves_knight(self.grid, color, start_square)
            
        elif piece_type == 3:
            legal_moves = legal_moves_bishop(self.grid, color, start_square)
            
        elif piece_type == 4:
            legal_moves = legal_moves_rook(self.grid, color, start_square)
            
        elif piece_type == 5:
            legal_moves = legal_moves_queen(self.grid, color, start_square)
            
        elif piece_type == 6:
            legal_moves = legal_moves_king(self.grid, color, start_square, 
                                           self.game_state.kingside_castling_possible[color], 
                                           self.game_state.queenside_castling_possible[color])
    
        return legal_moves
        
    def undo_move(self, update_legal_moves: bool = True):
        if self.history:
            move_record:MoveRecord = self.history[-1]
            
            # Return the piece
            start_row, start_col, end_row, end_col = move_record.move.unpack()
            self.grid[end_row][end_col] = 0
            self.grid[start_row][start_col] = move_record.move.piece
            
            # TODO handle enpassant and castling special moves (place back rook and captured pawn)
            if move_record.move.move_type == MoveTypeEnum.CAPTURE:
                self.grid[end_row][end_col] = move_record.move.captured_piece
            
            if move_record.move.move_type == MoveTypeEnum.ENPASSANT:
                self._handle_enpassant(move_record.move, undo = True)

            if move_record.move.move_type in [MoveTypeEnum.KINGSIDE_CASTLING, MoveTypeEnum.QUEENSIDE_CASTLING]:
                self._handle_castling(move_record.move, undo = True)
                
            # Reset game state
            if len(self.history)>1:     
                self.game_state = self.history[-2].game_state.copy()
            else:
                self.game_state = self._init_game_state()
                
            self.history.pop()
            if update_legal_moves:
                self.update_legal_moves()
                
        
    @log_execution_time
    def move_piece(self, move: Move, override_rules: bool = False, update_legal_moves: bool = True):
        """Let's a player or a bot interact with the game by moving a piece"""
        logging.log(level = logging.DEBUG, msg = str(move.to_json()))
        if override_rules:
            pass
        else:
            if not move in self.legal_moves:
                raise ValueError(f"Not a valid move. {move}")
        
        # Move the piece
        start_row, start_col, end_row, end_col = move.unpack()
        self.grid[start_row][start_col] = 0
        self.grid[end_row][end_col] = move.piece
        
        if move.move_type == MoveTypeEnum.ENPASSANT:
            self._handle_enpassant(move)
            
        if move.move_type == MoveTypeEnum.PAWN_DOUBLE_STEP:
            self.game_state.enpassant_end_square[self.game_state.turn*-1] = (start_row-self.game_state.turn,start_col)
        else:
            self.game_state.enpassant_end_square = [None, None, None]

        if move.move_type in [MoveTypeEnum.KINGSIDE_CASTLING, MoveTypeEnum.QUEENSIDE_CASTLING]:
            self._handle_castling(move)
        
        self._update_castling_availability(move)

        if move.move_type == MoveTypeEnum.PAWN_PROMOTION:
            self._promote_pawn(move)            
        
        self._update_check()
        
        self.game_state.turn = self.game_state.turn * -1
        self._record_move(move)
        
        if update_legal_moves:
            self.update_legal_moves()
            self._update_game_is_over()
            
            if self.game_state.game_is_over:
                self.history[-1].game_state.game_is_over = True # add the game is over flag to the history-recorded (copied) game state.
        
            
    def _promote_pawn(self,move: Move):
        end_row, end_col = move.end_square
        if move.piece == self.game_state.turn and end_row in [BOARD_START_IDX,BOARD_START_IDX+7]:
            if move.pawn_promotion_piece is None:
                raise ValueError("You need to supply a pawn promotion piece.") 
            self.grid[end_row][end_col] = move.pawn_promotion_piece
    
    def _record_move(self, move: Move):
        record = MoveRecord(
            move = move,
            game_state = self.game_state.copy()
        )
        self.history.append(record)

    def _handle_enpassant(self, move: Move, undo: bool = False) -> None:
        enpassant_capture_row, enpassant_capture_col = move.enpassant_capture_square
        if not undo:
            self.grid[enpassant_capture_row][enpassant_capture_col] = 0 
        else:
            self.grid[enpassant_capture_row][enpassant_capture_col] = move.piece*-1 # Replace the pawn
    
    def _handle_castling(self, move: Move, undo: bool = False) -> None:
        rook_start_row, rook_start_col = move.rook_start_square
        rook_end_row, rook_end_col = move.rook_end_square
        color = move.piece/abs(move.piece)
        
        if not undo:
            self.grid[rook_start_row][rook_start_col] = 0
            self.grid[rook_end_row][rook_end_col] = color*4
        else:
            self.grid[rook_start_row][rook_start_col] = color*4
            self.grid[rook_end_row][rook_end_col] = 0
    
    def _update_castling_availability(self, move: Move):
        ## Remove castling ability
        color = move.piece//abs(move.piece)
        if abs(move.piece) == 6:
            self.game_state.kingside_castling_possible[color] = False
            self.game_state.queenside_castling_possible[color] = False
        elif abs(move.piece) == 4:
            if self.game_state.queenside_castling_possible[color] and move.start_square[1] == BOARD_START_IDX:
                self.game_state.queenside_castling_possible[color] = False
            elif self.game_state.kingside_castling_possible and move.start_square[1] == BOARD_START_IDX+7:
                self.game_state.kingside_castling_possible[color] = False
            
    def _update_check(self) -> None:
        # Checks if king's are in check
        for color in [1,-1]:
            self.game_state.king_in_check[color] = count_attackers(self.grid, get_king_pos(self.grid, color), color*-1) > 0
        
    def _update_game_is_over(self) -> bool:
        for color in [1,-1]: 
            if len(self.legal_moves) == 0:
                if self.game_state.king_in_check[color]:
                    self.winner = color*-1
                    self.game_is_over = True
                elif color == self.game_state.turn*-1:
                    self.game_is_over = True # Stalemate
    
    def to_json(self):
        data = {
            'grid': self.grid,
            'game_state': self.game_state,
            'history' : [move_record.to_json() for move_record in self.history]
        }
        return data
        
    @staticmethod
    def from_json(data) -> "ChessBoard":
        board = ChessBoard()
        board.grid = data['grid']
        board.game_state = GameState.from_json(data['game_state'])

        board.history = []
        for move_record in data['history']:
            board.history.append(MoveRecord.from_json(move_record))

        board.update_legal_moves()

        return board
    

            
        