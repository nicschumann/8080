from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


class MOV_Reg_Reg(Op):
	def __init__(self, code: bytes, r1: int, r2: int):

		comment_string = f'\t\t; {U8.to_string(r1)} := {U8.to_string(r2)}'
		super().__init__(code, 'mov', [U8.to_string(r1), U8.to_string(r2)], [], comment_string)
		self.r1 = r1
		self.r2 = r2

	def step(self, state: State):
		state.REG_UINT8[ self.r1 ] = state.REG_UINT8[ self.r2 ]

	def test(self, preop_state: State, postop_state: State):
		R1_is_R2 = postop_state.REG_UINT8[ self.r1 ] == preop_state.REG_UINT8[ self.r2 ]
		R2_is_R2 = postop_state.REG_UINT8[ self.r2 ] == preop_state.REG_UINT8[ self.r2 ]

		assert R1_is_R2, f'{U8.to_string(self.r1)}\' =/= {U8.to_string(self.r2)}'
		assert R2_is_R2, f'{U8.to_string(self.r2)}\' =/= {U8.to_string(self.r2)}'






class MOV_Reg_Mem(Op):
	def __init__(self, code: bytes, r1: int):
		comment_string = f'\t\t; {U8.to_string(r1)} := (HL)'
		super().__init__(code, 'mov', [U8.to_string(r1), 'M'], [], comment_string)
		self.r1 = r1

	def step(self, state: State):
		memory_location = self.subop_address_from_HL(state)
		state.REG_UINT8[ self.r1 ] = state.MEM[memory_location]

	def test(self, preop_state: State, postop_state: State):
		memory_location = self.subop_address_from_HL(preop_state)

		R1_is_MEM = postop_state.REG_UINT8[ self.r2 ] == preop_state.MEM[ memory_location ]

		assert R1_is_MEM, f'{U8.to_string(self.r2)}\' =/= {U8.to_string(self.r1)}'
		assert R1_is_R2, f'{U8.to_string(self.r2)}\' =/= {U8.to_string(self.r2)}'





class LXI_Reg(Op):
	def __init__(self, code : bytes, r : int):
		super().__init__(code, 'lxi', [U8.to_string(r), '{1}{0}'], [1,1], '\t\t; B := data:{1}; C := data:{0}')
		self.r = r

	# def step(self, state: State):
	# 	pass

	# def test(self, preop_state: State, postop_state: State):
	# 	pass