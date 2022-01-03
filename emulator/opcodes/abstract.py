import numpy as np
from emulator.state import State
from emulator.state import Uint16Registers as U16
from emulator.state import Uint8Registers as U8
from emulator.state import FlagsRegisters as F
from functools import reduce

class Op:
	def __init__(
			self, 
			code: bytes, # hexcode of the op
			name: str, # assembly name of the op
			str_args: list, # list of argnames,
			byte_arg_counts: list, # additional bytes to read from memory 
			comment: str # comment to display in disassembly
		):
		self.code = code
		self.name = name
		self.str_args = str_args
		self.byte_arg_counts = byte_arg_counts
		self.comment = comment

	def step(self, state: State):
		assert False, f"[{self.code}] {self.name}: step unimplemented!"

	def test(self, preop_state: State, postop_state: State):
		assert False, f"[{self.code}] {self.name}: test unimplemented!"

	def disassembly_data(self):
		return [self.name, self.str_args, self.comment], self.byte_arg_counts

	def get_name(self):
		return f'{hex(self.code)}: {self.name} {", ".join(self.str_args)}'

	def mem_invariant(self, preop_state: State, postop_state: State):
		return np.all(preop_state.MEM == postop_state.MEM)

	def subop_u8_pair_to_u16(self, high, low):
		return high << 8 | low

	def subop_u16_to_u8_pair(self, value):
		high_bits = value >> 8
		low_bits = value & 0xFF

		return high_bits, low_bits

	def subop_addr_from_HL(self, state: State):
		return self.subop_u8_pair_to_u16(state.REG_UINT8[ U8.H ], state.REG_UINT8[ U8.L ])

	def subop_setflags_add(self, result: int, state: State, CY=True):
		"""result may be a 16-bit uint"""
		state.FLAGS[ F.Z ] = True if result & 0xFF == 0 else False
		state.FLAGS[ F.S ] = True if result & 0x80 != 0 else False
		state.FLAGS[ F.P ] = True if (result & 0xFF) % 2 == 0 else False 
		
		if CY:
			state.FLAGS[ F.CY ] = True if result > 0xFF or result < 0x00 else False

	def subop_add(self, *arguments):
		return reduce(lambda a,b: a + b, map(int, arguments))

	def subop_sub(self, *arguments):
		return reduce(lambda a,b: a - b, map(int, arguments))

	def subop_and(self, *arguments):
		return reduce(lambda a,b: a & b, map(int, arguments))

	def subop_xor(self, *arguments):
		return reduce(lambda a,b: a ^ b, map(int, arguments))

	def subop_or(self, *arguments):
		return reduce(lambda a,b: a | b, map(int, arguments))





def UnimplementedOp(Op):
	def __init__(self):
		super().__init__('none', 'unimplimented', [], [], '')