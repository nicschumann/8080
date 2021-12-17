import numpy as np
from emulator.state import State
from emulator.state import Uint16Registers as U16
from emulator.state import Uint8Registers as U8
from emulator.state import FlagsRegisters as F

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

	def disassembly_data(self):
		return [self.name, self.str_args, self.comment], self.byte_arg_counts


	def mem_invariant(self, preop_state: State, postop_state: State):
		return np.all(preop_state.MEM == postop_state.MEM)


	def subop_addr_from_H_and_L(self, state: State):
		return (state.REG_UINT8[ U8.H ] << 8) | state.REG_UINT8[ U8.L ]


	def step(self, state: State):
		assert False, f"[{self.code}] {self.name}: step unimplemented!"

	def test(self, preop_state: State, postop_state: State):
		assert False, f"[{self.code}] {self.name}: test unimplemented!"

	def get_name(self):
		return f'{hex(self.code)}: {self.name}'


def UnimplementedOp(Op):
	def __init__(self):
		super().__init__('none', 'unimplimented', [], [], '')