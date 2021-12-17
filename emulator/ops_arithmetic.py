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

def subop_setflags_add(result: int, state: State):
	"""result may be a 16-bit uint"""
	state.FLAGS[ F.Z ] = True if result & 0xFF == 0 else False
	state.FLAGS[ F.S ] = True if result & 0x80 > 0 else False
	state.FLAGS[ F.P ] = True if (result & 0xFF) % 2 == 0 else False 
	state.FLAGS[ F.CY ] = True if result > 0xFF else False
	# NOTE(Nic): AC is not implemented in this emulator yet...




# ---- ops -------------------------------------------------------
# These functions emulate individual opcodes
# of repeated functionality that span multiple opcodes
#
# naming convention: op_[canonical opname]_0x[opcode hex]
# ----------------------------------------------------------------

def op_add_M_0x86(state: State):
	target_address = (state.REG_UINT8[ U8.H ] << 8) | state.REG_UINT8[ U8.L ]
	result = state.REG_UINT8[ U8.A ] + state.MEM[ target_address ]
	subop_setflags_add(result, state)
	state.REG_UINT8[ U8.A ] = result & 0xFF

def op_adc_M_0x8E(state: State):
	target_address = (state.REG_UINT8[ U8.H ] << 8) | state.REG_UINT8[ U8.L ]
	result = state.REG_UINT8[ U8.A ] + state.MEM[ target_address ] + state.FLAGS[ F.CY ]
	subop_setflags_add(result, state)
	state.REG_UINT8[ U8.A ] = result & 0xFF

# ---- optemplates -----------------------------------------------
# These functions are simple higher-order templates that 
# return opcode functions. I use these to implement basic classes 
# of operations like add, sub, etc ~ where there are many opcodes
# that behave identically except for the registers they operate on.
#
# naming convention: optemplate_[canonical opname]
# ----------------------------------------------------------------

def optemplate_add(reg: U8):
	def op(state: State):
		result = state.REG_UINT8[ U8.A ] + state.REG_UINT8[reg]
		subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF # cast result to a uint8_t

	return op


def optemplate_adc(reg: U8):
	def op(state: State):
		result = state.REG_UINT8[ U8.A ] + state.REG_UINT8[reg] + state.FLAGS[ F.CY ]
		subop_setflags_add(result, state)
		state.REG_UINT8[ U8.A ] = result & 0xFF

	return op


ARITHMETIC_OPCODES = {
	0x80: optemplate_add( U8.B ),
	0x81: optemplate_add( U8.C ),
	0x82: optemplate_add( U8.D ),
	0x83: optemplate_add( U8.E ),
	0x84: optemplate_add( U8.H ),
	0x85: optemplate_add( U8.L ),
	0x86: op_add_M_0x86,
	0x87: optemplate_add( U8.A ),

	0x88: optemplate_adc( U8.B ),
	0x89: optemplate_adc( U8.C ),
	0x8A: optemplate_adc( U8.D ),
	0x8B: optemplate_adc( U8.E ),
	0x8C: optemplate_adc( U8.H ),
	0x8D: optemplate_adc( U8.L ),
	0x8E: op_adc_M_0x8E,
	0x8F: optemplate_adc( U8.A ),
}