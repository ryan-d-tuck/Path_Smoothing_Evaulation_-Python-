import sys,os

#Game Constants
SYS_PATH            = sys.path[0]
SCREEN_WIDTH        = 640
SCREEN_HEIGHT       = 640
BG_COLOR            = 175, 238, 238

QUAD_TREE_DEPTH     = 9
QT_EMPTY            = 0
QT_FULL             = 1
QT_OPEN             = 2

RDP_EPSILON         = 20

RPF_MAX_DIST        = 100

INFINITY            = 100000000000

WORLD_BLOCK_COLOR   = 25, 25, 25 #79, 115, 0

QUAD_EMPTY_LINE_COLOR = 250,218,221
QUAD_FULL_LINE_COLOR = 227,38,54
QUAD_OPEN_LINE_COLOR = 102,2,60

NAV_NODE_COLOR      = 0,49,83
NAV_LINE_COLOR      = 220, 208, 255

PATH_LINE_COLOR     = 160, 92, 240

LEFT                = 1
MIDDLE              = 2
RIGHT               = 3

ALG_ASTAR           = 0
ALG_ASTAR_PS        = 1
ALG_THETA_STAR      = 2
ALG_RDP             = 3
ALG_FUNNEL          = 4
ALG_RPF             = 5


OPTIMIZE_QUADS      = 0
TIMES_TO_RUN_ALG    = 5
CURR_ALG            = ALG_RDP
MAP_NAME            = "AR0204SR"

