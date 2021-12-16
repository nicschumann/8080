from .state import State
from .state import Uint16Registers as U16
from .state import Uint8Registers as U8
from .state import FlagsRegisters as F

from .ops_arithmetic import ARITHMETIC_OPCODES

# ---- ops -------------------------------------------------------
# These functions emulate individual opcodes
# of repeated functionality that span multiple opcodes
#
# naming convention: op_[canonical opname]_0x[opcode hex]
# ----------------------------------------------------------------

def op_unimplemented(state: State):
	print(f'[Emulator Error] Unimplemented opcode: {hex(state.MEM[state.PC[0]])}')
	exit()


def op_nop_0x00(state: State): 
	pass


def op_lxi_0x01(state: State):
	pc = state.REG_UINT16[ U16.PC ]

	state.REG_UINT8[ U8.C ] = state.MEM[pc + 1]
	state.REG_UINT8[ U8.B ] = state.MEM[pc + 2]
	state.REG_UINT16[ U16.PC ] += 0x2



OPCODE_TABLE = {
	**ARITHMETIC_OPCODES,
}


def decode_op(state):
	pc = state.REG_UINT16[ U16.PC ]
	opcode = state.MEM[pc]

	try:
		return OPCODE_TABLE[opcode]

	except KeyError:
		return unimplemented


def step(state: State):
	# fetch & decode
	op = decode_op(state)
	state.REG_UINT16[ U16.PC ] += 0x01

	# execute & writeback
	op(state)
	