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


class PUSH_Reg(Op):
	def __init__(self, code: bytes, rh: int, rl: int):
		comment_string = f'\t\t; (SP - 1) = {U8.to_string(rh)}; (SP - 2) = {U8.to_string(rl)}; SP = SP - 2'
		super().__init__(code, 'push', [f'{U8.to_string(rh)}'], [], comment_string)
		self.rh = rh
		self.rl = rl

	def step(self, state: State):
		SP = state.REG_UINT16[U16.SP]
		state.MEM[SP - 0x1] = state.REG_UINT8[self.rh]
		state.MEM[SP - 0x2] = state.REG_UINT8[self.rl]
		state.REG_UINT16[U16.SP] -= 0x2

	def test(self, preop_state: State, postop_state: State):
		SP = preop_state.REG_UINT16[U16.SP]

		SP_is_rh = postop_state.MEM[SP - 0x1] == preop_state.REG_UINT8[self.rh]
		SP_is_rl = postop_state.MEM[SP - 0x2] == preop_state.REG_UINT8[self.rl]
		SP_has_decremented = postop_state.REG_UINT16[U16.SP] == SP - 0x2

		assert SP_is_rh, f'MEM\'[SP - 1] =/= {U8.to_string(self.rh)}'
		assert SP_is_rl, f'MEM\'[SP - 2] =/= {U8.to_string(self.rl)}'
		assert SP_has_decremented, 'SP\' =/= SP - 2'


