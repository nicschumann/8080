import curses
import curses.panel as panel

from emulator.state import State, initialize_state_from_rom
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.step import step
from .utils import int_to_hex, int_to_bin
from .colors import GRAY_COLOR, REG_U8_COLORS, REG_U16_COLORS

class RegisterPanel():
	def __init__(self, y, x, lines, cols):
		assert lines >= 14, '[RegisterPanel] Error: not enough lines to show the entire register file.'
		self.window = curses.newwin(lines, cols, y, x)

		self.y = y
		self.x = x
		self.lines = lines
		self.cols = cols
		self.half_w = cols // 2

	def set_size(self, lines, cols):
		self.window.resize(lines, cols)
		self.lines = lines
		self.cols = cols
		self.half_w = cols // 2


	def render_binary_string(self, win, string, pos=(0,0)):
		y, x = pos
		for i, c in enumerate(list(string)):
			if c == '0':
				win.attron(curses.color_pair(GRAY_COLOR))
			elif c == '1':
				win.attrset(0)

			win.addstr(y, x + i, c)

		win.attrset(0)


	def render_uint8_reg(self, state: State, reg: int, pos=(0,0)):
		y,x = pos
		large_display = 18 < self.half_w

		sc = '┼' if reg > 0 else '┬'
		ec = '┼' if reg < U8.MAX_REG - 2 else '┴'

		win = self.window
		# win.clear()

		# Borders
		win.attron(curses.color_pair(GRAY_COLOR))
		self.render_v_border(y-1, y+2, x+3, start_chr=sc, end_chr=ec)
		if large_display: 
			self.render_v_border(y-1, y+2, x+8, start_chr=sc, end_chr=ec)
		win.attrset(0)

		# Reg Name
		win.attron(curses.color_pair(REG_U8_COLORS[reg]))
		win.attron(curses.A_BOLD)
		win.addstr(y, x, f' {U8.to_string(reg)}')
		win.attrset(0)

		# Reg Values
		win.addstr(y, x + 5, f'{int_to_hex(int(state.REG_UINT8[reg]))}')
		if large_display:
			data = f'{int_to_bin(int(state.REG_UINT8[reg]))}'
			self.render_binary_string(win, data, pos=(y, x+10))

		win.attrset(0)
		# win.refresh()


	def render_flags_reg(self, state: State, pos=(0,0)):
		y, x = pos
		large_display = 18 < self.half_w
		win = self.window
		PSW = state.processor_status_word()

		win.attron(curses.color_pair(GRAY_COLOR))
		self.render_v_border(y-1, y+2, x+3, start_chr='┬', end_chr='┼')
		if large_display: self.render_v_border(y-1, y+2, x+8, start_chr='┬', end_chr='┼')
		win.attrset(0)

		win.attron(curses.A_BOLD)
		win.addstr(y, x, f' F')
		win.attrset(0)

		win.addstr(y, x + 5, f'{int_to_hex(int(PSW))}' )
		if large_display:
			data = f'{int_to_bin(int(PSW))}'
			self.render_binary_string(win, data, pos=(y, x+10))
			win.addstr(y - 1, x + 10, 'S')
			win.addstr(y - 1, x + 11, 'Z')
			win.addstr(y - 1, x + 13, 'A')
			win.addstr(y - 1, x + 15, 'P')
			win.addstr(y - 1, x + 17, 'C')


	def render_uint16_reg(self, state: State, reg: int, pos=(0,0)):
		y, x = pos
		win = self.window
		large_display = 28 < 2 * self.half_w
		sc = '┼' if reg > 0 else '┬'
		ec = '┼' if reg < U16.MAX_REG - 2 else '┴'


		# Borders
		win.attron(curses.color_pair(GRAY_COLOR))
		self.render_v_border(y-1, y+2, x+3, start_chr='┼', end_chr=ec)
		# win.addstr(y, x + 3, f'|')
		if large_display:
			self.render_v_border(y-1, y+2, x+10, start_chr=sc, end_chr=ec)
		win.attrset(0)

		# Name
		win.attron(curses.color_pair(REG_U16_COLORS[reg]))
		win.attron(curses.A_BOLD)
		win.addstr(y, x, f'{U16.to_string(reg)}')
		win.attrset(0)

		win.addstr(y, x + 5, f'{int_to_hex(int(state.REG_UINT16[reg]), fill=4)}')
		if large_display:
			data = f'{int_to_bin(int(state.REG_UINT16[reg]), fill=16)}'
			self.render_binary_string(win, data, pos=(y, x + 12))

		win.attrset(0)


	def render_h_border(self, y, start_x, end_x, start_chr='├', end_chr='┤', mid_chr='─'):
		for x in range(start_x + 1, end_x - 1):
			self.window.addstr(y, x, mid_chr)

		self.window.addstr(y, start_x, start_chr)
		self.window.addstr(y, end_x - 1, end_chr)

	def render_v_border(self, start_y, end_y, x, start_chr='┬', end_chr='┴', mid_chr='│'):
		for y in range(start_y + 1, end_y - 1):
			self.window.addstr(y, x, mid_chr)

		self.window.addstr(start_y, x, start_chr)
		self.window.addstr(end_y-1, x, end_chr)


	def render(self, state):
		self.window.clear()

		# render border and table elements
		self.window.attron(curses.color_pair(GRAY_COLOR))

		self.render_v_border(0, self.lines - 1, 0)
		self.render_v_border(0, self.lines - 1, self.cols - 1)
		self.render_h_border(0, 0, self.cols, start_chr='┌', end_chr='┐' )
		self.render_h_border(12, 0, self.cols, start_chr='└', end_chr='┘' )

		self.render_h_border(2, 0, self.cols)
		self.render_h_border(4, 0, self.cols)
		self.render_h_border(6, 0, self.cols)
		self.render_h_border(8, 0, self.cols)
		self.render_h_border(10, 0, self.cols)

		self.window.attrset(0)

		# render register states
		self.render_uint8_reg(state, U8.A, pos=(1, 1))
		self.render_flags_reg(state, pos=(1, self.half_w))

		self.render_uint8_reg(state, U8.B, pos=(3, 1))
		self.render_uint8_reg(state, U8.C, pos=(3, self.half_w))

		self.render_uint8_reg(state, U8.D, pos=(5, 1))
		self.render_uint8_reg(state, U8.E, pos=(5, self.half_w))

		self.render_uint8_reg(state, U8.H, pos=(7, 1))
		self.render_uint8_reg(state, U8.L, pos=(7, self.half_w))

		self.render_uint16_reg(state, U16.SP, pos=(9, 1))
		self.render_uint16_reg(state, U16.PC, pos=(11, 1))

		# blit
		self.window.refresh()

		