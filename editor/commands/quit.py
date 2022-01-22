
class QuitCommand():
	def __init__(self):
		self.name = 'q'
		self.longname = 'quit'

	def execute(self, trace, editor):
		editor.is_running = False
