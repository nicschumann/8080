import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

COLOR_TABLE = {
	# opcode colors
	'nop': Style.DIM,
	'misc': Fore.BLUE,
	'jump': Style.BRIGHT + Fore.CYAN,
	'call': Style.BRIGHT + Fore.MAGENTA,
	'lsi-8bit': '',
	'lsi-16bit': Style.BRIGHT,
	'al-8bit': Fore.YELLOW,
	'al-16bit': Style.BRIGHT + Fore.YELLOW,
	
	# arguments to commands
	'A': Fore.RED + Style.BRIGHT,
	'B': Fore.RED,
	'C': Fore.RED,
	'D': Fore.RED,
	'E': Fore.RED,
	'F': Fore.RED,
	'H': Fore.RED,
	'L': Fore.RED,
	'M': Fore.GREEN + Style.BRIGHT,
	'PSW': Fore.RED,
	'memory': Fore.GREEN,
	'data': Style.BRIGHT,

	# other stuff
	'comment': Style.DIM,
	'punc': Style.DIM,
	'line': Style.DIM,
}

OPCODE_TYPES = {
	'nop': 'nop',
	'*nop': 'nop',
	'rim': 'nop',
	'sim': 'nop',

	'in': 'misc',
	'ei': 'misc',
	'out': 'misc',
	'hlt': 'misc',

	'jmp': 'jump',
	'jm': 'jump',
	'jc': 'jump',
	'jz': 'jump',
	'jnz': 'jump',
	'jnc': 'jump',
	'jpo': 'jump',
	'pchl': 'jump',

	'call': 'call',
	'cnz': 'call',
	'cpe': 'call',
	'cz': 'call',
	'cm': 'call',
	'ret': 'call',
	'rnz': 'call',
	'rpo': 'call',
	'rz': 'call',
	'rc': 'call',
	'rp': 'call',
	'rm': 'call',
	'rnc': 'call',

	'rst': 'call',

	'push': 'lsi-16bit',
	'pop': 'lsi-16bit',
	'lxi': 'lsi-16bit',
	'shld': 'lsi-16bit',
	'xchg': 'lsi-16bit',
	'xthl': 'lsi-16bit',
	'lhld': 'lsi-16bit',
	'ldax': 'lsi-16bit',
	'stax': 'lsi-16bit',

	'mov': 'lsi-8bit',
	'mvi': 'lsi-8bit',
	'sta': 'lsi-8bit',
	'lda': 'lsi-8bit',

	'inx': 'al-16bit',
	'dcx': 'al-16bit',
	'dad': 'al-16bit',

	'inr': 'al-8bit',
	'ana': 'al-8bit',
	'ani': 'al-8bit',
	'adi': 'al-8bit',
	'add': 'al-8bit',
	'adc': 'al-8bit',
	'cmp': 'al-8bit',
	'cmc': 'al-8bit',
	'cma': 'al-8bit',
	'daa': 'al-8bit',
	'dcr': 'al-8bit',
	'ora': 'al-8bit',
	'ori': 'al-8bit',
	'rrc': 'al-8bit',
	'rlc': 'al-8bit',
	'rar': 'al-8bit',
	'cpi': 'al-8bit',
	'xra': 'al-8bit',
	'sub': 'al-8bit',
	'sbi': 'al-8bit',
	'sbb': 'al-8bit',
	'sui': 'al-8bit',
	'stc': 'al-8bit',
	'xri': 'al-8bit',
}

def set_format_and_color(line_number, dissasembly, argument_data):
	command, argument_formats, comment = dissasembly

	# Color the line number with the line style.
	line_number = COLOR_TABLE['line'] + line_number + Style.RESET_ALL

	# format the arguments
	arguments = []

	for i in range(len(argument_formats)):
		argument = argument_formats[i]
		argument = argument.format(*argument_data)

		if argument in COLOR_TABLE:
			arguments.append(COLOR_TABLE[argument] + argument + Style.RESET_ALL)

		elif command[-1] == 'i': # denotes immediate value
			arguments.append(COLOR_TABLE['data'] + argument + Style.RESET_ALL)

		else:
			arguments.append(COLOR_TABLE['memory'] + argument + Style.RESET_ALL)

	# argument_formats = list(map(lambda f: f.format(*arguments), argument_formats))	
	
	try:
		command_color = COLOR_TABLE[ OPCODE_TYPES[command] ]

	except KeyError:
		print(f'\n[Disassembler Error] Missing command color assignment for \'{command}\'')
		exit()

	command = command_color + command + Style.RESET_ALL

	comment = COLOR_TABLE['comment'] + comment.format(*argument_data) + Style.RESET_ALL
	p_color = COLOR_TABLE['punc']

	return line_number + command + ' ' + (f'{ p_color }, {Style.RESET_ALL}'.join(arguments)) + comment