class PUSH_PSW(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; (SP - 1) := A; (SP - 2) := FLAGS; SP := SP - 2'
		super().__init__(code, 'push', [f'PSW'], [], comment_string)

	def step(self, state: State):
		SP = state.REG_UINT16[U16.SP]
		psw = self.subop_get_processor_status_word(state)
		state.MEM[SP - 0x1] = state.REG_UINT8[U8.A]
		state.MEM[SP - 0x2] = psw
		state.REG_UINT16[U16.SP] -= 0x2


	def test(self, preop_state: State, postop_state: State):
		SP = preop_state.REG_UINT16[U16.SP]
		PSW = self.subop_get_processor_status_word(preop_state)
		SP_is_A = postop_state.MEM[SP - 0x1] == preop_state.REG_UINT8[U8.A]
		SP_is_PSW = postop_state.MEM[SP - 0x2] == PSW
		SP_has_decremented = postop_state.REG_UINT16[U16.SP] == SP - 0x2

		assert SP_is_A, f'MEM\'[SP - 1] =/= A'
		assert SP_is_PSW, f'MEM\'[SP - 2] =/= PSW'
		assert SP_has_decremented, 'SP\' =/= SP - 2'


class POP_Reg(Op):
	def __init__(self, code: bytes, rh: int, rl: int):
		comment_string = f'\t\t;  {U8.to_string(rh)} = (SP + 1); {U8.to_string(rl)} = SP; SP = SP + 2'
		super().__init__(code, 'pop', [f'{U8.to_string(rh)}'], [], comment_string)
		self.rh = rh
		self.rl = rl

	def step(self, state: State):
		SP = state.REG_UINT16[U16.SP]
		state.REG_UINT8[self.rh] = state.MEM[SP + 0x1]
		state.REG_UINT8[self.rl] = state.MEM[SP]
		state.REG_UINT16[U16.SP] += 0x2

	def test(self, preop_state: State, postop_state: State):
		SP = preop_state.REG_UINT16[U16.SP]

		SP_is_rh = postop_state.REG_UINT8[self.rh] == preop_state.MEM[SP + 0x1]
		SP_is_rl = postop_state.REG_UINT8[self.rl] == preop_state.MEM[SP]
		SP_has_incremented = postop_state.REG_UINT16[U16.SP] == SP + 0x2

		assert SP_is_rh, f'{U8.to_string(self.rh)}\' =/= MEM[SP - 1]'
		assert SP_is_rl, f'{U8.to_string(self.rl)}\' =/= MEM[SP - 2]'
		assert SP_has_incremented, 'SP\' =/= SP + 2'


class POP_PSW(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; (SP - 1) := A; (SP - 2) := FLAGS; SP := SP - 2'
		super().__init__(code, 'pop', [f'PSW'], [], comment_string)

	def step(self, state: State):
		SP = state.REG_UINT16[U16.SP]
		PSW = state.MEM[ SP ]
		A = state.MEM[ SP + 0x1 ]

		state.REG_UINT8[U8.A] = A
		self.subop_set_processor_status_word(PSW, state)
		state.REG_UINT16[U16.SP] += 0x2

	def test(self, preop_state: State, postop_state: State):
		SP = preop_state.REG_UINT16[U16.SP]
		PSW = self.subop_get_processor_status_word(postop_state)

		# print(f'MEM: {bin((preop_state.MEM[SP] & 0xD7) | 0x2)}')
		# print(f'PSW: {bin(PSW)}')

		SP_is_A = preop_state.MEM[SP + 0x1] == postop_state.REG_UINT8[U8.A]
		SP_is_PSW = (preop_state.MEM[SP] & 0xD7) | 0x2 == PSW
		SP_has_incremented = postop_state.REG_UINT16[U16.SP] == SP + 0x2

		assert SP_is_A, f'A\' =/= MEM[SP - 1]'
		assert SP_is_PSW, f'PSW\' =/= MEM[SP]'
		assert SP_has_incremented, 'SP\' =/= SP + 2'


class XTHL(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; H <=> (SP); L <=> (SP+1)'
		super().__init__(code, 'xthl', [], [], comment_string)

	def step(self, state: State):
		H = state.REG_UINT8[U8.H]
		L = state.REG_UINT8[U8.L]
		SP = state.REG_UINT16[U16.SP]

		state.REG_UINT8[U8.L] = state.MEM[SP]
		state.REG_UINT8[U8.H] = state.MEM[SP + 0x1]
		state.MEM[SP] = L
		state.MEM[SP + 0x1] = H

	def test(self, preop_state: State, postop_state: State):
		SP = preop_state.REG_UINT16[U16.SP]

		H_is_SP_plus_1 = postop_state.REG_UINT8[U8.H] == preop_state.MEM[SP + 0x1]
		L_is_SP = postop_state.REG_UINT8[U8.L] == preop_state.MEM[SP]
		SP_plus_1_is_H = postop_state.MEM[SP + 0x1] == preop_state.REG_UINT8[U8.H]
		SP_is_L = postop_state.MEM[SP] == preop_state.REG_UINT8[U8.L]

		assert H_is_SP_plus_1, 'H\' =/= MEM[SP+1]'
		assert L_is_SP, 'L\' =/= MEM[SP]'
		assert SP_plus_1_is_H, 'MEM\'[SP+1] =/= H'
		assert SP_is_L, 'MEM\'[SP] = L'


class SPHL(Op):
	def __init__(self, code: bytes):
		comment_string = f'\t\t; H <=> (SP); L <=> (SP+1)'
		super().__init__(code, 'sphl', [], [], comment_string)

	def step(self, state: State):
		addr = self.subop_addr_from_HL(state)
		state.REG_UINT16[U16.SP] = addr


	def test(self, preop_state: State, postop_state: State):
		addr = (preop_state.REG_UINT8[U8.H] << 8) | preop_state.REG_UINT8[U8.L]

		SP_has_jumped = postop_state.REG_UINT16[U16.SP] == addr

		assert SP_has_jumped, 'SP\' =/= (HL)'


class IN_Imm(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; A := (data bus):{0}'
		super().__init__(code, 'in', ['{0}'], [1], comment_string)

	def step(self, state: State):
		...

	def test(self, preop_state: State, postop_state: State):
		# Note(Nic): input from peripherals is not yet implemented 
		# on this emulator...
		assert True


class OUT_Imm(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; (data bus):{0} := A'
		super().__init__(code, 'out', ['{0}'], [1], comment_string)

	def step(self, state: State):
		...

	def test(self, preop_state: State, postop_state: State):
		# Note(Nic): input from peripherals is not yet implemented 
		# on this emulator...
		assert True


class DI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; disable interrupts'
		super().__init__(code, 'di', [], [], comment_string)

	def step(self, state: State):
		state.FLAGS[F.DI] = True

	def test(self, preop_state: State, postop_state: State):
		# Note(Nic): Nothing really to test here, just sets a status flag
		assert postop_state.FLAGS[F.DI]


class EI(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; enable interrupts'
		super().__init__(code, 'ei', [], [], comment_string)

	def step(self, state: State):
		state.FLAGS[F.DI] = False

	def test(self, preop_state: State, postop_state: State):
		# Note(Nic): Nothing really to test here, just sets a status flag
		assert not postop_state.FLAGS[F.DI]


class HLT(Op):
	def __init__(self, code: bytes):
		comment_string = '\t\t; halts processor'
		super().__init__(code, 'hlt', [], [], comment_string)

	def step(self, state: State):
		state.FLAGS[F.E] = False

	def test(self, preop_state: State, postop_state: State):
		# Note(Nic): Nothing really to test here, just sets a status flag
		assert not postop_state.FLAGS[F.E]



