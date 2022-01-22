import curses
from .colors import GRAY_BG_COLOR, WHITE_BG_COLOR

class InputPanel():
	def __init__(self, y, cols):
		self.y = y
		self.cols = cols

		self.window = curses.newwin(2, cols, y, 0)

	def render(self, partial_input, last_command_name):
		self.window.clear()
		self.window.attron(curses.color_pair(WHITE_BG_COLOR))
		self.window.attron(curses.A_BOLD)
		H, W = self.window.getmaxyx()

		command_string = f'({last_command_name}): {partial_input}'
		command_string = command_string + (' ' * (W - len(command_string)))

		self.window.addstr(0, 0, command_string)

		self.window.attrset(0)
		self.window.refresh()

