from sys import argv
from disassembler import disassemble


filepath = argv[1] # just get the second arg and assume its an 8080 binary c:
file = open(filepath, 'rb')

disassemble(file)

file.close()