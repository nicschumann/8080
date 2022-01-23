import curses
import curses.panel as panel

from emulator.trace import Trace
from emulator.state import State, initialize_state_from_rom
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16

from emulator.step import step

from .input import InputPanel
from .memory import MemoryPanel
from .disassembly import DisassemblyPanel
from .registers import RegisterPanel
from .colors import init_colors

from .commands import EDITOR_COMMAND_TABLE
from .commands import parse_command_string



class EditorState():
	def __init__(self, screen):
		curses.curs_set(0)
		init_colors()

		screen.clear()
		screen.refresh()
		H, W = screen.getmaxyx()
		MPW = min(W // 2, 56) # width of the memory panel.
			
		self.parent_screen = screen
		self.input_panel = InputPanel(H - 1, W)
		self.memory_panel = MemoryPanel(0, 0, H - 1, MPW)
		self.dissasembly_panel = DisassemblyPanel(0, MPW, H - 13, W - MPW)
		self.register_panel = RegisterPanel(H - 14, MPW, 14, W - MPW)

		self.is_running = True

		self.partial_input = ''
		self.command_history = []


	def render(self, trace):
		H, W = self.parent_screen.getmaxyx()
		MPW = min(W // 2, 56) # this should be in the memory panel module, really...

		state = trace.current_state()

		if self.memory_panel.is_out_of_frame(state.REG_UINT16[U16.PC]):
			self.memory_panel.set_target_address(state.REG_UINT16[U16.PC])

		if self.dissasembly_panel.is_out_of_frame(state.REG_UINT16[U16.PC]):
			self.dissasembly_panel.set_target_address(state.REG_UINT16[U16.PC])
	
		# update sizes based on potential resize
		self.register_panel.set_size(14, W - MPW)

		self.memory_panel.render(state)
		self.dissasembly_panel.render(state)
		self.register_panel.render(state)

		last_command_name = self.command_history[-1].longname if len(self.command_history) else ''
		self.input_panel.render(self.partial_input, last_command_name)
	

	def handle_input(self):
		k = self.parent_screen.getch()

		KEY_DEL = 127
		KEY_NEWLINE = 10

		if k == KEY_NEWLINE and self.partial_input == '':
			# in this case, we want to repeat the last command.
			# just pull it out of the command_history, and we're good.
			try:
				command = self.command_history[-1]
				return command

			except IndexError:
				return None				


		if k == KEY_NEWLINE:
			# look up the current input in the list of commands.
			# execute the command. Same basic structure as the opcode data
			try:
				count, command_name, args = parse_command_string(self.partial_input)
				command_template = EDITOR_COMMAND_TABLE[command_name]
				# instantiate the command template with any args / repeats
				command = command_template(count, args) 

				self.command_history.append(command)
				self.partial_input = '' # clear input.
				return command

			except KeyError:
				return None


		if k == KEY_DEL:
			self.partial_input = self.partial_input[:len(self.partial_input) - 1]


		else:
			self.partial_input += chr(k)
			# self.partial_input += f':{int(k)}' # useful for debugging codes

		return None




def ui_main(stdscr):

	file = open('roms/invaders/invaders', 'rb')
	state = initialize_state_from_rom(file.read())
	trace = Trace(state)
	editor = EditorState(stdscr)

	while editor.is_running: 
		editor.render(trace)
		command = editor.handle_input()

		if command is not None: command.execute(trace, editor)


def run():
	curses.wrapper(ui_main)