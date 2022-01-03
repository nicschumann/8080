import pytest
import numpy as np

from emulator.state import State
from emulator.state import Uint16Registers as U16
from emulator.state import Uint8Registers as U8
from emulator.state import FlagsRegisters as F

from emulator.opcodes import OPCODE_LIST

from emulator.step import step

from test.test_ops_base import get_initial_state, get_op_name


BRANCH_OPCODES = [
	'jmp', 'jnz', 'jz',
	'jnc', 'jc', 'jpo',
	'jpe', 'jp', 'jm',

	'call', 'cnz', 'cz',
	'cnc', 'cc', 'cpo',
	'cpe', 'cp', 'cm',

	'ret', 'rnz', 'rz',
	'rnc', 'rc', 'rpo',
	'rpe', 'rp', 'rm'
]

OPCODES = list(filter(lambda op: op.name in BRANCH_OPCODES, OPCODE_LIST))

@pytest.mark.parametrize('op', OPCODES, ids=get_op_name)
def test_op(op):
	for flag_state in [False, True]:
		preop_state = get_initial_state(flags=flag_state)
		preop_state.MEM[0x0] = op.code

		postop_state = preop_state.clone()
		step(postop_state)

		op.test(preop_state, postop_state)
