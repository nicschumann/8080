import pytest
import numpy as np

from .state import State
from .state import Uint16Registers as U16
from .state import Uint8Registers as U8
from .state import FlagsRegisters as F

from .step import step


def get_initial_state():
	state = State()
	state.REG_UINT16[ U16.PC ] = 0x0
	state.REG_UINT8[ U8.A ] = 0x10
	state.REG_UINT8[ U8.B ] = 0x01
	state.REG_UINT8[ U8.C ] = 0x02
	state.REG_UINT8[ U8.D ] = 0x03
	state.REG_UINT8[ U8.E ] = 0x04
	state.REG_UINT8[ U8.H ] = 0x05
	state.REG_UINT8[ U8.L ] = 0x06

	return state


# ---------
# ADD
# ---------

@pytest.mark.parametrize(
	'opcode,register,val_1,val_2', 
	[
		(0x80, U8.B, 0x10, 0x10), 
		(0x81, U8.C, 0x10, 0x10),
		(0x82, U8.D, 0x10, 0x10),
		(0x83, U8.E, 0x10, 0x10),
		(0x84, U8.H, 0x10, 0x10),
		(0x85, U8.L, 0x10, 0x10),
		(0x87, U8.A, 0x10, 0x10) 
	]
)
def test_op_add_reg(opcode, register, val_1, val_2):
	initial_state = get_initial_state()
	opcodes_to_test = np.array([opcode])

	initial_state.REG_UINT8[ U8.A ] = val_1
	initial_state.REG_UINT8[ register ] = val_2
	initial_state.MEM[ :opcodes_to_test.shape[0] ] = opcodes_to_test
	
	state = initial_state.clone()
	step(state)

	A_is_sum_of_A_and_REG = state.REG_UINT8[ U8.A ] == initial_state.REG_UINT8[ U8.A ] + initial_state.REG_UINT8[ register ]
	PC_has_incremented = state.REG_UINT16[ U16.PC ] == initial_state.REG_UINT16[ U16.PC ] + 1
	REG_is_unchanged = (U8.A == register) or (state.REG_UINT8[ register ] == initial_state.REG_UINT8[ register ])
	MEM_is_unchanged = np.all(state.MEM == initial_state.MEM)


	assert A_is_sum_of_A_and_REG, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: A\' =/= A + REG' 	
	assert PC_has_incremented, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: PC\' =/= PC + 1' 
	assert REG_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: REG\' =/= REG' 
	assert MEM_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: MEM\' =/= MEM' 


def test_op_add_mem():
	initial_state = get_initial_state()
	opcodes_to_test = np.array([0x86])

	initial_state.REG_UINT8[ U8.H ] = 0x05
	initial_state.REG_UINT8[ U8.L ] = 0x06
	initial_state.MEM[ :opcodes_to_test.shape[0] ] = opcodes_to_test
	initial_state.MEM[ 0x0506 ] = 0x10

	state = initial_state.clone()
	step(state)

	A_is_sum_of_A_and_MEM = state.REG_UINT8[ U8.A ] == initial_state.REG_UINT8[ U8.A ] + initial_state.MEM[ 0x0506 ]
	PC_has_incremented = state.REG_UINT16[ U16.PC ] == initial_state.REG_UINT16[ U16.PC ] + 1
	MEM_is_unchanged = np.all(state.MEM == initial_state.MEM)

	assert A_is_sum_of_A_and_MEM, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: A\' =/= A + MEM' 	
	assert PC_has_incremented, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: PC\' =/= PC + 1' 
	assert MEM_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: MEM\' =/= MEM' 


# ---------
# ADC
# ---------

@pytest.mark.parametrize(
	'opcode,register,val_1,val_2,carry', 
	[
		(0x88, U8.B, 0x10, 0x10, True), 
		(0x89, U8.C, 0x10, 0x10, False),
		(0x8A, U8.D, 0x10, 0x10, True),
		(0x8B, U8.E, 0x10, 0x10, False),
		(0x8C, U8.H, 0x10, 0x10, True),
		(0x8D, U8.L, 0x10, 0x10, False),
		(0x8F, U8.A, 0x10, 0x10, True) 
	]
)
def test_op_adc_reg(opcode, register, val_1, val_2, carry):
	initial_state = get_initial_state()
	opcodes_to_test = np.array([opcode])
	initial_state.MEM[ :opcodes_to_test.shape[0] ] = opcodes_to_test
	initial_state.REG_UINT8[ U8.A ] = val_1
	initial_state.REG_UINT8[ register ] = val_2
	initial_state.FLAGS[ F.CY ] = carry
	
	state = initial_state.clone()
	step(state)

	A_is_sum_of_A_and_REG_and_CY = state.REG_UINT8[ U8.A ] == initial_state.REG_UINT8[ U8.A ] + initial_state.REG_UINT8[ register ] + initial_state.FLAGS[ F.CY ]
	PC_has_incremented = state.REG_UINT16[ U16.PC ] == initial_state.REG_UINT16[ U16.PC ] + 1
	REG_is_unchanged = (U8.A == register) or (state.REG_UINT8[ register ] == initial_state.REG_UINT8[ register ])
	MEM_is_unchanged = np.all(state.MEM == initial_state.MEM)


	assert A_is_sum_of_A_and_REG_and_CY, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: A\' =/= A + REG + CY' 	
	assert PC_has_incremented, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: PC\' =/= PC + 1' 
	assert REG_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: REG\' =/= REG' 
	assert MEM_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: MEM\' =/= MEM' 


def test_op_adc_mem():
	initial_state = get_initial_state()
	opcodes_to_test = np.array([0x8E])

	initial_state.REG_UINT8[ U8.H ] = 0x05
	initial_state.REG_UINT8[ U8.L ] = 0x06
	initial_state.MEM[ :opcodes_to_test.shape[0] ] = opcodes_to_test
	initial_state.MEM[ 0x0506 ] = 0x10
	initial_state.FLAGS[ F.CY ] = True

	state = initial_state.clone()
	step(state)

	A_is_sum_of_A_and_MEM_and_CY = state.REG_UINT8[ U8.A ] == initial_state.REG_UINT8[ U8.A ] + initial_state.MEM[ 0x0506 ] + initial_state.FLAGS[ F.CY ]
	PC_has_incremented = state.REG_UINT16[ U16.PC ] == initial_state.REG_UINT16[ U16.PC ] + 1
	MEM_is_unchanged = np.all(state.MEM == initial_state.MEM)

	assert A_is_sum_of_A_and_MEM_and_CY, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: A\' =/= A + MEM + CY' 	
	assert PC_has_incremented, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: PC\' =/= PC + 1' 
	assert MEM_is_unchanged, f'[postcondition] op {hex(state.MEM[state.REG_UINT16[U16.PC - 1]])}: MEM\' =/= MEM' 



