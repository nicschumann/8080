from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


class ADD_Reg(Op):
	def __init__(self, code: bytes, r: int):

		comment_string = f'\t\t; A := {U8.to_string(r)} + A'
		super().__init__(code, 'add', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = state.REG_UINT8[ U8.A ] + state.REG_UINT8[ self.r ]
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		result = preop_state.REG_UINT8[self.r] + preop_state.REG_UINT8[U8.A]
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		R_invariant = self.r == U8.A or preop_state.REG_UINT8[self.r] == postop_state.REG_UINT8[self.r]
		
		assert A_is_sum, f'A\' =/= A + {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ADD_Mem(Op):
	def __init__(self, code: bytes):

		comment_string = f'\t\t; A := A + (H)(L) '
		super().__init__(code, 'add', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = state.REG_UINT8[U8.A] + state.MEM[addr]
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = preop_state.MEM[addr] + preop_state.REG_UINT8[U8.A]
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A + {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


