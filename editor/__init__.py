import curses
import curses.panel as panel

from emulator.state import State, initialize_state_from_rom
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.step import step

from .memory import MemoryPanel
from .disassembly import DisassemblyPanel
from .registers import RegisterPanel
from .colors import init_colors



def ui_main(stdscr):
	k = 0
	cursor_x = 0
	cursor_y = 0

	stdscr.clear()
	stdscr.refresh()

	init_colors()


	curses.curs_set(0)
	H, W = stdscr.getmaxyx()
	memory_panel_width = min(W // 2, 56)

	file = open('roms/invaders/invaders', 'rb')
	state = initialize_state_from_rom(file.read())

	memory_panel = MemoryPanel(0, 0, H, memory_panel_width)
	dissasembly_panel = DisassemblyPanel(0, memory_panel_width, 5, W - memory_panel_width)
	register_panel = RegisterPanel(H - 13, memory_panel_width, 14, W - memory_panel_width)

	while k != ord('q'):

		H, W = stdscr.getmaxyx()

		memory_panel.render(state)
		dissasembly_panel.render(state)
		register_panel.render(state)

		register_panel.set_size(14, W - memory_panel_width)

		k = stdscr.getch()

		if k == ord('s'):
			
			step(state)
			
			if memory_panel.is_out_of_frame(state.REG_UINT16[U16.PC]):
				memory_panel.set_target_address(state.REG_UINT16[U16.PC])




def run():
	curses.wrapper(ui_main)