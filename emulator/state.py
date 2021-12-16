import numpy as np
from dataclasses import dataclass

@dataclass
class Uint8Registers():
	A : int = 0
	B : int = 1
	C : int = 2
	D : int = 3
	E : int = 4
	H : int = 5
	L : int = 6

	MAX_REG : int = 7


@dataclass
class Uint16Registers():
	SP : int = 0
	PC : int = 1

	MAX_REG : int = 2


@dataclass
class FlagsRegisters():
	Z  : int = 0
	S  : int = 1
	P  : int = 2
	CY : int = 3
	AC : int = 464
	E  : int = 5

	MAX_REG : int = 6



@dataclass
class State:
	MEMSIZE = 2 ** 16 # 65536 = 64k bytes

	# register file ---------------------

	REG_UINT8 : np.array = np.zeros(Uint8Registers.MAX_REG).astype(np.uint8)
	REG_UINT16 : np.array = np.zeros(Uint16Registers.MAX_REG).astype(np.uint16)
	FLAGS : np.array = np.zeros(FlagsRegisters.MAX_REG).astype(bool)


	# memory layout ---------------------
	# 0x0000 – 0x1FFF: ROM
	# -----------------------------------
	# 0x2000 – 0x23FF: STACK 
	# 0x2400 – 0x3FFF: HEAP
	# -----------------------------------

	MEM : np.array = np.zeros(MEMSIZE).astype(np.uint8) # 8KB mem


	def clone(self):
		new_state = State()
		new_state.REG_UINT8 = self.REG_UINT8.copy()
		new_state.REG_UINT16 = self.REG_UINT16.copy()
		new_state.FLAGS = self.FLAGS.copy()
		new_state.MEM = self.MEM.copy()

		return new_state


	def __eq__(self, other_state):
		uint8_reg_equal = np.all(self.REG_UINT8 == other.REG_UINT8)
		uint16_reg_equal = np.all(self.REG_UINT16 == other.REG_UINT16)
		flags_reg_equal = np.all(self.FLAGS == other.FLAGS)
		mem_equal = np.all(self.MEM == other.MEM)

		return uint8_reg_equal and uint16_reg_equal and flags_reg_equal and mem_equal

	def __repr__(self):
		rep  = f'A: {hex(self.REG_UINT8[Uint8Registers.A])}\n'
		rep += f'B: {hex(self.REG_UINT8[Uint8Registers.B])}\tC:{hex(self.REG_UINT8[Uint8Registers.C])}\n'
		rep += f'D: {hex(self.REG_UINT8[Uint8Registers.D])}\tD:{hex(self.REG_UINT8[Uint8Registers.D])}\n'
		rep += f'H: {hex(self.REG_UINT8[Uint8Registers.H])}\tL:{hex(self.REG_UINT8[Uint8Registers.L])}\n\n'

		rep += f'SP: {hex(self.REG_UINT16[Uint16Registers.SP])}\nPC: {hex(self.REG_UINT16[Uint16Registers.PC])}\n\n'

		rep += f'Z: {int(self.FLAGS[FlagsRegisters.Z])}, '
		rep += f'S: {int(self.FLAGS[FlagsRegisters.S])}, '
		rep += f'P: {int(self.FLAGS[FlagsRegisters.P])}, '
		rep += f'CY: {int(self.FLAGS[FlagsRegisters.CY])}, '
		rep += f'CY: {int(self.FLAGS[FlagsRegisters.AC])}, '
		rep += f'E: {int(self.FLAGS[FlagsRegisters.E])}'

		return rep



def initialize_state_from_rom(data: bytes):
	
	state = State()
	ROM = np.frombuffer(data, dtype=np.uint8)
	state.MEM[:ROM.shape[0]] = ROM

	return state