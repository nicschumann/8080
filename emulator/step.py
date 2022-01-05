from .state import State
from .state import Uint16Registers as U16
from .state import Uint8Registers as U8
from .state import FlagsRegisters as F

from .opcodes import OPCODE_TABLE
from .opcodes.abstract import UnimplementedOp


def decode_op(state: State):
	pc = state.REG_UINT16[ U16.PC ]
	opcode = state.MEM[pc]

	try:
		return OPCODE_TABLE[opcode]

	except KeyError:
		return UnimplementedOp()


def step(state: State):
	# fetch & decode
	op = decode_op(state)
	state.REG_UINT16[ U16.PC ] += 0x01

	# execute & writeback
	op.step(state)	