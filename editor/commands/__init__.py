from .step import StepCommand


EDITOR_COMMAND_LIST = [
	StepCommand()
]

EDITOR_COMMAND_TABLE = {command.name: command for command in EDITOR_COMMAND_LIST}