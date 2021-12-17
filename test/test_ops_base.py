import pytest
import numpy as np

from emulator.state import State
from emulator.state import Uint16Registers as U16
from emulator.state import Uint8Registers as U8
from emulator.state import FlagsRegisters as F

from emulator.opcodes import OPCODE_LIST

from emulator.step import step


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

def get_op_name(val):
	return val.get_name()


@pytest.mark.parametrize('op', OPCODE_LIST, ids=get_op_name)
def test_op(op):
	preop_state = get_initial_state()
	preop_state.MEM[0x0] = op.code

	postop_state = preop_state.clone()
	step(postop_state)

	op.test(preop_state, postop_state)
