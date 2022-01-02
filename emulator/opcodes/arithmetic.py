import numpy as np

from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


# ADD GROUP ======

class ADD_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t; A := {U8.to_string(r)} + A'
		super().__init__(code, 'add', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_add(state.REG_UINT8[ U8.A ], state.REG_UINT8[ self.r ])
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
		result = self.subop_add(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) + int(preop_state.REG_UINT8[U8.A])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A + MEM'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ADC_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t; A := A + {U8.to_string(r)} + CY'
		super().__init__(code, 'adc', [f'{U8.to_string(r)}'], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_add(state.REG_UINT8[ U8.A ], state.REG_UINT8[ self.r ], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[self.r]) + int(preop_state.REG_UINT8[U8.A]) + int(preop_state.FLAGS[F.CY])
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
		result = self.subop_add(state.REG_UINT8[ U8.A ], state.MEM[ addr ], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) + int(preop_state.REG_UINT8[U8.A]) + int(preop_state.FLAGS[F.CY])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A + MEM + CY (== {preop_state.FLAGS[F.CY]})'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ADI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A + data:{0} (add immediate)'
		super().__init__(code, 'adi', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_add(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) + int(preop_state.MEM[data_pointer])

		A_is_sum = postop_state.REG_UINT8[U8.A] == (data & 0xFF)
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A + MEM[PC + 1]'
		assert PC_has_incremented, 'PC\' =/= PC + 2'


class ACI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A + data:{0} + CY (add immediate)'
		super().__init__(code, 'aci', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_add(state.REG_UINT8[U8.A], state.MEM[ data_pointer ], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) + int(preop_state.MEM[data_pointer]) + int(preop_state.FLAGS[F.CY])

		A_is_sum = postop_state.REG_UINT8[U8.A] == (data & 0xFF)
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A + MEM[PC + 1] + CY'
		assert PC_has_incremented, 'PC\' =/= PC + 2'



# SUBTRACT GROUP ======


class SUB_Reg(Op):
	def __init__(self, code: bytes, r: int):

		comment_string = f'\t\t; A := {U8.to_string(r)} - A'
		super().__init__(code, 'sub', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_sub(state.REG_UINT8[U8.A], state.REG_UINT8[self.r])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.REG_UINT8[self.r])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		R_invariant = self.r == U8.A or preop_state.REG_UINT8[self.r] == postop_state.REG_UINT8[self.r]
		
		assert A_is_sum, f'A\' =/= A - {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class SUB_Mem(Op):
	def __init__(self, code: bytes):

		comment_string = f'\t\t; A := A - (H)(L) '
		super().__init__(code, 'sub', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.MEM[addr])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A - MEM'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class SBB_Reg(Op):
	def __init__(self, code: bytes, r: int):

		comment_string = f'\t\t; A := A - {U8.to_string(r)} - CY'
		super().__init__(code, 'sbb', [f'{U8.to_string(r)}'], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_sub(state.REG_UINT8[ U8.A ], state.REG_UINT8[ self.r ], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.REG_UINT8[self.r]) - int(preop_state.FLAGS[F.CY])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		R_invariant = self.r == U8.A or preop_state.REG_UINT8[self.r] == postop_state.REG_UINT8[self.r]
		
		assert A_is_sum, f'A\' =/= A - {U8.to_string(self.r)} - CY (== {preop_state.FLAGS[F.CY]})'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'

class SBB_Mem(Op):
	def __init__(self, code: bytes):

		comment_string = f'\t\t; A := A - (HL) - CY'
		super().__init__(code, 'sbb', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[addr], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.MEM[addr]) - int(preop_state.FLAGS[F.CY])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result & 0xFF
		
		assert A_is_sum, f'A\' =/= A - MEM - CY (== {preop_state.FLAGS[F.CY]})'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class SUI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A - data:{0} (sub immediate)'
		super().__init__(code, 'sui', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.MEM[data_pointer])

		A_is_sum = postop_state.REG_UINT8[U8.A] == (data & 0xFF)
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A - MEM[PC + 1]'
		assert PC_has_incremented, 'PC\' =/= PC + 2'


class SBI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A - data:{0} - CY (add immediate)'
		super().__init__(code, 'sbi', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[ data_pointer ], state.FLAGS[F.CY])
		self.subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) - int(preop_state.MEM[data_pointer]) - int(preop_state.FLAGS[F.CY])

		A_is_sum = postop_state.REG_UINT8[U8.A] == (data & 0xFF)
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A - MEM[PC + 1] - CY'
		assert PC_has_incremented, 'PC\' =/= PC + 2'


class INR_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t\t; {U8.to_string(r)} := {U8.to_string(r)} + 1; set flags Z, S, P, AC'
		super().__init__(code, 'inr', [f'{U8.to_string(r)}'], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_add(state.REG_UINT8[self.r], 1)
		self.subop_setflags_add(result, state, CY=False)
		state.REG_UINT8[ self.r ] = result & 0xFF

	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[self.r]) + 1
		R_is_R_plus_1 = postop_state.REG_UINT8[self.r] == (result & 0xFF)
		
		assert R_is_R_plus_1, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)} + 1'


class INR_Mem(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t\t; (HL) := (HL) + 1; set flags Z, S, P, AC'
		super().__init__(code, 'inr', [f'M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_add(state.MEM[addr], 1)
		self.subop_setflags_add(result, state, CY=False)
		state.MEM[ addr ] = result & 0xFF

	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) + 1
		MEM_is_MEM_plus_1 = postop_state.MEM[addr] == (result & 0xFF)
		
		assert MEM_is_MEM_plus_1, f'MEM[addr]\' =/= MEM[addr] + 1'


class DCR_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t\t; {U8.to_string(r)} := {U8.to_string(r)} - 1; set flags Z, S, P, AC'
		super().__init__(code, 'dcr', [f'{U8.to_string(r)}'], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_sub(state.REG_UINT8[self.r], 1)
		self.subop_setflags_add(result, state, CY=False)
		state.REG_UINT8[ self.r ] = result & 0xFF

	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[self.r]) - 1
		R_is_R_sub_1 = postop_state.REG_UINT8[self.r] == (result & 0xFF)
		
		assert R_is_R_sub_1, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)} - 1'


class DCR_Mem(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t\t; (HL) := (HL) - 1; set flags Z, S, P, AC'
		super().__init__(code, 'dcr', [f'M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_sub(state.MEM[addr], 1)
		self.subop_setflags_add(result, state, CY=False)
		state.MEM[ addr ] = result & 0xFF

	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) - 1
		MEM_is_MEM_plus_1 = postop_state.MEM[addr] == (result & 0xFF)
		
		assert MEM_is_MEM_plus_1, f'MEM[addr]\' =/= MEM[addr] - 1'


class INX_Reg(Op):
	def __init__(self, code: bytes, rh: int, rl: int):
		comment_string = f'\t\t\t; ({U8.to_string(rh)}{U8.to_string(rl)}) = ({U8.to_string(rh)}{U8.to_string(rl)}) + 1; no flags set.'
		super().__init__(code, 'inx', [f'{U8.to_string(rh)}'], [], comment_string)
		self.rh = rh
		self.rl = rl

	def step(self, state: State):
		value = self.subop_u8_pair_to_u16(state.REG_UINT8[self.rh], state.REG_UINT8[self.rl])
		result = self.subop_add(value, 1)
		val_h, val_l = self.subop_u16_to_u8_pair(result)
		state.REG_UINT8[ self.rh ] = val_h & 0xFF
		state.REG_UINT8[ self.rl ] = val_l & 0xFF

	def test(self, preop_state: State, postop_state: State):
		value = self.subop_u8_pair_to_u16(preop_state.REG_UINT8[self.rh], preop_state.REG_UINT8[self.rl])
		result = int(value) + 1
		val_h = result >> 8
		val_l = result & 0xFF

		RH_is_high_byte = postop_state.REG_UINT8[self.rh] == val_h 
		RL_is_low_byte = postop_state.REG_UINT8[self.rl] == val_l

		
		assert RH_is_high_byte, f'{U8.to_string(self.rh)}{U8.to_string(self.rl)}\' =/= {U8.to_string(self.rh)}{U8.to_string(self.rl)} + 1'
		assert RL_is_low_byte, f'{U8.to_string(self.rh)}{U8.to_string(self.rl)}\' =/= {U8.to_string(self.rh)}{U8.to_string(self.rl)} + 1'
	

class INX_SP(Op):
	def __init__(self, code: bytes ):
		comment_string = f'\t\t\t; (SP) = (SP) + 1; no flags set.'
		super().__init__(code, 'inx', [f'SP'], [], comment_string)

	def step(self, state: State):
		print(state.REG_UINT16[U16.SP])
		result = self.subop_add(state.REG_UINT16[U16.SP], 1)
		state.REG_UINT16[ U16.SP ] = result & 0xFFFF

	def test(self, preop_state: State, postop_state: State):
		SP_has_incremented = postop_state.REG_UINT16[U16.SP] == ((preop_state.REG_UINT16[U16.SP] + 1) & 0xFFFF)
		assert SP_has_incremented, f'SP\' =/= SP + 1'
		

class DCX_Reg(Op):
	def __init__(self, code: bytes, rh: int, rl: int):
		comment_string = f'\t\t\t; ({U8.to_string(rh)}{U8.to_string(rl)}) = ({U8.to_string(rh)}{U8.to_string(rl)}) - 1; no flags set.'
		super().__init__(code, 'dcx', [f'{U8.to_string(rh)}'], [], comment_string)
		self.rh = rh
		self.rl = rl

	def step(self, state: State):
		value = self.subop_u8_pair_to_u16(state.REG_UINT8[self.rh], state.REG_UINT8[self.rl])
		result = self.subop_sub(value, 1)
		val_h, val_l = self.subop_u16_to_u8_pair(result)
		state.REG_UINT8[ self.rh ] = val_h & 0xFF
		state.REG_UINT8[ self.rl ] = val_l & 0xFF

	def test(self, preop_state: State, postop_state: State):
		value = self.subop_u8_pair_to_u16(preop_state.REG_UINT8[self.rh], preop_state.REG_UINT8[self.rl])
		result = int(value) - 1
		val_h = result >> 8
		val_l = result & 0xFF

		RH_is_high_byte = postop_state.REG_UINT8[self.rh] == val_h 
		RL_is_low_byte = postop_state.REG_UINT8[self.rl] == val_l

		
		assert RH_is_high_byte, f'{U8.to_string(self.rh)}{U8.to_string(self.rl)}\' =/= {U8.to_string(self.rh)}{U8.to_string(self.rl)} - 1'
		assert RL_is_low_byte, f'{U8.to_string(self.rh)}{U8.to_string(self.rl)}\' =/= {U8.to_string(self.rh)}{U8.to_string(self.rl)} - 1'
	

class DCX_SP(Op):
	def __init__(self, code: bytes ):
		comment_string = f'\t\t\t; (SP) = (SP) - 1; no flags set.'
		super().__init__(code, 'dcx', [f'SP'], [], comment_string)

	def step(self, state: State):
		print(state.REG_UINT16[U16.SP])
		result = self.subop_sub(state.REG_UINT16[U16.SP], 1)
		state.REG_UINT16[ U16.SP ] = result & 0xFFFF

	def test(self, preop_state: State, postop_state: State):
		SP_has_incremented = postop_state.REG_UINT16[U16.SP] == ((preop_state.REG_UINT16[U16.SP] - 1) & 0xFFFF)
		assert SP_has_incremented, f'SP\' =/= SP + 1'
		


