import curses


GRAY_COLOR = 17
GRAY_FG = (350, 350, 350)

LINE_FG_COLOR = 25
LINE_FG = (500, 500, 500)

REG_A_COLOR = 26
REG_A_FG = (1000, 100, 0)

REG_U8_COLOR = 27
REG_U8_FG = (200, 500, 800)

REG_PC_COLOR = 28
REG_PC_FG = (000, 700, 800)

REG_SP_COLOR = 29
REG_SP_FG = (700, 800, 000)

REG_U8_COLORS = [
	REG_A_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
	REG_U8_COLOR,
]

REG_U16_COLORS = [
	REG_SP_COLOR,
	REG_PC_COLOR
]

def init_colors():
	curses.start_color()
	# program counter color

	curses.init_color(REG_A_COLOR, *REG_A_FG)
	curses.init_color(REG_U8_COLOR, *REG_U8_FG)

	curses.init_color(REG_SP_COLOR, *REG_SP_FG)
	curses.init_color(REG_PC_COLOR, *REG_PC_FG)

	curses.init_color(GRAY_COLOR, *GRAY_FG)

	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
	curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	
	curses.init_pair(GRAY_COLOR, GRAY_COLOR, curses.COLOR_BLACK)
	curses.init_pair(REG_A_COLOR, REG_A_COLOR, curses.COLOR_BLACK)
	curses.init_pair(REG_U8_COLOR, REG_U8_COLOR, curses.COLOR_BLACK)
	curses.init_pair(REG_SP_COLOR, REG_SP_COLOR, curses.COLOR_BLACK)
	curses.init_pair(REG_PC_COLOR, REG_PC_COLOR, curses.COLOR_BLACK)
