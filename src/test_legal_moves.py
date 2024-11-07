from legal_moves import legal_moves_bishop


def test_bishop_moves():
    grid = [
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
    
    return legal_moves_bishop(grid, -1, (2,5))