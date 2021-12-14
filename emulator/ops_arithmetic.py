from .state import State
from .state import Uint16Registers as U16
from .state import Uint8Registers as U8
from .state import FlagsRegisters as F


# ---- subops ----------------------------------------------------
# These helpers compartmentalize simple units 
# of repeated functionality that span multiple opcodes
# 
# naming convention: subop_[name]
# ----------------------------------------------------------------

def subop_setflags(result: int, state: State):
	"""result may be a 16-bit uint"""
	state.FLAGS[ F.Z ] = True if result & 0xFF == 0 else False
	state.FLAGS[ F.S ] = True if result & 0x80 > 0 else False
	state.FLAGS[ F.P ] = True if (result & 0xFF) % 2 == 0 else False 
	state.FLAGS[ F.CY ] = True if result > 0xFF else False




# ---- ops -------------------------------------------------------
# These functions emulate individual opcodes
# of repeated functionality that span multiple opcodes
#
# naming convention: op_[canonical opname]_0x[opcode hex]
# ----------------------------------------------------------------

...


# ---- optemplates -----------------------------------------------
# These functions are simple higher-order templates that 
# return opcode functions. I use these to implement basic classes 
# of operations like add, sub, etc ~ where there are many opcodes
# that behave identically except for the registers they operate on.
#
# naming convention: optemplate_[canonical opname]
# ----------------------------------------------------------------

def optemplate_add(reg: U8):
	def op(state : State):
		result = state.REG_UINT8[ U8.A ] + state.REG_UINT8[reg]
		subop_setflags(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	return op


ARITHMETIC_OPCODES = {
	0x80: optemplate_add( U8.B ),
	0x81: optemplate_add( U8.C )
}