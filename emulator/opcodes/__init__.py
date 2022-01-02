# 8080 Opcode Table
# =================
# constructed by looking at:
# - http://www.emulator101.com/8080-by-opcode.html
# also: https://pastraiser.com/cpu/i8080/i8080_opcodes.html

from emulator.state import State
from emulator.state import Uint8Registers as U8
from emulator.state import Uint16Registers as U16
from emulator.state import FlagsRegisters as F

from .datatransfer import *
from .arithmetic import *
from .machine import *


OPCODE_LIST = [
	NOP(),
	# LXI BLOCK: Load Extended Immediate Values
	LXI_Reg_Imm(0x01, U8.B, U8.C),
	LXI_Reg_Imm(0x11, U8.D, U8.E),
	LXI_Reg_Imm(0x21, U8.H, U8.L),
	LXI_SP(0x31),

	# LDA / STA BLOCK: Load and Store the accumulator
	STAX_Reg(0x02, U8.B, U8.C),
	STAX_Reg(0x12, U8.D, U8.E),
	LDAX_Reg(0x0A, U8.B, U8.C),
	LDAX_Reg(0x1A, U8.D, U8.E),
	SHLD(0x22),
	LHLD(0x2A),
	STA(0x32),
	LDA(0x3A),
	XCHG(0xEB),


	# MVI BLOCK: Move Immediate Values
	MVI_Reg_Imm(0x06, U8.B),
	MVI_Reg_Imm(0x16, U8.D),
	MVI_Reg_Imm(0x26, U8.H),
	MVI_Mem_Imm(0x36),
	MVI_Reg_Imm(0x0E, U8.C),
	MVI_Reg_Imm(0x1E, U8.E),
	MVI_Reg_Imm(0x2E, U8.L),
	MVI_Reg_Imm(0x3E, U8.A),

	# MOV BLOCK: 0x40 – 0x7F (with HLT at 0x76)
	MOV_Reg_Reg(0x40, U8.B, U8.B),
	MOV_Reg_Reg(0x41, U8.B, U8.C),
	MOV_Reg_Reg(0x42, U8.B, U8.D),
	MOV_Reg_Reg(0x43, U8.B, U8.E),
	MOV_Reg_Reg(0x44, U8.B, U8.H),
	MOV_Reg_Reg(0x45, U8.B, U8.L),
	MOV_Reg_Mem(0x46, U8.B),
	MOV_Reg_Reg(0x47, U8.B, U8.A),

	MOV_Reg_Reg(0x48, U8.C, U8.B),
	MOV_Reg_Reg(0x49, U8.C, U8.C),
	MOV_Reg_Reg(0x4A, U8.C, U8.D),
	MOV_Reg_Reg(0x4B, U8.C, U8.E),
	MOV_Reg_Reg(0x4C, U8.C, U8.H),
	MOV_Reg_Reg(0x4D, U8.C, U8.L),
	MOV_Reg_Mem(0x4E, U8.C),
	MOV_Reg_Reg(0x4F, U8.C, U8.A),

	MOV_Reg_Reg(0x50, U8.D, U8.B),
	MOV_Reg_Reg(0x51, U8.D, U8.C),
	MOV_Reg_Reg(0x52, U8.D, U8.D),
	MOV_Reg_Reg(0x53, U8.D, U8.E),
	MOV_Reg_Reg(0x54, U8.D, U8.H),
	MOV_Reg_Reg(0x55, U8.D, U8.L),
	MOV_Reg_Mem(0x56, U8.D),
	MOV_Reg_Reg(0x57, U8.D, U8.A),

	MOV_Reg_Reg(0x58, U8.E, U8.B),
	MOV_Reg_Reg(0x59, U8.E, U8.C),
	MOV_Reg_Reg(0x5A, U8.E, U8.D),
	MOV_Reg_Reg(0x5B, U8.E, U8.E),
	MOV_Reg_Reg(0x5C, U8.E, U8.H),
	MOV_Reg_Reg(0x5D, U8.E, U8.L),
	MOV_Reg_Mem(0x5E, U8.E),
	MOV_Reg_Reg(0x5F, U8.E, U8.A),

	MOV_Reg_Reg(0x60, U8.H, U8.B),
	MOV_Reg_Reg(0x61, U8.H, U8.C),
	MOV_Reg_Reg(0x62, U8.H, U8.D),
	MOV_Reg_Reg(0x63, U8.H, U8.E),
	MOV_Reg_Reg(0x64, U8.H, U8.H),
	MOV_Reg_Reg(0x65, U8.H, U8.L),
	MOV_Reg_Mem(0x66, U8.H),
	MOV_Reg_Reg(0x67, U8.H, U8.A),

	MOV_Reg_Reg(0x68, U8.L, U8.B),
	MOV_Reg_Reg(0x69, U8.L, U8.C),
	MOV_Reg_Reg(0x6A, U8.L, U8.D),
	MOV_Reg_Reg(0x6B, U8.L, U8.E),
	MOV_Reg_Reg(0x6C, U8.L, U8.H),
	MOV_Reg_Reg(0x6D, U8.L, U8.L),
	MOV_Reg_Mem(0x6E, U8.L),
	MOV_Reg_Reg(0x6F, U8.L, U8.A),

	MOV_Mem_Reg(0x70, U8.B),
	MOV_Mem_Reg(0x71, U8.C),
	MOV_Mem_Reg(0x72, U8.D),
	MOV_Mem_Reg(0x73, U8.E),
	MOV_Mem_Reg(0x74, U8.H),
	MOV_Mem_Reg(0x75, U8.L),
	# MOV_Mem_Reg(0x70, U8.L), # Put HLT here.
	MOV_Mem_Reg(0x77, U8.A),

	MOV_Reg_Reg(0x78, U8.A, U8.B),
	MOV_Reg_Reg(0x79, U8.A, U8.C),
	MOV_Reg_Reg(0x7A, U8.A, U8.D),
	MOV_Reg_Reg(0x7B, U8.A, U8.E),
	MOV_Reg_Reg(0x7C, U8.A, U8.H),
	MOV_Reg_Reg(0x7D, U8.A, U8.L),
	MOV_Reg_Mem(0x7E, U8.A),
	MOV_Reg_Reg(0x7F, U8.A, U8.A),


	# Arithmetic Group

	INX_Reg(0x03, U8.B, U8.C),
	INX_Reg(0x13, U8.D, U8.E),
	INX_Reg(0x23, U8.H, U8.L),
	INX_SP(0x33),

	INR_Reg(0x04, U8.B),
	INR_Reg(0x14, U8.D),
	INR_Reg(0x24, U8.H),
	INR_Mem(0x34),
	INR_Reg(0x0C, U8.C),
	INR_Reg(0x1C, U8.E),
	INR_Reg(0x2C, U8.L),
	INR_Reg(0x3C, U8.A),

	DCX_Reg(0x0B, U8.B, U8.C),
	DCX_Reg(0x1B, U8.D, U8.E),
	DCX_Reg(0x2B, U8.H, U8.L),
	DCX_SP(0x3B),

	DCR_Reg(0x05, U8.B),
	DCR_Reg(0x15, U8.D),
	DCR_Reg(0x25, U8.H),
	DCR_Mem(0x35),
	DCR_Reg(0x0D, U8.C),
	DCR_Reg(0x1D, U8.E),
	DCR_Reg(0x2D, U8.L),
	DCR_Reg(0x3D, U8.A),


	ADD_Reg(0x80, U8.B),
	ADD_Reg(0x81, U8.C),
	ADD_Reg(0x82, U8.D),
	ADD_Reg(0x83, U8.E),
	ADD_Reg(0x84, U8.H),
	ADD_Reg(0x85, U8.L),
	ADD_Mem(0x86),
	ADD_Reg(0x87, U8.A),

	ADC_Reg(0x88, U8.B),
	ADC_Reg(0x89, U8.C),
	ADC_Reg(0x8A, U8.D),
	ADC_Reg(0x8B, U8.E),
	ADC_Reg(0x8C, U8.H),
	ADC_Reg(0x8D, U8.L),
	ADC_Mem(0x8E),
	ADC_Reg(0x8F, U8.A),

	SUB_Reg(0x90, U8.B),
	SUB_Reg(0x91, U8.C),
	SUB_Reg(0x92, U8.D),
	SUB_Reg(0x93, U8.E),
	SUB_Reg(0x94, U8.H),
	SUB_Reg(0x95, U8.L),
	SUB_Mem(0x96),
	SUB_Reg(0x97, U8.A),

	SBB_Reg(0x98, U8.B),
	SBB_Reg(0x99, U8.C),
	SBB_Reg(0x9A, U8.D),
	SBB_Reg(0x9B, U8.E),
	SBB_Reg(0x9C, U8.H),
	SBB_Reg(0x9D, U8.L),
	SBB_Mem(0x9E),
	SBB_Reg(0x9F, U8.A),
	

	ADI(0xC6),
	SUI(0xD6),

	ACI(0xCE),
	SBI(0xDE)



]

