from src.chess_backend_v2.bitboard_utils import get_active_positions, index_to_chess_notation

def test_bitboard_utils():
    test_get_active_positions()
    test_index_to_chess_notation()

def test_get_active_positions():
    bitboard = 0
    assert get_active_positions(bitboard) == []
    
    bitboard = 1
    assert get_active_positions(bitboard) == [0]
    
    bitboard = 4 # 100
    assert get_active_positions(bitboard) == [2]
    
def test_index_to_chess_notation():
    assert index_to_chess_notation(2) == 'c1'
    assert index_to_chess_notation(3) == 'd1'
    assert index_to_chess_notation(7) == 'h1'
    assert index_to_chess_notation(15) == 'h2'
    assert index_to_chess_notation(28) == 'e4'
    assert index_to_chess_notation(63) == 'h8'