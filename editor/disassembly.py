import curses
import curses.panel as panel

from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.opcodes import OPCODE_TABLE

from .utils import int_to_hex
from .colors import GRAY_COLOR, REG_U16_COLORS


class DisassemblyPanel():
	def __init__(self, y, x, lines, cols):
		self.window = curses.newwin(lines, cols, y, x)
		# self.panel = panel.new_panel(self.window)

		self.line_offset = 2
		self.line_margin = 20
		self.op_margin = 5
		self.target_addr = 0x00
		# this isn't correct because it doesn't account for instruction lengths
		# but it gets fixed as soon as we call render()
		self.max_addr = lines 

	def set_target_address(self, addr):
		self.target_addr = addr

	def is_out_of_frame(self, addr):
		return addr < self.target_addr or addr >= self.max_addr

	def render(self, state):
		self.window.clear()

		H, W = self.window.getmaxyx()
		PC = state.REG_UINT16[U16.PC]

		current_addr = self.target_addr

		for line_index in range(1, H - 1):
			opcode = state.MEM[current_addr]

			try:
				op = OPCODE_TABLE[opcode]
				line = f'{int_to_hex(current_addr, fill=4)}:'
				name, args, _ = op.get_tokens(state, current_addr)
				
			
			except KeyError: 
				name = f'unrecognized: {opcode}'
				args = []
				break

			color_id = REG_U16_COLORS[U16.PC] if current_addr == state.REG_UINT16[U16.PC] else GRAY_COLOR
			self.window.attron(curses.color_pair(color_id))

			self.window.addstr(line_index, self.line_offset, line)
			self.window.attrset(0)

			self.window.addstr(line_index, self.line_margin, name)
			self.window.addstr(line_index, self.line_margin + self.op_margin, ', '.join(args))

			current_addr += len(op)

		self.max_addr = current_addr
		self.window.refresh()
