import curses
from .colors import GRAY_BG_COLOR, WHITE_BG_COLOR

class InputPanel():
	def __init__(self, y, cols):
		self.y = y
		self.cols = cols

		self.window = curses.newwin(2, cols, y, 0)

	def render(self, input_data):
		self.window.clear()
		self.window.attron(curses.color_pair(WHITE_BG_COLOR))
		self.window.attron(curses.A_BOLD)
		H, W = self.window.getmaxyx()

		self.window.addstr(0, 0, input_data)

		for i in range(len(input_data), W):
			self.window.addstr(0, i, ' ')

		self.window.attrset(0)
		self.window.refresh()

