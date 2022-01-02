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


class ADC_Reg(Op):
	def __init__(self, code: bytes, r: int):

		comment_string = f'\t\t; A := A + {U8.to_string(r)} + CY'
		super().__init__(code, 'adc', [f'{U8.to_string(r)}'], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = state.REG_UINT8[ U8.A ] + state.REG_UINT8[ self.r ] + state.FLAGS[F.CY]
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		result = preop_state.REG_UINT8[self.r] + preop_state.REG_UINT8[U8.A] + preop_state.FLAGS[F.CY]
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		R_invariant = self.r == U8.A or preop_state.REG_UINT8[self.r] == postop_state.REG_UINT8[self.r]
		
		assert A_is_sum, f'A\' =/= A + {U8.to_string(self.r)} + CY (== {preop_state.FLAGS[F.CY]})'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'

class ADC_Mem(Op):
	def __init__(self, code: bytes):

		comment_string = f'\t\t; A := A + (HL) + CY'
		super().__init__(code, 'adc', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = state.REG_UINT8[ U8.A ] + state.MEM[ addr ] + state.FLAGS[F.CY]
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = preop_state.MEM[addr] + preop_state.REG_UINT8[U8.A] + preop_state.FLAGS[F.CY]
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A + MEM + CY (== {preop_state.FLAGS[F.CY]})'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'

class ADI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A + data:{0} (add immediate)'
		super().__init__(code, 'adc', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		data = state.MEM[ data_pointer ]
		result = state.REG_UINT8[U8.A] + data
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = preop_state.REG_UINT8[U8.A] + preop_state.MEM[data_pointer]

		A_is_sum = postop_state.REG_UINT8[U8.A] == (data & 0xFF)
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A + MEM[PC + 1])'
		assert PC_has_incremented, 'PC\' =/= PC + 2'

