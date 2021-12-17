import numpy as np

from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


class NOP(Op):
	def __init__(self):
		super().__init__(0x00, 'nop', [], [], '')

	def step(self, state: State): pass

	def test(self, state: State, state_prime: State):
		MEM_is_unchanged = np.all(state.MEM == state_prime.MEM)
		U8_is_unchanged = np.all(state.REG_UINT8 == state_prime.REG_UINT8)
		PC_has_incremented = state.REG_UINT16[ U16.PC ] + 1 == state_prime.REG_UINT16[ U16.PC ]
		
		assert MEM_is_unchanged, "MEM =/= MEM'"
		assert U8_is_unchanged, "REG =/= REG'"
		assert PC_has_incremented, "PC + 1 =/= PC'"

