
class StepCommand():
	def __init__(self):
		self.name = 's'
		self.longname = 'step'

	def execute(self, trace, editor):
		trace.step_forward()
