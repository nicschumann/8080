import curses
import curses.panel as panel

from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.opcodes import OPCODE_TABLE

from .utils import int_to_hex


class DisassemblyPanel():
	def __init__(self, y, x, lines, cols):
		self.window = curses.newwin(lines, cols, y, x)
		# self.panel = panel.new_panel(self.window)

		self.line_offset = 1
		self.line_margin = 20
		self.op_margin = 5

	def render(self, state):
		self.window.clear()

		H, W = self.window.getmaxyx()
		PC = state.REG_UINT16[U16.PC]

		opcode = state.MEM[PC]
		
		try:
			op = OPCODE_TABLE[opcode]
			line = f'{int_to_hex(PC, fill=4)}:'
			name, args, _ = op.get_tokens(state, PC)
		
		except KeyError: 
			name = f'unrecognized: {opcode}'
			args = []
		

		self.window.addstr(H // 2, self.line_offset, line)
		self.window.addstr(H // 2, self.line_margin, name)
		self.window.addstr(H // 2, self.line_margin + self.op_margin, ', '.join(args))

		self.window.border()
		self.window.refresh()
