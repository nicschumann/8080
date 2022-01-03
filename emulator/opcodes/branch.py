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
			assert PC_has_incremented, f'[no-jmp] PC\' =/= PC + 2'


class CCOND_Imm(Op):
	def __init__(self, code: bytes, name: str, predicate):
		comment_string = '\t\t; PC := {1}{0}'
		super().__init__(code, name, ['{1}{0}'], [1,1], comment_string)
		self.predicate = predicate 

	def step(self, state: State):
		if self.predicate(state.FLAGS):
			PC = state.REG_UINT16[U16.PC]
			SP = state.REG_UINT16[U16.SP]

			# the address of the next instruction 
			# is pushed onto the stack.
			PCH, PCL = self.subop_u16_to_u8_pair(PC + 0x2)
			state.MEM[ SP - 0x1 ] = PCH
			state.MEM[ SP - 0x2 ] = PCL
			state.REG_UINT16[U16.SP] -= 0x2

			addr_low_byte = state.MEM[ PC ]
			addr_high_byte = state.MEM[ PC + 0x1 ]
			addr = self.subop_u8_pair_to_u16(addr_high_byte, addr_low_byte)
			state.REG_UINT16[ U16.PC ] = addr 
		
		else:
			state.REG_UINT16[U16.PC] += 0x2

	def test(self, preop_state: State, postop_state: State):
		if self.predicate(preop_state.FLAGS):
			PC = preop_state.REG_UINT16[U16.PC]
			PC_prime = postop_state.REG_UINT16[U16.PC]
			SP = preop_state.REG_UINT16[U16.SP]
			SP_prime = postop_state.REG_UINT16[U16.SP]

			addr = (preop_state.MEM[PC + 0x2] << 8) | preop_state.MEM[PC + 0x1]
			PCH = (PC + 0x3) >> 8
			PCL = (PC + 0x3) & 0xFF

			PC_has_jumped = postop_state.REG_UINT16[U16.PC] == addr
			Stack_contains_PC_high = postop_state.MEM[SP - 0x1] == PCH
			Stack_contains_PC_low = postop_state.MEM[SP - 0x2] == PCL
			SP_has_decremented = postop_state.REG_UINT16[U16.SP] == SP - 0x2

			assert PC_has_jumped, f'PC\' =/= data:{addr}'
			assert Stack_contains_PC_high, f'MEM\'[SP - 1] =/= SP[7:0]'
			assert Stack_contains_PC_low, f'MEM\'[SP - 2] =/= SP[15:8]'
			assert SP_has_decremented, f'SP\' =/= SP - 2'

		else:
			PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x03
			assert PC_has_incremented, f'PC\' =/= PC + 3'


class RCOND(Op):
	def __init__(self, code: bytes, name: str, predicate):
		comment_string = '\t\t; PC := {1}{0}'
		super().__init__(code, name, ['{1}{0}'], [1,1], comment_string)
		self.predicate = predicate 

	def step(self, state: State):
		if self.predicate(state.FLAGS):
			PCL = state.MEM[ state.REG_UINT16[U16.SP] ]
			PCH = state.MEM[ state.REG_UINT16[U16.SP] + 0x1 ]
			PC = self.subop_u8_pair_to_u16(PCH, PCL)

			state.REG_UINT16[U16.PC] = PC
			state.REG_UINT16[U16.SP] += 0x2


	def test(self, preop_state: State, postop_state: State):
		if self.predicate(preop_state.FLAGS):
			PC = preop_state.REG_UINT16[U16.PC]
			SP = preop_state.REG_UINT16[U16.SP]

			PC_prime_L = preop_state.MEM[SP]
			PC_prime_H = preop_state.MEM[SP + 0x1]
			PC_prime = (PC_prime_H << 8) | PC_prime_L

			PC_has_returned = postop_state.REG_UINT16[U16.PC] == PC_prime
			SP_has_incremented = postop_state.REG_UINT16[U16.SP] == SP + 0x2

			assert PC_has_returned, 'PC\' =/= MEM[SP + 1]|MEM[SP]'
			assert SP_has_incremented, 'SP\' =/= SP + 2'

		else:
			PC_has_incremented = postop_state.REG_UINT16[U16.PC] == preop_state.REG_UINT16[U16.PC] + 0x01
			assert PC_has_incremented, f'PC\' =/= PC + 3'



class RST(Op):
	def __init__(self, code: bytes):
		data = code & 0x38 # 0b00111000 ; this is the addr of the new PC
		comment_code = data >> 3
		comment_string = f'\t\t; PC := {hex(data)} (addr #{comment_code})'
		super().__init__(code, 'rst', [f'#{comment_code}'], [1,1], comment_string)
		self.addr = data

	def step(self, state: State):
		SP = state.REG_UINT16[U16.SP]
		PCH, PCL = self.subop_u16_to_u8_pair(state.REG_UINT16[U16.PC])
		state.MEM[SP - 0x1] = PCH
		state.MEM[SP - 0x2] = PCL
		state.REG_UINT16[U16.SP] -= 0x2
		state.REG_UINT16[U16.PC] = self.addr


	def test(self, preop_state: State, postop_state: State):
		PC = preop_state.REG_UINT16[U16.PC]
		SP = preop_state.REG_UINT16[U16.SP]
		PCL = (PC + 0x1) & 0xFF
		PCH = (PC + 0x1) >> 8

		PC_has_jumped = postop_state.REG_UINT16[U16.PC] == self.addr
		PCL_is_on_stack = postop_state.MEM[SP - 0x2] == PCL
		PCH_is_on_stack = postop_state.MEM[SP - 0x1] == PCH
		SP_has_decremented = postop_state.REG_UINT16[U16.SP] == SP - 0x2

		assert PC_has_jumped, f'PC\' =/= {self.addr}'
		assert PCL_is_on_stack, f'SP\'[SP - 2] =/= PC[7:0]'
		assert PCH_is_on_stack, f'SP\'[SP - 1] =/= PC[15:8]'
		assert SP_has_decremented, 'SP\' =/= SP - 2'


