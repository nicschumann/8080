import curses
import curses.panel as panel

from emulator.state import State, initialize_state_from_rom
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.step import step


def int_to_hex(i, fill=2):
	return hex(i)[2:].zfill(fill)

class MemoryPanel():
	def __init__(self, lines, cols):
		self.window = curses.newwin(lines, cols, 0, 0)
		self.panel = panel.new_panel(self.window)
		self.target_addr = 0x00
		# self.panel.move(0,0)

		self.line_margin = 7 # blocks
		self.blocks_per_byte = 3 # one for each hex, and a space

	def set_size(self, H, W):
		self.window.resize(H, W)

	def set_target_address(self, addr):
		self.target_addr = addr

	def get_offset(self):
		H, W = self.window.getmaxyx()
		bytes_per_line = (W - self.line_margin - 1) // self.blocks_per_byte
		offset = ((H - 2) // 2) * bytes_per_line
		correction = (offset % bytes_per_line)
		
		return offset - correction + (bytes_per_line // 2), bytes_per_line  

	def is_out_of_frame(self, addr):
		offset, _ = self.get_offset()
		return addr < self.target_addr - offset or addr > self.target_addr + offset


	# renders
	def render(self, state: State):
		
		self.window.clear()
		H, W = self.window.getmaxyx()

		mem_len = len(state.MEM) // (H - 2)
		bytes_per_block = mem_len // (W - 7)

		# self.target_addr = state.REG_UINT16[U16.PC]
		address_space_size = len(state.MEM)

		offset, bytes_per_line = self.get_offset()	
		starting_addr = max(self.target_addr - offset, 0)
		current_addr = starting_addr

		for row in range(1, H - 1):
			
			self.window.attron(curses.A_DIM)
			self.window.addstr(row, 1, f'{int_to_hex(current_addr, fill=4)}:')
			self.window.attrset(0)

			for col in range(self.line_margin, W - self.blocks_per_byte, self.blocks_per_byte):
				if current_addr == state.REG_UINT16[U16.PC]:
					self.window.attron(curses.color_pair(1))

				byte = state.MEM[current_addr]

				self.window.addstr(row, col, f'{int_to_hex(byte)}')
				
				if current_addr == state.REG_UINT16[U16.PC]:
					self.window.attrset(0)
				
				current_addr += 1
				if current_addr >= address_space_size: break


		title = f' [{H}, {W}] [{int_to_hex(starting_addr, fill=4)} : {int_to_hex(current_addr, fill=4)}] ({bytes_per_line} bytes/line) '
		if len(title) >= W:
			title = f'[{hex(starting_addr)[2:]} : {hex(current_addr)[2:]}]'

		cursor_x = max(W // 2 - len(title) // 2, 0)
		cursor_y = H // 2
		self.window.attron(curses.A_BOLD)
		
		self.window.border()
		# self.window.attron(curses.color_pair(3))
		if len(title) <= W: self.window.addstr(H - 1, cursor_x, title)
		self.window.attrset(0)

		self.window.move(0,0)

		# refresh loop
		self.window.refresh()
		self.panel.show()



def ui_main(stdscr):
	k = 0
	cursor_x = 0
	cursor_y = 0

	stdscr.clear()
	stdscr.refresh()

	curses.start_color()
	# program counter color
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.curs_set(0)
	H, W = stdscr.getmaxyx()

	file = open('roms/invaders/invaders', 'rb')
	state = initialize_state_from_rom(file.read())

	memory_panel = MemoryPanel(H, W)

	while k != ord('q'):

		H, W = stdscr.getmaxyx()

		memory_panel.set_size(H, min(W // 2, 56))
		memory_panel.render(state)

		k = stdscr.getch()

		if k == ord('s'):
			
			step(state)
			
			if memory_panel.is_out_of_frame(state.REG_UINT16[U16.PC]):
				memory_panel.set_target_address(state.REG_UINT16[U16.PC])




def run():
	curses.wrapper(ui_main)