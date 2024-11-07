
import logging

from src.log import log_execution_time
from src.constants import BOARD_START_IDX, COL_RANGE, ROW_RANGE
from src.legal_moves import legal_moves_bishop, legal_moves_king, legal_moves_knight, legal_moves_pawn, legal_moves_queen, legal_moves_rook
from src.move import Move, MoveRecord, MoveTypeEnum
from src.check import count_attackers, get_king_pos, king_in_check

class ChessBoard:
    def __init__(self, grid = None):
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
        
        self.turn = 1
        
        # Check
        self.king_attackers = [0,0,0] # index 1 is white, 2 is black (as -1 gets the 2nd index)

        # End of game
        self.game_is_over = False
        self.winner = None
        
        # Holds possible positions for enpassant for the one turn when they're available.
        self.enpassant_position = [None,None,None] # index 1 is white, 2 is black
        
        # If castling no longer possible, set to false (king or rook moves).
        self.kingside_castling_possible = [None, True, True]
        self.queenside_castling_possible = [None, True, True]
        
        # Tracking move history
        self.history = []
        
        # Initialize legal moves
        self.update_legal_moves()
        

    @log_execution_time
    def update_legal_moves(self):
        # While all moves for the player who's not in turn are illegal per se, the set of legal moves is also used for board evaluation (e.g. seeing how many squares are attacked.) thus we iterate through both colors.
        moves = {1: set(), -1: set()}
        for row in ROW_RANGE:
            for col in COL_RANGE:
                piece = self.grid[row][col]
                if piece != 0:
                    color = piece//abs(piece)
                    moves[color] = moves[color].union(self._get_legal_moves((row,col), piece, color))
        
        self.legal_moves = {1: set(), -1: set()}
        for color in [1,-1]:
            for move in moves[color]:
                self.move_piece(move, override_rules = True, update_legal_moves= False)
                if not king_in_check(self.grid, color):
                    self.legal_moves[color].add(move)
                self.undo_move(update_legal_moves = False) 
    
    def _get_legal_moves(self, start_square, piece:int, color:int):  
        piece_type = abs(piece)
        if piece_type == 1:
            enpassant_square = self.enpassant_position[color]
            legal_moves =  legal_moves_pawn(self.grid, color, start_square, enpassant_square)
            
        elif piece_type == 2:
            legal_moves = legal_moves_knight(self.grid, color, start_square)
            
        elif piece_type == 3:
            legal_moves = legal_moves_bishop(self.grid, color, start_square)
            
        elif piece_type == 4:
            legal_moves = legal_moves_rook(self.grid, color, start_square)
            
        elif piece_type == 5:
            legal_moves = legal_moves_queen(self.grid, color, start_square)
            
        elif piece_type == 6:
            kingside_castling_possible = self.kingside_castling_possible[color]
            queenside_castling_possible = self.queenside_castling_possible[color]
            legal_moves = legal_moves_king(self.grid, color, start_square, kingside_castling_possible, queenside_castling_possible)
    
        return legal_moves
    
    def undo_move(self, update_legal_moves: bool = True):
        if self.history:
            move_record:MoveRecord = self.history[-1]
            
            # Return the piece
            start_row, start_col, end_row, end_col = move_record.move.unpack()
            self.grid[end_row][end_col] = move_record.captured_piece
            self.grid[start_row][start_col] = move_record.move.piece
            
            # TODO handle enpassant and castling special moves (place back rook and captured pawn)
            if move_record.move.move_type == MoveTypeEnum.ENPASSANT:
                self._handle_enpassant(move_record.move, undo = True)

            if move_record.move.move_type in [MoveTypeEnum.KINGSIDE_CASTLING, MoveTypeEnum.QUEENSIDE_CASTLING]:
                self._handle_castling(move_record.move, undo = True)
                
            # Reset game state
            self.kingside_castling_possible = move_record.kingside_castling_possible_before_move
            self.queenside_castling_possible = move_record.kingside_castling_possible_before_move
            self.enpassant_position = move_record.enpassant_position_before_move
            
            self.turn = self.turn * -1
            if update_legal_moves:
                self.update_legal_moves()
                self._update_game_is_over()
            self._update_check()
            self.history.pop()
        
    @log_execution_time
    def move_piece(self, move: Move, override_rules: bool = False, update_legal_moves: bool = True):
        """Let's a player or a bot interact with the game by moving a piece"""
        logging.log(level = logging.DEBUG, msg = str(move.to_json()))
        if override_rules:
            pass
        else:
            if not move in self.legal_moves[self.turn]:
                raise ValueError(f"Not a valid move. {move}")
        
        # Used for record, and undo
        kingside_castling_possible = self.kingside_castling_possible[:]
        queenside_castling_possible = self.queenside_castling_possible[:]
        enpassant_position = self.enpassant_position
        
        start_row, start_col, end_row, end_col = move.unpack()
        
        # Move the piece
        captured_piece = self.grid[end_row][end_col] # Saves the captured piece for record (if any)
        self.grid[start_row][start_col] = 0
        self.grid[end_row][end_col] = move.piece
        
        if move.move_type == MoveTypeEnum.ENPASSANT:
            self._handle_enpassant(move)
            
        if move.move_type == MoveTypeEnum.PAWN_DOUBLE_STEP:
            self.enpassant_position = (start_row-self.turn,start_col)
        else:
            self.enpassant_position = [None, None, None]

        if move.move_type in [MoveTypeEnum.KINGSIDE_CASTLING, MoveTypeEnum.QUEENSIDE_CASTLING]:
            self._handle_castling(move)
        
        self._update_castling_availability(move)

        if move.move_type == MoveTypeEnum.PAWN_PROMOTION:
            self._promote_pawn(move)            
        
        self._update_check()
        if update_legal_moves:
            self.update_legal_moves()
            self._update_game_is_over()
            
        
        self._record_move(move, captured_piece, kingside_castling_possible, queenside_castling_possible, enpassant_position)
        self.turn = self.turn * -1
            
    def _promote_pawn(self,move: Move):
        end_row, end_col = move.end_square
        if move.piece == 1*self.turn and end_row in [0,7]:
            if move.pawn_promotion_piece is None:
                raise ValueError("You need to supply a pawn promotion piece.") 
            self.grid[end_row][end_col] = move.pawn_promotion_piece
    
    def _record_move(self, move: Move, captured_piece: int, kingside_castling_possible, queenside_castling_possible, enpassant_position):
        color = move.piece//abs(move.piece)
        check = self.king_attackers[color] > 0
        if self.game_is_over and self.winner != 0:
            checkmate = True
        else:
            checkmate = False
        
        record = MoveRecord(
            move = move,
            captured_piece = captured_piece,
            check = check,
            checkmate = checkmate,
            kingside_castling_possible_before_move = kingside_castling_possible,
            queenside_castling_possible_before_move = queenside_castling_possible,
            enpassant_position_before_move = enpassant_position
        )
        self.history.append(record)

    def _handle_enpassant(self, move: Move, undo: bool = False) -> None:
        end_row, end_col = move.end_square
        if not undo:
            self.grid[end_row+move.piece][end_col] = 0 # Selected pawn will add +1 or -1 to the row
        else:
            self.grid[end_row+move.piece][end_col] = move.piece*-1
 
    
    def _handle_castling(self, move: Move, undo: bool = False) -> None:
        start_row, _ = move.start_square
        if move.move_type == MoveTypeEnum.KINGSIDE_CASTLING:
            rook_start_col = BOARD_START_IDX + 7
            rook_end_col = BOARD_START_IDX + 5
        else:
            rook_start_col = BOARD_START_IDX
            rook_end_col = BOARD_START_IDX + 3
        
        color = move.piece//abs(move.piece)
        if not undo:
            self.grid[start_row][rook_start_col] = 0
            self.grid[start_row][rook_end_col] = 4*color
        else:
            self.grid[start_row][rook_start_col] = 4*color
            self.grid[start_row][rook_end_col] = 0
    
    def _update_castling_availability(self, move: Move):
        ## Remove castling ability
        color = move.piece//abs(move.piece)
        if abs(move.piece) == 6:
            self.kingside_castling_possible[color] = False
            self.queenside_castling_possible[color] = False
        elif abs(move.piece) == 4:
            if self.queenside_castling_possible[color] and move.end_square[1] == BOARD_START_IDX:
                self.queenside_castling_possible[color] = False
            elif self.kingside_castling_possible and move.end_square[1] == BOARD_START_IDX+7:
                self.kingside_castling_possible[color] = False
            
    def _update_check(self) -> None:
        # Checks if king's are in check
        for color in [1,-1]:
            self.king_attackers[color] = count_attackers(self.grid, get_king_pos(self.grid, color), color*-1) 
        
    def _update_game_is_over(self) -> bool:
        for color in [1,-1]: 
            if len(self.legal_moves[color]) == 0:
                if self.king_attackers[color] > 0:
                    self.winner = color*-1
                    self.game_is_over = True
                elif color == self.turn*-1:
                    self.game_is_over = True # Stalemate
    
    def to_json(self):
        data = {
            'grid': self.grid,
            'turn': self.turn,
            'king_attackers': self.king_attackers,
            'game_is_over':self.game_is_over,
            'winner': self.winner,
            'enpassant_position': self.enpassant_position,
            'kingside_castling_possible': self.kingside_castling_possible,
            'queenside_castling_possible': self.queenside_castling_possible,
            'history' : [move_record.to_json() for move_record in self.history]
        }
        return data
        
    @staticmethod
    def from_json(data) -> "ChessBoard":
        board = ChessBoard()
        board.grid = data['grid']
        board.turn = data['turn']
        
        board.king_attackers = data['king_attackers']
        board.game_is_over = data['game_is_over']
        board.winner = data['winner']
        
        board.enpassant_position = data['enpassant_position']
        board.kingside_castling_possible = data['kingside_castling_possible']
        board.queenside_castling_possible = data['queenside_castling_possible']

        board.update_legal_moves()

        board.history = []
        for move_record in data['history']:
            board.history.append(MoveRecord.from_json(move_record))
        return board
    

            
        