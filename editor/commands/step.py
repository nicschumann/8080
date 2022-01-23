from editor.commands.abstract import Command


class StepCommand(Command):
	name : str = 's'
	longname : str = 'step'
		
	def execute(self, trace, editor):
		for i in range(self.repeats):
			trace.step_forward()
