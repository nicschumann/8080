from .state import State, initialize_state_from_rom
from .step import step





def emulate_from_rom(rom: bytes):
	state = initialize_state_from_rom(data)


	










# if __name__ == '__main__':
# 	filepath = './roms/invaders/invaders'
# 	file = open(filepath, 'rb')
# 	data = file.read()

# 	state = initialize_state_from_rom(data)
# 	print(state)

# 	emulate(state)


# print(b'\x02'[0] & b'\x03'[0])