NEW_OPCODE_TABLE = dict(map(lambda op: (op.code, op), OPCODE_LIST))

OPCODE_TABLE = {
			 # format string for printing opcode, structure of args to read.
	b'\x00': [['nop', [], ''], []],
	b'\x01': [['lxi', ['B', '{1}{0}'], '\t\t; B := data:{1}; C := data:{0}'], [1,1]],
	b'\x02': [['stax', ['B'], '\t\t\t; (BC) := A'], []],
	b'\x03': [['inx', ['B'], '\t\t\t; BC := BC + 1'], []],
	b'\x04': [['inr', ['B'], '\t\t\t; B := B + 1; set flags Z, S, P, AC'], []],
	b'\x05': [['dcr', ['B'], '\t\t\t; B := B - 1; set flags Z, S, P, AC'], []],
	b'\x06': [['mvi', ['B', '{0}'], '\t\t; B := data:{0}'], [1]],
	b'\x07': [['rlc', [], '\t\t\t; A := A << 1; A[0] := A_prev[7]; CY = A_prev[7]'], []],
	b'\x08': [['*nop', [], '\t\t\t; nonstandard no op'], []],
	b'\x09': [['dad', ['B'], '\t\t\t; HL = HL + BC; set flags CY'], []],
	b'\x0A': [['ldax', ['B'], '\t\t\t; A := (BC)'], []],
	b'\x0B': [['dcx', ['B'], '\t\t\t; BC = BC - 1'], []],
	b'\x0C': [['inr', ['C'], '\t\t\t; C := C + 1; set flags Z, S, P, AC'], []],
	b'\x0D': [['dcr', ['C'], '\t\t\t; C := C - 1; set flags Z, S, P, AC'], []],
	b'\x0E': [['mvi', ['C', '{0}'], '\t\t; C := data:{0}'], [1]],
	b'\x0F': [['rrc', [], '\t\t\t; A := A >> 1; A[7] = A_prev[0], CY = A_prev[0]'], []],
	
	b'\x10': [['*nop', [], '\t\t\t; nonstandard no op'], []],
	b'\x11': [['lxi', ['D', '{1}{0}'], '\t\t; D := data:{1}; E := data:{0}'], [1,1]],
	b'\x12': [['stax', ['D'], '\t\t\t; (DE) := A'], []],
	b'\x13': [['inx', ['D'], '\t\t\t; (DE) := (DE) + 1'], []],
	b'\x14': [['inr', ['D'], '\t\t\t; D := D + 1; set flags Z, S, P, AC'], []],
	b'\x15': [['dcr', ['D'], '\t\t\t; D := D - 1; set flags Z, S, P, AC'], []],
	b'\x16': [['mvi', ['D', '{0}'], '\t\t; D := data:{0}'], [1]],
	b'\x18': [['*nop', [], '\t\t\t; nonstandard no op'], []],
	b'\x19': [['dad', ['D'], '\t\t\t; HL = HL + DE, set flags CY'], []],
	b'\x1A': [['ldax', ['D'], '\t\t\t; A := (DE)'], []],
	b'\x1B': [['dcx', ['D'], '\t\t\t; DE = DE - 1'], []],
	b'\x1C': [['inr', ['E'], '\t\t\t; E := E + 1; set flags Z, S, P, AC'], []],
	b'\x1D': [['dcr', ['E'], '\t\t\t; E := E - 1; set flags Z, S, P, AC'], []],
	b'\x1E': [['mvi', ['E', '{0}'], '\t\t\t; E := data:{0}'], [1]],
	b'\x1F': [['rar', [], '\t\t\t; A := A >> 1; A[7] := A_prev[7]; CY := A_prev[0]'], []],
	
	b'\x20': [['rim', [], '\t\t\t; "special", nop'], []],
	b'\x21': [['lxi', ['H', '{1}{0}'], '\t\t; H := data:{1}; L := data:{0}'], [1,1]],
	b'\x22': [['shld', ['${1}{0}'], '\t\t; (addr:{1}{0}) := L; (addr:{1}{0} + 1) := H'], [1,1]],
	b'\x23': [['inx', ['H'], '\t\t\t; H := H + 1'], []],
	b'\x24': [['inr', ['H'], '\t\t\t; H := H + 1; set flags Z, S, P, AC'], []],
	b'\x25': [['dcr', ['H'], '\t\t\t; H := H - 1; set flags Z, S, P, AC'], []],
	b'\x26': [['mvi', ['H', '{0}'], '\t\t; L := data:{0}'], [1]],
	b'\x27': [['daa', [], '\t\t\t; "special"'], []],
	b'\x28': [['*nop', [], '\t\t\t; nonstandard no op'], []],
	b'\x29': [['dad', ['H'], '\t\t\t; HL = HL + HI, set flags CY'], []],
	b'\x2A': [['lhld', ['{1}{0}'], '\t\t; L := (addr:{1}{0}); H := (addr:{1}{0} + 1)'], [1,1]],
	b'\x2B': [['dcx', ['H'], '\t\t\t; HL := HL - 1'], []],
	b'\x2C': [['inr', ['L'], '\t\t\t; L = L + 1; set flags Z, S, P, AC'], []],
	b'\x2E': [['mvi', ['L', '{0}'], '\t\t; L := data:{0}'], [1]],
	b'\x2F': [['cma', [], '\t\t\t; A := !A'], []],
	
	b'\x30': [['sim', [], '\t\t\t; "special"; i8080 opcodes lists as no op'], []],
	b'\x31': [['lxi', ['SP', '{1}{0}'], '\t\t; SP[8:16] := data:{1}; SP[0:8] := data:{0}'], [1,1]],
	b'\x32': [['sta', ['{1}{0}'], '\t\t; (addr:{1}{0}) := A'], [1,1]],
	b'\x34': [['inr', ['M'], '\t\t\t; (HL) := (HL) + 1, set flags Z, S, P, AC'], []],
	b'\x35': [['dcr', ['M'], '\t\t\t; (HL) := (HL) - 1; set flags Z, S, P, AC'], []],
	b'\x36': [['mvi', ['M', '{0}'], '\t\t; (HL) := data:{0}'], [1]],
	b'\x37': [['stc', [], '\t\t\t; CY = 1'], []],
	b'\x38': [['*nop', [], '\t\t\t; nonstandard no op'], []],
	b'\x39': [['dad', ['SP'], '\t\t\t; HL = HL + SP; set flags CY'], []],
	b'\x3A': [['lda', ['{1}{0}'], '\t\t; A := (addr:{1}{0})'], [1,1]],
	b'\x3C': [['inr', ['A'], '\t\t\t; A := A + 1; set flags Z, S, P, AC'], []],
	b'\x3D': [['dcr', ['A'], '\t\t\t; A := A - 1; set flags Z, S, P, AC'], []],
	b'\x3E': [['mvi', ['A', '{0}'], '\t\t; A := {0} (set immediate)'], [1]],
	b'\x3F': [['cmc', [], '\t\t\t; CY = !CY; set flags CY'], []],
	
	b'\x40': [['mov', ['B', 'B'], '\t\t; B := B'], []],
	b'\x41': [['mov', ['B', 'C'], '\t\t; B := C'], []],
	b'\x42': [['mov', ['B', 'D'], '\t\t; B := D'], []],
	b'\x43': [['mov', ['B', 'E'], '\t\t; B := E'], []],
	b'\x44': [['mov', ['B', 'H'], '\t\t; B := H'], []],
	b'\x45': [['mov', ['B', 'L'], '\t\t; B := L'], []],
	b'\x46': [['mov', ['B', 'M'], '\t\t; B := (HL)'], []],
	b'\x47': [['mov', ['B', 'A'], '\t\t; B := A'], []],
	b'\x48': [['mov', ['C', 'B'], '\t\t; C := B'], []],
	b'\x49': [['mov', ['C', 'C'], '\t\t; C := C'], []],
	b'\x4A': [['mov', ['C', 'D'], '\t\t; C := D'], []],
	b'\x4B': [['mov', ['C', 'E'], '\t\t; C := E'], []],
	b'\x4C': [['mov', ['C', 'H'], '\t\t; C := H'], []],
	b'\x4D': [['mov', ['C', 'L'], '\t\t; C := L'], []],
	b'\x4E': [['mov', ['C', 'M'], '\t\t; C := (HL)'], []],
	b'\x4F': [['mov', ['C', 'A'], '\t\t; C := A'], []],
	
	b'\x50': [['mov', ['D', 'B'], '\t\t; D := B'], []],
	b'\x51': [['mov', ['D', 'C'], '\t\t; D := C'], []],
	b'\x54': [['mov', ['D', 'H'], '\t\t; D := H'], []],
	b'\x56': [['mov', ['D', 'M'], '\t\t; D := (HL)'], []],
	b'\x57': [['mov', ['D', 'A'], '\t\t; D := A'], []],
	b'\x59': [['mov', ['E', 'C'], '\t\t; E := C'], []],
	b'\x5B': [['mov', ['E', 'E'], '\t\t; E := E'], []],
	b'\x5E': [['mov', ['E', 'M'], '\t\t; E := (HL)'], []],
	b'\x5F': [['mov', ['E', 'A'], '\t\t; E := A'], []],
	
	b'\x60': [['mov', ['H', 'B'], '\t\t; H := B'], []],
	b'\x61': [['mov', ['H', 'C'], '\t\t; H := C'], []],
	b'\x62': [['mov', ['H', 'D'], '\t\t; H := D'], []],
	b'\x63': [['mov', ['H', 'E'], '\t\t; H := E'], []],
	b'\x64': [['mov', ['H', 'H'], '\t\t; H := H'], []],
	b'\x65': [['mov', ['H', 'L'], '\t\t; H := L'], []],
	b'\x66': [['mov', ['H', 'M'], '\t\t; H := (HL)'], []],
	b'\x67': [['mov', ['H', 'A'], '\t\t; H := A'], []],
	b'\x68': [['mov', ['L', 'B'], '\t\t; L := B'], []],
	b'\x69': [['mov', ['L', 'C'], '\t\t; L := C'], []], 
	b'\x6C': [['mov', ['L', 'H'], '\t\t; L := H'], []], 
	b'\x6D': [['mov', ['L', 'L'], '\t\t; L := L'], []],
	b'\x6E': [['mov', ['L', 'M'], '\t\t; L := (HL)'], []],
	b'\x6F': [['mov', ['L', 'A'], '\t\t; L := A'], []],
	
	b'\x70': [['mov', ['M', 'B'], '\t\t; (HL) := B'], []],
	b'\x71': [['mov', ['M', 'C'], '\t\t; (HL) := C'], []],
	b'\x72': [['mov', ['M', 'D'], '\t\t; (HL) := D'], []],
	b'\x73': [['mov', ['M', 'E'], '\t\t; (HL) := E'], []],
	b'\x74': [['mov', ['M', 'H'], '\t\t; (HL) := H'], []],
	b'\x76': [['hlt', [], '\t\t\t; "special", halt machine'], []],
	b'\x77': [['mov', ['M', 'A'], '\t\t; (HL) := A'], []],
	b'\x78': [['mov', ['A', 'B'], '\t\t; A := B'], []],
	b'\x79': [['mov', ['A', 'C'], '\t\t; A := C'], []],
	b'\x7A': [['mov', ['A', 'D'], '\t\t; A := D'], []],
	b'\x7B': [['mov', ['A', 'E'], '\t\t; A := E'], []],
	b'\x7C': [['mov', ['A', 'H'], '\t\t; A := H'], []],
	b'\x7D': [['mov', ['A', 'L'], '\t\t; A := L'], []],
	b'\x7E': [['mov', ['A', 'M'], '\t\t; A := (HL)'], []],
	b'\x7F': [['mov', ['A', 'A'], '\t\t; A := A'], []],
	
	b'\x80': [['add', ['B'], '\t\t\t; A := A + B, set flags Z, S, P, CY, AC'], []],
	b'\x81': [['add', ['C'], '\t\t\t; A := A + C, set flags Z, S, P, CY, AC'], []],
	b'\x82': [['add', ['D'], '\t\t\t; A := A + D, set flags Z, S, P, CY, AC'], []],
	b'\x83': [['add', ['E'], '\t\t\t; A := A + E, set flags Z, S, P, CY, AC'], []],
	b'\x84': [['add', ['H'], '\t\t\t; A := A + H, set flags Z, S, P, CY, AC'], []],
	b'\x85': [['add', ['L'], '\t\t\t; A := A + L, set flags Z, S, P, CY, AC'], []],
	b'\x86': [['add', ['M'], '\t\t\t; A := A + (HL), set flags Z, S, P, CY, AC'], []],
	b'\x88': [['adc', ['B'], '\t\t\t; A := A + B + CY; set flags Z, S, P, CY, AC'], []],
	b'\x8A': [['adc', ['D'], '\t\t\t; A := A + D + CY; set flags Z, S, P, CY, AC'], []],
	b'\x8B': [['adc', ['E'], '\t\t\t; A := A + E + CY; set flags Z, S, P, CY, AC'], []],
	b'\x8E': [['adc', ['M'], '\t\t\t; A := A + (HL) + CY; set flags Z, S, P, CY, AC'], []],

	b'\x90': [['sub', ['B'], '\t\t\t; A := A - B; set flags Z, S, P, CY, AC'], []],
	b'\x94': [['sub', ['H'], '\t\t\t; A := A - H; set flags Z, S, P, CY, AC'], []],
	b'\x97': [['sub', ['A'], '\t\t\t; A := A - A; set flags Z, S, P, CY, AC'], []],
	b'\x98': [['sbb', ['B'], '\t\t\t; A := A - B - CY; set flags Z, S, P, CY, AC'], []],
	b'\x99': [['sbb', ['C'], '\t\t\t; A := A - C - CY; set flags Z, S, P, CY, AC'], []],
	b'\x9A': [['sbb', ['D'], '\t\t\t; A := A - D - CY; set flags Z, S, P, CY, AC'], []],
	b'\x9B': [['sbb', ['E'], '\t\t\t; A := A - E - CY; set flags Z, S, P, CY, AC'], []],
	b'\x9D': [['sbb', ['L'], '\t\t\t; A := A - L - CY; set flags Z, S, P, CY, AC'], []],
	b'\x9E': [['sbb', ['M'], '\t\t\t; A := A - (HL) - CY; set flags Z, S, P, CY, AC'], []],
	
	b'\xA0': [['ana', ['B'], '\t\t\t; A = A & B; set flags Z, S, O, CY, AC'], []],
	b'\xA3': [['ana', ['E'], '\t\t\t; A = A & E; set flags Z, S, O, CY, AC'], []],
	b'\xA6': [['ana', ['M'], '\t\t\t; A = A & M; set flags Z, S, O, CY, AC'], []],
	b'\xA8': [['xra', ['B'], '\t\t\t; A := A ^ B; set flags Z, S, O, CY, AC'], []],
	b'\xA7': [['ana', ['A'], '\t\t\t; A = A & A; set flags Z, S, O, CY, AC'], []],
	b'\xAA': [['xra', ['D'], '\t\t\t; A = A ^ D, set flags Z, S, O, CY, AC'], []],
	b'\xAF': [['xra', ['A'], '\t\t\t; A = A ^ A, set flags Z, S, O, CY, AC'], []],
	
	b'\xB0': [['ora', ['B'], '\t\t\t; A := A | B; set flags Z, S, P, CY, AC'], []],
	b'\xB3': [['ora', ['E'], '\t\t\t; A := A | E; set flags Z, S, P, CY, AC'], []],
	b'\xB4': [['ora', ['H'], '\t\t\t; A := A | H; set flags Z, S, P, CY, AC'], []],
	b'\xB6': [['ora', ['M'], '\t\t\t; A := A | (HL); set flags Z, S, P, CY, AC'], []],
	b'\xB8': [['cmp', ['B'], '\t\t\t; A - B; set flags Z, S, P, CY, AC'], []],
	b'\xBB': [['cmp', ['E'], '\t\t\t; A - E; set flags Z, S, P, CY, AC'], []],
	b'\xBC': [['cmp', ['H'], '\t\t\t; A - H; set flags Z, S, P, CY, AC'], []],
	b'\xBE': [['cmp', ['M'], '\t\t\t; A - (HL); set flags Z, S, P, CY, AC'], []],

	b'\xC0': [['rnz', [], '\t\t\t; if NZ; return'], []],
	b'\xC1': [['pop', ['B'], '\t\t\t; C := (SP); B := (SP + 1); SP := SP + 2'], []],
	b'\xC2': [['jnz', ['${1}{0}'], '\t\t; if NZ; PC := addr:{1}{0}'], [1,1]],
	b'\xC3': [['jmp', ['${1}{0}'], '\t\t; PC := addr:{1}{0}'], [1,1]],
	b'\xC4': [['cnz', ['${1}{0}'], '\t\t; if NZ; call addr:{1}{0}'], [1,1]],
	b'\xC5': [['push', ['B'], '\t\t\t; (SP - 2) := C; (SP - 1) := B; SP := SP - 2'], []],
	b'\xC6': [['adi', ['{0}'], '\t\t\t; A := A + data:{0} (add immediate)'], [1]],
	b'\xC8': [['rz', [], '\t\t\t; if Z; return'], []],
	b'\xC9': [['ret', [], '\t\t\t; PC[0:8] := (SP); PC[8:16] := (SP + 1); SP := SP + 2'], []],
	b'\xCA': [['jz', ['${1}{0}'], '\t\t\t; if Z; PC := addr:{1}{0}'], [1,1]],
	b'\xCC': [['cz', ['${1}{0}'], '\t\t\t; if Z; call addr:{1}{0}'], [1,1]],
	b'\xCD': [['call', ['${1}{0}'], '\t\t; (SP - 1) := PC[8:16]; (SP - 2) := PC[0:8]; SP = SP + 2; PC = addr:{0}'], [1,1]],
	
	b'\xD0': [['rnc', [], '\t\t\t; if NCY; return'], []],
	b'\xD1': [['pop', ['D'], '\t\t\t; E := (SP); D := (SP - 1); SP = SP + 2'], []],
	b'\xD2': [['jnc', ['${1}{0}'], '\t\t; if NCY, PC := addr:{1}{0}'], [1,1]],
	b'\xD3': [['out', ['{0}'], '\t\t\t; special'], [1]],
	b'\xD4': [['cnc', ['${1}{0}'], '\t\t\t; if NCY; call addr:{1}{0}'], [1,1]],
	b'\xD5': [['push', ['D'], '\t\t\t; (SP - 2) := E; (SP - 1) := D; SP := SP - 2'], []],
	b'\xD6': [['sui', ['{0}'], '\t\t\t; A := A - data:{0}; set flags Z, S, P, CY, AC'], [1]],
	b'\xD8': [['rc', [], '\t\t\t; if CY; ret'], []],
	b'\xDA': [['jc', ['${1}{0}'], '\t\t\t; if CY, PC := addr:{1}{0}'], [1,1]],
	b'\xDB': [['in', ['#${0}'], '\t\t\t; interrupt'], [1]],
	b'\xDE': [['sbi', ['{0}'], '\t\t\t; A := A - data:{0} - CY; set flags Z, S, P, CY, AC'], [1]],
	
	b'\xE0': [['rpo', [], '\t\t\t; if PO, return'], []],
	b'\xE1': [['pop', ['H'], '\t\t\t; L := (SP); H := (SP + 1); SP := SP + 2'], []],
	b'\xE2': [['jpo', ['${1}{0}'], '\t\t; if PO, PC := addr:{1}{0}'], [1,1]],
	b'\xE3': [['xthl', [], '\t\t\t; L <=> (SP); H <=> (SP + 1)'], []],
	b'\xE5': [['push', ['H'], '\t\t\t; (SP - 2) := L; (SP - 1) := H; SP := SP - 2'], []],
	b'\xE6': [['ani', ['A', '{0}'], '\t\t; A := A & data:{0}; set flags Z, S, P, CY, AC'], [1]],
	b'\xE9': [['pchl', [], '\t\t\t; PC[8:16] = H; PC[0:7] = L'], []],
	b'\xEA': [['jpe', ['${1}{0}'], '\t\t; if PE; PC := addr:{1}{0}'], [1,1]],
	b'\xEB': [['xchg', [], '\t\t\t; H <=> D, L <=> E'], []],
	b'\xEC': [['cpe', ['${1}{0}'], '\t\t; if PE, call addr:{1}{0}'], [1,1]],
	b'\xEE': [['xri', ['{0}'], '\t\t\t; A := A ^ data:{0} set flags Z, S, P, CY, AC'], [1]],
	
	b'\xF0': [['rp', [], '\t\t\t; if P; return'], []],
	b'\xF1': [['pop', ['PSW'], '\t\t\t; flags := (SP); A := (SP + 1); SP := SP + 2'], []],
	b'\xF5': [['push', ['PSW'], '\t\t; (SP - 2) := flags; (SP - 1) := A; SP := SP - 2'], []],
	b'\xF6': [['ori', ['{0}'], '\t\t\t; A := A | data:{0}; set flags Z, S, P, CY, AC'], [1]],
	b'\xF8': [['rm', [], '\t\t\t; if M; ret'], []],
	b'\xFA': [['jm', ['${1}{0}'], '\t\t\t; if M; PC := addr:{1}{0}'], [1,1]],
	b'\xFB': [['ei', [], '\t\t\t; "special"'], []],
	b'\xFC': [['cm', ['${1}{0}'], '\t\t\t; if M, call addr:{1}{0}'], [1,1]],
	b'\xFE': [['cpi', ['{0}'], '\t\t\t; A - data:{0} (compare immediate)'], [1]],
	b'\xFF': [['rst', ['#7'], '\t\t\t; quick call addr:38'], []],
}