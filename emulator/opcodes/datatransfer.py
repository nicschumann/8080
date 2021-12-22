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

		data = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)
		state.REG_UINT16[ U16.SP ] = data

		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		data = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		SP_is_ROM = postop_state.REG_UINT16[U16.SP] == data
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert SP_is_ROM, f'SP\' =/= MEM[PC+1 : PC+2]'
		assert PC_has_incremented, f'PC\' =/= PC + 3'


class LDA(Op):
	def __init__(self, code: int):
		comment = '\t\t; A := (addr:{1}{0})'
		super().__init__(code, 'lda', ['{1}{0}'], [1,1], comment)

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		state.REG_UINT8[ U8.A ] = state.MEM[ addr ]
		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		A_is_mem = postop_state.REG_UINT8[U8.A] == preop_state.MEM[addr]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert A_is_mem, f'A\' =/= MEM[addr]'
		assert PC_has_incremented, f'PC\' =/= PC + 3'


class STA(Op):
	def __init__(self, code: int):
		comment = '\t\t; (addr:{1}{0}) := A'
		super().__init__(code, 'sta', ['{1}{0}'], [1,1], comment)

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		state.MEM[ addr ] = state.REG_UINT8[ U8.A ]
		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		MEM_is_A = postop_state.MEM[addr] == preop_state.REG_UINT8[U8.A]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert MEM_is_A, f'MEM[addr]\' =/= A'
		assert PC_has_incremented, f'PC\' =/= PC + 3'
		



class SHLD(Op):
	def __init__(self, code: int):
		comment = '\t\t; (addr:{1}{0}) := L; (addr:{1}{0} + 1) := H'
		super().__init__(code, 'shld', ['{1}{0}'], [1,1], comment)

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		state.MEM[addr + 0x01] = state.REG_UINT8[U8.H]
		state.MEM[addr] = state.REG_UINT8[U8.L]

		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		L_is_addr = postop_state.MEM[addr] == preop_state.REG_UINT8[U8.L]
		H_is_addr_plus_1 = postop_state.MEM[addr + 0x01] == preop_state.REG_UINT8[U8.H]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert L_is_addr, 'MEM\'[addr] =/= L'
		assert H_is_addr_plus_1, 'MEM\'[addr+1] =/= H'
		assert PC_has_incremented, f'PC\' =/= PC + 3'


class LHLD(Op):
	def __init__(self, code: int):
		comment = '\t\t; L := (addr:{1}{0}); H := (addr:{1}{0} + 1)'
		super().__init__(code, 'lhld', ['{1}{0}'], [1,1], comment)

	def step(self, state: State):
		low_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] ]
		high_byte_from_rom = state.MEM[ state.REG_UINT16[ U16.PC ] + 0x01 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		state.REG_UINT8[U8.H] = state.MEM[addr + 0x01]
		state.REG_UINT8[U8.L] = state.MEM[addr]

		state.REG_UINT16[ U16.PC ] += 0x02

	def test(self, preop_state: State, postop_state: State):
		preop_PC = preop_state.REG_UINT16[ U16.PC ]
		low_byte_from_rom = preop_state.MEM[ preop_PC + 0x01 ]
		high_byte_from_rom = preop_state.MEM[ preop_PC + 0x02 ]
		addr = self.subop_u8_pair_to_u16(high_byte_from_rom, low_byte_from_rom)

		L_is_addr = postop_state.REG_UINT8[U8.L] == preop_state.MEM[addr]
		H_is_addr_plus_1 = postop_state.REG_UINT8[U8.H] == preop_state.MEM[addr + 0x01]
		PC_has_incremented = postop_state.REG_UINT16[ U16.PC ] == preop_PC + 0x03

		assert L_is_addr, 'L\' =/= MEM[addr]'
		assert H_is_addr_plus_1, 'H\' =/= MEM[addr+1]'
		assert PC_has_incremented, f'PC\' =/= PC + 3'


class LDAX_Reg(Op):
	def __init__(self, code: int, r1: int, r2: int):
		comment = f'\t\t\t; A := ({U8.to_string(r1)}{U8.to_string(r2)})'
		super().__init__(code, 'ldax', [f'{U8.to_string(r1)}'], [], comment)
		self.r1 = r1
		self.r2 = r2

	def step(self, state: State):
		low_byte_from_reg = state.REG_UINT8[self.r2]
		high_byte_from_reg = state.REG_UINT8[self.r1]
		addr = self.subop_u8_pair_to_u16(high_byte_from_reg, low_byte_from_reg)

		state.REG_UINT8[ U8.A ] = state.MEM[addr]

	def test(self, preop_state: State, postop_state: State):
		low_byte_from_reg = preop_state.REG_UINT8[self.r2]
		high_byte_from_reg = preop_state.REG_UINT8[self.r1]
		addr = self.subop_u8_pair_to_u16(high_byte_from_reg, low_byte_from_reg)

		A_is_MEM = postop_state.REG_UINT8[U8.A] == preop_state.MEM[addr]

		assert A_is_MEM, f'A\' =/= MEM[addr]'

class STAX_Reg(Op):
	def __init__(self, code: int, r1: int, r2: int):
		comment = f'\t\t\t; ({U8.to_string(r1)}{U8.to_string(r2)}) := A'
		super().__init__(code, 'stax', [f'{U8.to_string(r1)}'], [], comment)
		self.r1 = r1
		self.r2 = r2

	def step(self, state: State):
		low_byte_from_reg = state.REG_UINT8[self.r2]
		high_byte_from_reg = state.REG_UINT8[self.r1]
		addr = self.subop_u8_pair_to_u16(high_byte_from_reg, low_byte_from_reg)

		state.MEM[addr] = state.REG_UINT8[ U8.A ]

	def test(self, preop_state: State, postop_state: State):
		low_byte_from_reg = preop_state.REG_UINT8[self.r2]
		high_byte_from_reg = preop_state.REG_UINT8[self.r1]
		addr = self.subop_u8_pair_to_u16(high_byte_from_reg, low_byte_from_reg)

		MEM_is_A = postop_state.MEM[addr] == preop_state.REG_UINT8[U8.A]

		assert MEM_is_A, f'MEM[addr]\' =/= A'


class XCHG(Op):
	def __init__(self, code: int):
		comment = '\t\t\t; H <=> D, L <=> E'
		super().__init__(code, 'xchg', [], [], comment)

	def step(self, state: State):
		tmp_high = state.REG_UINT8[ U8.D ]
		tmp_low = state.REG_UINT8[ U8.E ]

		state.REG_UINT8[ U8.D ] = state.REG_UINT8[ U8.H ]
		state.REG_UINT8[ U8.E ] = state.REG_UINT8[ U8.L ]

		state.REG_UINT8[ U8.H ] = tmp_high
		state.REG_UINT8[ U8.L ] = tmp_low

	def test(self, preop_state: State, postop_state: State):
		H_is_now_D = postop_state.REG_UINT8[U8.H] == preop_state.REG_UINT8[U8.D]
		D_is_now_H = postop_state.REG_UINT8[U8.D] == preop_state.REG_UINT8[U8.H]

		L_is_now_E = postop_state.REG_UINT8[U8.L] == preop_state.REG_UINT8[U8.E]
		E_is_now_L = postop_state.REG_UINT8[U8.E] == preop_state.REG_UINT8[U8.L]

		assert H_is_now_D, 'H\' =/= D'
		assert D_is_now_H, 'D\' =/= H'
		assert L_is_now_E, 'L\' =/= E'
		assert E_is_now_L, 'E\' =/= L'







