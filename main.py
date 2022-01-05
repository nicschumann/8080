from sys import argv
from disassembler import disassemble
from emulator import emulate_from_rom

from emulator.opcodes import NEW_OPCODE_TABLE


# Run as: python -m main





filepath = argv[1] # just get the second arg and assume its an 8080 binary c:
file = open(filepath, 'rb')

emulate_from_rom(file.read())

# disassemble(file)

file.close()