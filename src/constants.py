# Chess constants
BOARD_START_IDX = 2
ROW_RANGE = range(BOARD_START_IDX, BOARD_START_IDX+8)
COL_RANGE = range(BOARD_START_IDX, BOARD_START_IDX+8)

# File constants
IMAGE_DIR = "images"

# Bot constants
BOT_COLOR = -1
BOT_EVALUATION_DEPTH = 3
VISUALIZE = False

# Game text constants this
GAME_TITLE = "Chess Game"

WHITE = (255,255,255)
OFF_WHITE = (251, 245, 222)       # Off-white, warm tone
BLUE = (0, 68, 116)            # Dark blue
BLACK = (34, 32, 52)           # Dark gray-black, not too harsh
GRAY = (128, 128, 128)         # Medium gray, neutral
RED = (179, 57, 57)            # Warm, muted red
GREEN = (34, 139, 34)          # Forest green, natural tone
YELLOW = (252, 196, 25)         # Golden yellow, slightly warm
BRIGHT_YELLOW = (255,255,0)            # Bright yellow
ORANGE = (245, 130, 49)        # Muted orange, not too bright
PURPLE = (102, 51, 153)        # Deep purple, rich tone
CYAN = (0, 139, 139)           # Dark cyan, with some depth
PINK = (255, 182, 193)         # Light pink, soft tone
BROWN = (139, 69, 19)          # Dark brown, earthy tone

WHITE_SQUARE_COLOR = OFF_WHITE
BLACK_SQUARE_COLOR = BLACK
DEBUG_AREA_COLOR = BROWN
SELECTED_SQUARE_COLOR = BRIGHT_YELLOW
TEXT_COLOR = BLACK
SQUARE_ALPHA = 150
HIGHLIGHT = YELLOW
HIGHLIGHT_CAPTURE = RED



# Screen area constants
TEXT_AREA_WIDTH = 600
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
TOTAL_WIDTH = WIDTH + TEXT_AREA_WIDTH

