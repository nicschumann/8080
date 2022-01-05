from .state import State, initialize_state_from_rom
from .state import FlagsRegisters as F
from .step import step


def emulate_from_rom(rom: bytes):
	state = initialize_state_from_rom(rom)
	state.FLAGS[F.E] = True

	while state.FLAGS[F.E]:
		print(state)

		try:
			step(state)
			input()
		except:
			print('Exception')
			state.FLAGS[F.E] = False

	print('Done.')



	




# if __name__ == '__main__':
# 	filepath = './roms/invaders/invaders'
# 	file = open(filepath, 'rb')
# 	data = file.read()

# 	state = initialize_state_from_rom(data)
# 	print(state)

# 	emulate(state)


# print(b'\x02'[0] & b'\x03'[0])