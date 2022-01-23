from .step import StepCommand
from .quit import QuitCommand


def parse_command_string(partial_input: str):
	parts = partial_input.strip().split(' ')

	try:
		if len(parts) > 1:
			count = int(parts[0])
			command = parts[1]
			args = parts[2:]

		else:
			count = 1
			command = parts[0]
			args = []


	except ValueError:
		count = 1
		command = parts[0]
		args = parts[1:]

	return count, command, args


EDITOR_COMMAND_LIST = [
	StepCommand,
	QuitCommand
]

EDITOR_COMMAND_TABLE = {command.name: command for command in EDITOR_COMMAND_LIST}