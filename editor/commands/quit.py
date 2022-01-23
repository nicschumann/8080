from editor.commands.abstract import Command

class QuitCommand(Command):
	name : str = 'q'
	longname : str = 'quit'	

	def execute(self, trace, editor):
		editor.is_running = False
