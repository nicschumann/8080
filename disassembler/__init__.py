from .opcodes import OPCODE_TABLE
from .colors import set_format_and_color

def set_format(line_number, dissasembly, argument_data):
	command, argument_formats, comment = dissasembly
	arguments = list(map(lambda a: a.format(*argument_data), argument_formats))
	comment = comment.format(*argument_data)
	return line_number + command + ' ' + ', '.join(arguments) + comment


def disassemble(file):
	# Disassembly Loop
	opcode = file.read(1)

	i = 0
	while opcode:
		line_number = file.tell() - 1

		try:
			dissasembly, argsizes = OPCODE_TABLE[opcode]

		except KeyError:
			print(f'\n[Disassembler Error] Unrecognized opcode: {opcode.hex()}')
			exit()

		arguments = tuple(map(lambda argsize: bytearray(file.read(argsize)).hex(), argsizes))

		line_number = f'{hex(line_number)}:\t\t'	

		try: 
			line = set_format_and_color(line_number, dissasembly, arguments)
			print(line);
			opcode = file.read(1)
			i += 1

		except ValueError:
			print(f'[Disassembler Error] misformatted instruction table entry: {opcode.hex()}')
			exit()