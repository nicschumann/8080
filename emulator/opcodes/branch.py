import numpy as np

from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


# JMP GROUP ======

class JCOND_Imm(Op):
	def __init__(self, code: bytes, name: str, predicate):
		comment_string = '\t\t; PC := {1}{0}'
		super().__init__(code, name, ['{1}{0}'], [1,1], comment_string)
		self.predicate = predicate

	def step(self, state: State):
		if self.predicate(state.FLAGS):
			PC = state.REG_UINT16[U16.PC]
			low_byte = state.MEM[ PC ]
			high_byte = state.MEM[ PC + 0x1 ]
			addr = self.subop_u8_pair_to_u16(high_byte, low_byte)
			state.REG_UINT16[ U16.PC ] = addr 
		
		else:
			state.REG_UINT16[U16.PC] += 0x2

	def test(self, preop_state: State, postop_state: State):
		if self.predicate(preop_state.FLAGS):
			PC = preop_state.REG_UINT16[U16.PC]
			addr = (preop_state.MEM[PC + 0x2] << 8) | preop_state.MEM[ PC + 0x1 ]
			PC_has_jumped = postop_state.REG_UINT16[U16.PC] == addr

			assert PC_has_jumped, f'[jmp] PC\' =/= data:{addr}'

		else:
			PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x03
			assert PC_has_incremented, f'[no-jmp] PC\' =/= PC + 0x2'
