# Game constants and configuration

from pygame.locals import *

# Block dimensions
BWIDTH     = 20
BHEIGHT    = 20
MESH_WIDTH = 1

# Board configuration
BOARD_HEIGHT     = 7
BOARD_UP_MARGIN  = 40
BOARD_MARGIN     = 2

# Color definitions (RGB)
WHITE    = (255,255,255)
RED      = (255,0,0)
GREEN    = (0,255,0)
BLUE     = (0,0,255)
ORANGE   = (255,69,0)
GOLD     = (255,125,0)
PURPLE   = (128,0,128)
CYAN     = (0,255,255) 
BLACK    = (0,0,0)

# Game timing and events
MOVE_TICK          = 1000
TIMER_MOVE_EVENT   = USEREVENT+1
GAME_SPEEDUP_RATIO = 1.5
SCORE_LEVEL        = 2000
SCORE_LEVEL_RATIO  = 2 

# Scoring
POINT_VALUE       = 100
POINT_MARGIN      = 10

# UI
FONT_SIZE         = 25