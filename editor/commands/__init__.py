from .step import StepCommand
from .quit import QuitCommand


EDITOR_COMMAND_LIST = [
	StepCommand(),
	QuitCommand()
]

EDITOR_COMMAND_TABLE = {command.name: command for command in EDITOR_COMMAND_LIST}