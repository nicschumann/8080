from sys import argv
from disassembler import disassemble
# from emulator import emulate_from_rom

# Run as: python -m main

filepath = argv[1] # just get the second arg and assume its an 8080 binary c:
file = open(filepath, 'rb')

disassemble(file)

file.close()