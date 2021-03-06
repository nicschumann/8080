import numpy as np

from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .abstract import Op


# ANA GROUP ======


class ANA_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t; A := {U8.to_string(r)} & A; CY is cleared'
		super().__init__(code, 'ana', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_and(state.REG_UINT8[U8.A], state.REG_UINT8[self.r])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.REG_UINT8[U8.A] = result


	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[U8.A]) & int(preop_state.REG_UINT8[self.r]) 
		A_is_and = postop_state.REG_UINT8[U8.A] == result
		R_invariant = postop_state.REG_UINT8[self.r] == preop_state.REG_UINT8[self.r]	
		
		assert A_is_and, f'A\' =/= A & {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ANA_Mem(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; A := A & (H)(L) '
		super().__init__(code, 'ana', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_and(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.REG_UINT8[ U8.A ] = result


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) & int(preop_state.REG_UINT8[U8.A])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result
		
		assert A_is_sum, f'A\' =/= A & MEM'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ANI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; A := A & data:{0}; set flags Z, S, P, CY, AC'
		super().__init__(code, 'ani', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_and(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[ U8.A ] = result
		state.REG_UINT16[U16.PC] += 0x1


	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) & int(preop_state.MEM[data_pointer])

		A_is_sum = postop_state.REG_UINT8[U8.A] == data
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A & MEM[PC + 1]'
		assert PC_has_incremented, 'PC\' =/= PC + 2'
		

class XRA_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t; A := {U8.to_string(r)} ^ A; AC and CY is cleared'
		super().__init__(code, 'xra', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_xor(state.REG_UINT8[U8.A], state.REG_UINT8[self.r])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[U8.A] = result


	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[U8.A]) ^ int(preop_state.REG_UINT8[self.r]) 
		A_is_and = postop_state.REG_UINT8[U8.A] == result
		R_invariant = self.r == U8.A or postop_state.REG_UINT8[self.r] == preop_state.REG_UINT8[self.r]	
		
		assert A_is_and, f'A\' =/= A ^ {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class XRA_Mem(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; A := A ^ (H)(L); AC and CY is cleared'
		super().__init__(code, 'xra', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_xor(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[ U8.A ] = result


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) ^ int(preop_state.REG_UINT8[U8.A])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result
		
		assert A_is_sum, f'A\' =/= A ^ MEM'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class XRI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; A := A ^ data:{0}; clear CY and AC'
		super().__init__(code, 'xri', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_xor(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[ U8.A ] = result
		state.REG_UINT16[U16.PC] += 0x1


	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) ^ int(preop_state.MEM[data_pointer])

		A_is_sum = postop_state.REG_UINT8[U8.A] == data
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A ^ MEM[PC + 1]'
		assert PC_has_incremented, 'PC\' =/= PC + 2'


class ORA_Reg(Op):
	def __init__(self, code: bytes, r: int):
		comment_string = f'\t\t; A := {U8.to_string(r)} | A; AC and CY is cleared'
		super().__init__(code, 'ora', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_or(state.REG_UINT8[U8.A], state.REG_UINT8[self.r])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[U8.A] = result


	def test(self, preop_state: State, postop_state: State):
		result = int(preop_state.REG_UINT8[U8.A]) | int(preop_state.REG_UINT8[self.r]) 
		A_is_and = postop_state.REG_UINT8[U8.A] == result
		R_invariant = self.r == U8.A or postop_state.REG_UINT8[self.r] == preop_state.REG_UINT8[self.r]	
		
		assert A_is_and, f'A\' =/= A | {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ORA_Mem(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; A := A | (H)(L); AC and CY is cleared'
		super().__init__(code, 'ora', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_or(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[ U8.A ] = result


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		result = int(preop_state.MEM[addr]) | int(preop_state.REG_UINT8[U8.A])
		A_is_sum = postop_state.REG_UINT8[U8.A] == result
		
		assert A_is_sum, f'A\' =/= A | MEM'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class ORI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; A := A | data:{0}; clear CY and AC'
		super().__init__(code, 'ori', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_or(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.FLAGS[F.CY] = False
		state.FLAGS[F.AC] = False
		state.REG_UINT8[ U8.A ] = result
		state.REG_UINT16[U16.PC] += 0x1


	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		data = int(preop_state.REG_UINT8[U8.A]) | int(preop_state.MEM[data_pointer])

		A_is_sum = postop_state.REG_UINT8[U8.A] == data
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x2
		
		assert A_is_sum, f'A\' =/= A | MEM[PC + 1]'
		assert PC_has_incremented, 'PC\' =/= PC + 2'


		
class CMP_Reg(Op):
	def __init__(self, code: bytes, r: int):

		comment_string = f'\t\t; {U8.to_string(r)} - A; Z = 1 if A = {U8.to_string(r)}; CY = 1 if A < {U8.to_string(r)}'
		super().__init__(code, 'cmp', [U8.to_string(r)], [], comment_string)
		self.r = r

	def step(self, state: State):
		result = self.subop_sub(state.REG_UINT8[U8.A], state.REG_UINT8[self.r])
		self.subop_setflags_add(result, state)

	def test(self, preop_state: State, postop_state: State):		
		CY_is_set = postop_state.FLAGS[F.CY] == (preop_state.REG_UINT8[U8.A] < preop_state.REG_UINT8[self.r])
		Z_is_set = postop_state.FLAGS[F.Z] == (preop_state.REG_UINT8[U8.A] == preop_state.REG_UINT8[self.r])
		R_invariant = preop_state.REG_UINT8[self.r] == postop_state.REG_UINT8[self.r]
		
		assert CY_is_set, f'CY\' =/= A < {U8.to_string(self.r)}'
		assert Z_is_set, f'Z\' =/= A == {U8.to_string(self.r)}'
		assert R_invariant, f'{U8.to_string(self.r)}\' =/= {U8.to_string(self.r)}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class CMP_Mem(Op):
	def __init__(self, code: bytes):

		comment_string = f'\t\t; A - (H)(L); Z = 1 if A = (HL); CY = 1 if A < (HL)'
		super().__init__(code, 'cmp', ['M'], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[addr])
		self.subop_setflags_add(result, state)


	def test(self, preop_state: State, postop_state: State):
		addr = self.subop_addr_from_HL(preop_state)
		CY_is_set = postop_state.FLAGS[F.CY] == (preop_state.REG_UINT8[U8.A] < preop_state.MEM[addr])
		Z_is_set = postop_state.FLAGS[F.Z] == (preop_state.REG_UINT8[U8.A] == preop_state.MEM[addr])
		
		assert CY_is_set, f'CY\' =/= A:{preop_state.REG_UINT8[U8.A]} < MEM[addr]:{preop_state.MEM[addr]}'
		assert Z_is_set, f'Z\' =/= A:{preop_state.REG_UINT8[U8.A]} == MEM[addr]:{preop_state.MEM[addr]}'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class CPI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := A - data:{0} (sub immediate)'
		super().__init__(code, 'cpi', ['{0}'], [1], comment_string)

	def step(self, state: State):
		data_pointer = state.REG_UINT16[U16.PC]
		result = self.subop_sub(state.REG_UINT8[U8.A], state.MEM[ data_pointer ])
		self.subop_setflags_add(result, state)
		state.REG_UINT16[U16.PC] += 0x1

	def test(self, preop_state: State, postop_state: State):
		data_pointer = preop_state.REG_UINT16[U16.PC] + 0x1
		CY_is_set = postop_state.FLAGS[F.CY] == (preop_state.REG_UINT8[U8.A] < preop_state.MEM[data_pointer])
		Z_is_set = postop_state.FLAGS[F.Z] == (preop_state.REG_UINT8[U8.A] == preop_state.MEM[data_pointer])
		PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x02
		
		assert CY_is_set, f'CY\' =/= A:{preop_state.REG_UINT8[U8.A]} < data:{preop_state.MEM[data_pointer]}'
		assert Z_is_set, f'Z\' =/= A:{preop_state.REG_UINT8[U8.A]} == data:{preop_state.MEM[data_pointer]}'
		assert PC_has_incremented, f'PC\' == PC + 2'
		assert self.mem_invariant(preop_state, postop_state), 'MEM\' =/= MEM'


class RLC(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A_n+1 := A_n; A_0 = A_7; CY = A_7'
		super().__init__(code, 'rlc', [], [], comment_string)

	def step(self, state: State):
		value = state.REG_UINT8[U8.A]
		rot_value = (value << 1) & 0xFF
		new_carry = (value >> 7)
		new_value = rot_value | new_carry

		state.REG_UINT8[U8.A] = new_value
		state.FLAGS[F.CY] = new_carry


	def test(self, preop_state: State, postop_state: State):
		high_bit = preop_state.REG_UINT8[U8.A] >> 7
		A_rot = (preop_state.REG_UINT8[U8.A] << 1) & 0xFE

		A_is_rotated = A_rot == postop_state.REG_UINT8[U8.A] & 0xFE
		A_high_bit = high_bit == postop_state.REG_UINT8[U8.A] & 0x1
		CY_is_set = high_bit == postop_state.FLAGS[F.CY]

		assert A_is_rotated, 'A\'_n+1 == A_n'
		assert A_high_bit, 'A\'_0 == A_7'
		assert CY_is_set, 'CY\' =/= A_7'


class RRC(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A_n := A_n-1; A_7 = A_0; CY = A_0'
		super().__init__(code, 'rrc', [], [], comment_string)

	def step(self, state: State):
		value = state.REG_UINT8[U8.A]

		new_carry = value & 0x1
		new_value = (new_carry << 7) | (value >> 1)

		state.REG_UINT8[U8.A] = new_value
		state.FLAGS[F.CY] = new_carry


	def test(self, preop_state: State, postop_state: State):
		low_bit = preop_state.REG_UINT8[U8.A] & 0x1
		A_rot = (preop_state.REG_UINT8[U8.A] >> 1) & 0b01111111

		A_is_rotated = A_rot == postop_state.REG_UINT8[U8.A] & 0b01111111
		A_low_bit = low_bit == (postop_state.REG_UINT8[U8.A] >> 7)
		CY_is_set = low_bit == postop_state.FLAGS[F.CY]

		assert A_is_rotated, 'A\'_n == A_n-1'
		assert A_low_bit, 'A\'_7 == A_0'
		assert CY_is_set, 'CY\' =/= A_0'


class RAL(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A_n+1 := A_n; A_0 = CY; CY = A_7'
		super().__init__(code, 'ral', [], [], comment_string)

	def step(self, state: State):
		value = state.REG_UINT8[U8.A]
		old_carry = state.FLAGS[F.CY]

		rot_value = (value << 1) & 0xFF
		new_carry = (value >> 7)
		new_value = rot_value | old_carry

		state.REG_UINT8[U8.A] = new_value
		state.FLAGS[F.CY] = new_carry


	def test(self, preop_state: State, postop_state: State):
		high_bit = preop_state.REG_UINT8[U8.A] >> 7
		carry = preop_state.FLAGS[F.CY]
		A_rot = (preop_state.REG_UINT8[U8.A] << 1) & 0xFE

		A_is_rotated = A_rot == postop_state.REG_UINT8[U8.A] & 0xFE
		A_high_bit_is_CY = carry == postop_state.REG_UINT8[U8.A] & 0x1
		CY_is_set = high_bit == postop_state.FLAGS[F.CY]

		assert A_is_rotated, 'A\'_n+1 == A_n'
		assert A_high_bit_is_CY, 'A\'_0 == CY'
		assert CY_is_set, 'CY\' =/= A_7'


class RAR(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A_n := A_n-1; A_7 = CY; CY = A_0'
		super().__init__(code, 'rar', [], [], comment_string)

	def step(self, state: State):
		value = state.REG_UINT8[U8.A]
		old_carry = state.FLAGS[F.CY]

		new_carry = value & 0x1
		new_value = (old_carry << 7) | (value >> 1)

		state.REG_UINT8[U8.A] = new_value
		state.FLAGS[F.CY] = new_carry


	def test(self, preop_state: State, postop_state: State):
		low_bit = preop_state.REG_UINT8[U8.A] & 0x1
		carry = preop_state.FLAGS[F.CY]
		A_rot = (preop_state.REG_UINT8[U8.A] >> 1) & 0b01111111

		A_is_rotated = A_rot == postop_state.REG_UINT8[U8.A] & 0b01111111
		A_low_bit_is_CY = carry == (postop_state.REG_UINT8[U8.A] >> 7)
		CY_is_set = low_bit == postop_state.FLAGS[F.CY]

		assert A_is_rotated, 'A\'_n == A_n-1'
		assert A_low_bit_is_CY, 'A\'_7 == CY'
		assert CY_is_set, 'CY\' =/= A_0'


class CMA(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; A := ~A'
		super().__init__(code, 'cma', [], [], comment_string)

	def step(self, state: State):
		state.REG_UINT8[U8.A] = ~state.REG_UINT8[U8.A] & 0xFF


	def test(self, preop_state: State, postop_state: State):
		A_is_A_comp = ~preop_state.REG_UINT8[U8.A] & 0xFF == postop_state.REG_UINT8[U8.A]
		assert A_is_A_comp, 'A\' =/= ~A'


class CMC(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; CY := ~CY'
		super().__init__(code, 'cmc', [], [], comment_string)

	def step(self, state: State):
		state.FLAGS[F.CY] = not state.FLAGS[F.CY]


	def test(self, preop_state: State, postop_state: State):
		CY_is_CY_comp = (not preop_state.FLAGS[F.CY]) == postop_state.FLAGS[F.CY]
		assert CY_is_CY_comp, 'CY\' =/= ~CY'


class STC(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t\t; CY := 1'
		super().__init__(code, 'stc', [], [], comment_string)

	def step(self, state: State):
		state.FLAGS[F.CY] = True

	def test(self, preop_state: State, postop_state: State):
		CY_is_True = postop_state.FLAGS[F.CY]
		assert CY_is_True, 'CY\' =/= 1'
