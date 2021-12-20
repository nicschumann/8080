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
		memory_location = self.subop_addr_from_HL(state)
		state.REG_UINT8[ self.r1 ] = state.MEM[memory_location]

	def test(self, preop_state: State, postop_state: State):
		memory_location = self.subop_addr_from_HL(preop_state)

		R1_is_MEM = postop_state.REG_UINT8[ self.r1 ] == preop_state.MEM[ memory_location ]

		assert R1_is_MEM, f'{U8.to_string(self.r2)}\' =/= {U8.to_string(self.r1)}'
		# assert R1_is_R2, f'{U8.to_string(self.r2)}\' =/= {U8.to_string(self.r2)}'




class MOV_Mem_Reg(Op):
	def __init__(self, code: bytes, r1: int):
		comment_string = f'\t\t; {U8.to_string(r1)} := (HL)'
		super().__init__(code, 'mov', ['M', U8.to_string(r1)], [], comment_string)
		self.r1 = r1

	def step(self, state: State):
		memory_location = self.subop_addr_from_HL(state)
		state.MEM[memory_location] = state.REG_UINT8[ self.r1 ]

	def test(self, preop_state: State, postop_state: State):
		memory_location = self.subop_addr_from_HL(preop_state)

		MEM_is_R1 = postop_state.MEM[ memory_location ] == preop_state.REG_UINT8[ self.r1 ]
		R1_is_R1 = postop_state.REG_UINT8[ self.r1 ] ==  preop_state.REG_UINT8[ self.r1 ]

		assert MEM_is_R1, f'M\' =/= {U8.to_string(self.r1)}'
		assert R1_is_R1, f'{U8.to_string(self.r1)}\' =/= {U8.to_string(self.r1)}'



class MVI_Reg_Imm(Op):	
	def __init__(self, code: bytes, r1: int):
			comment_string = f'\t\t; {U8.to_string(r1)} := data:{0}'
			super().__init__(code, 'mvi', [U8.to_string(r1), '{0}'], [1], comment_string)
			self.r1 = r1

	def step(self, state: State):
		data_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		state.REG_UINT8[ self.r1 ] = data_from_rom
		# for an immediate value, we need to increment the PC by one, again
		# so we start executing the next opcode, not the data, on the next cycle.
		state.REG_UINT16[ U16.PC ] += 0x01

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]

		REG_is_ROM = postop_state.REG_UINT8[ self.r1 ] == preop_state.MEM[preop_PC + 1]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x02

		assert REG_is_ROM, f'{U8.to_string(self.r1)}\' =/= MEM[PC + 1]'
		assert PC_has_incremented, f'PC\' =/= PC + 0x2'


class MVI_Mem_Imm(Op):	
	def __init__(self, code: bytes):
			comment_string = f'\t\t; (HL) := data:{0}'
			super().__init__(code, 'mvi', ['M', '{0}'], [1], comment_string)

	def step(self, state: State):
		memory_location = self.subop_addr_from_HL(state)
		data_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		state.MEM[memory_location] = data_from_rom
		# for an immediate value, we need to increment the PC by one, again
		# so we start executing the next opcode, not the data, on the next cycle.
		state.REG_UINT16[ U16.PC ] += 0x01

	def test(self, preop_state: State, postop_state: State):
		memory_location = self.subop_addr_from_HL(preop_state)
		preop_PC = preop_state.REG_UINT16[ U16.PC ]

		MEM_is_ROM = postop_state.MEM[ memory_location ] == preop_state.MEM[preop_PC + 1]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x02

		assert MEM_is_ROM, f'MEM\' =/= MEM[PC + 1]'
		assert PC_has_incremented, f'PC\' =/= PC + 0x2'




class LXI_Reg_Imm(Op):
	def __init__(self, code : bytes, rh : int, rl : int):
		comment = f'\t\t; {U8.to_string(rh)} := data:{1}; {U8.to_string(rl)} := data:{0}'
		super().__init__(code, 'lxi', [U8.to_string(rh), '{1}{0}'], [1,1], comment)
		self.rh = rh
		self.rl = rl

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]

		state.REG_UINT8[ self.rl ] = low_byte_from_rom
		state.REG_UINT8[ self.rh ] = high_byte_from_rom

		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]

		RH_is_high_byte = postop_state.REG_UINT8[ self.rh ] == high_byte_from_rom
		RL_is_low_byte = postop_state.REG_UINT8[ self.rl ] == low_byte_from_rom
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert RH_is_high_byte, f'{U8.to_string(self.rh)}\' =/= MEM[PC + 2]'
		assert RL_is_low_byte, f'{U8.to_string(self.rl)}\' =/= MEM[PC + 1]'
		assert PC_has_incremented, f'PC\' =/= PC + 3'



class LXI_SP(Op):
	def __init__(self, code: int):
		comment = '\t\t; SP[8:16] := data:{1}; SP[0:8] := data:{0}'
		super().__init__(code, 'lxi', ['SP', '{1}{0}'], [1,1], comment)

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]

		data = (high_byte_from_rom << 8) | low_byte_from_rom
		state.REG_UINT16[ U16.SP ] = data

		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		data = (high_byte_from_rom << 8) | low_byte_from_rom

		SP_is_ROM = postop_state.REG_UINT16[U16.SP] == data
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert SP_is_ROM, f'SP\' =/= MEM[PC+1 : PC+2]'
		assert PC_has_incremented, f'PC\' =/= PC + 3'










