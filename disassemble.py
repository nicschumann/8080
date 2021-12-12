# import colorama
# from colorama import Fore as F


# 8080 Opcode Table
# from: http://www.emulator101.com/8080-by-opcode.html
# also from: https://pastraiser.com/cpu/i8080/i8080_opcodes.html

OPCODE_TABLE = {
			 # format string for printing opcode, structure of args to read.
	b'\x00': ['nop', []],
	b'\x01': ['lxi B, {0}{1}\t\t; B := data:{0}; C := data:{1}', [1,1]],
	b'\x04': ['inr B\t\t\t; B := B + 1; set flags Z, S, P, AC', []],
	b'\x05': ['dcr B\t\t\t; B := B - 1; set flags Z, S, P, AC', []],
	b'\x06': ['mvi B, {0}\t\t; B := data:{0}', [1]],
	b'\x07': ['rlc\t\t\t; A := A << 1; A[0] := A_prev[7]; CY = A_prev[7]', []],
	b'\x0D': ['dcr C\t\t\t; C := C - 1; set flags Z, S, P, AC', []],
	b'\x0E': ['mvi C, {0}\t\t; C := data:{0}', [1]],
	b'\x0F': ['rrc\t\t\t; A := A >> 1; A[7] = A_prev[0], CY = A_prev[0]', []],
	
	b'\x11': ['lxi D, {0}{1}\t\t; D := data:{0}; E := data:{1}', [1,1]],
	b'\x13': ['inx D\t\t\t; (DE) := (DE) + 1', []],
	b'\x14': ['inr D\t\t\t; D := D + 1; set flags Z, S, P, AC', []],
	b'\x15': ['dcr D\t\t\t; D := D - 1; set flags Z, S, P, AC', []],
	b'\x16': ['mvi D, {0}\t\t; D := data:{0}', [1]],
	b'\x19': ['dad D\t\t\t; HL = HL + DE, set flags CY', []],
	b'\x1A': ['ldax D\t\t\t; A := (DE)', []],
	
	b'\x20': ['rim\t\t\t; "special", nop', []],
	b'\x21': ['lxi H, {0}{1}\t\t; H := data:{0}; L := data:{1}', [1,1]],
	# b'\x21': ['lxi H, {0}\t\t; H := byte 2; L := byte 3', [2]],
	b'\x22': ['shld {0}\t\t; (addr:{0}) := L; (addr:{0} + 1) := H', [2]],
	b'\x23': ['inx H\t\t\t; H := H + 1', []],
	b'\x26': ['mvi H, {0}\t\t; L := data:{0}', [1]],
	b'\x27': ['daa\t\t\t; "special"', []],
	b'\x29': ['dad H\t\t\t; HL = HL + HI, set flags CY', []],
	b'\x2A': ['lhld {0}\t\t; L := (addr:{0}); H := (addr:{0} + 1)', [2]],
	b'\x2B': ['dcx H\t\t\t; HL := HL - 1', []],
	b'\x2C': ['inr L\t\t\t; L = L + 1; set flags Z, S, P, AC', []],
	b'\x2E': ['mvi L, {0}\t\t; L := data:{0}', [1]],
	
	b'\x31': ['lxi SP, {0}{1}\t\t; SP[0:8] := data:{0}; SP[8:16] := data:{1}', [1,1]],
	b'\x32': ['sta {0}\t\t; (addr:{0}) := A', [2,]],
	b'\x34': ['inr M\t\t\t; (HL) := (HL) + 1, set flags Z, S, P, AC', []],
	b'\x35': ['dcr M\t\t\t; (HL) := (HL) - 1; set flags Z, S, P, AC', []],
	b'\x36': ['mvi M, {0}\t\t; (HL) := data:{0}', [1]],
	b'\x37': ['stc\t\t\t; CY = 1', []],
	b'\x3A': ['lda {0}\t\t; A := (addr:{0})', [2]],
	b'\x3C': ['inr A\t\t\t; A := A + 1; set flags Z, S, P, AC ', []],
	b'\x3D': ['dcr A\t\t\t; A := A - 1; set flags Z, S, P, AC', []],
	b'\x3E': ['mvi A, {0} \t\t; A := {0} (set immediate)', [1]],
	
	b'\x46': ['mov B, M\t\t; B := (HL)', []],
	b'\x47': ['mov B, A\t\t; B := A', []],
	b'\x4E': ['mov C, M\t\t; C := (HL)', []],
	b'\x4F': ['mov C, A\t\t; C := A', []],
	
	b'\x56': ['mov D, M\t\t; D := (HL)', []],
	b'\x5E': ['mov E, M\t\t; E := (HL)', []],
	b'\x5F': ['mov E, A\t\t; E := A', []],
	
	b'\x61': ['mov H, C\t\t; H := C', []],
	b'\x66': ['mov H, M\t\t; H := (HL)', []],
	b'\x67': ['mov H, A\t\t; H := A', []],
	b'\x68': ['mov L, B\t\t; L := B', []],
	b'\x69': ['mov L, C\t\t; L := C', []], 
	b'\x6F': ['mov L, A\t\t; L := A', []],
	
	b'\x70': ['mov M, B\t\t; (HL) := B', []],
	b'\x71': ['mov M, C\t\t; (HL) := C', []],
	b'\x72': ['mov M, D\t\t; (HL) := D', []],
	b'\x73': ['mov M, E\t\t; (HL) := E', []],
	b'\x77': ['mov M, A\t\t; (HL) := A', []],
	b'\x78': ['mov A, B\t\t; A := B', []],
	b'\x79': ['mov A, C\t\t; A := C', []],
	b'\x7A': ['mov A, D\t\t; A := D', []],
	b'\x7B': ['mov A, E\t\t; A := E', []],
	b'\x7C': ['mov A, H\t\t; A := H', []],
	b'\x7D': ['mov A, L\t\t; A := L', []],
	b'\x7E': ['mov A, M\t\t; A := (HL)', []],
	
	b'\x80': ['add B\t\t\t; A := A + B, set flags Z, S, P, CY, AC', []],
	b'\x85': ['add L\t\t\t; A := A + L, set flags Z, S, P, CY, AC', []],
	b'\x86': ['add M\t\t\t; A := A + (HL), set flags Z, S, P, CY, AC', []],

	b'\x97': ['sub A\t\t\t; A := A - A, set flags Z, S, P, CY, AC', []],
	
	b'\xA0': ['ana B\t\t\t; A = A & B; set flags Z, S, O, CY, AC', []],
	b'\xA7': ['ana A\t\t\t; A = A & A; set flags Z, S, O, CY, AC', []],
	b'\xAF': ['xra A\t\t\t; A = A ^ A, set flags Z, S, O, CY, AC', []],
	
	b'\xB0': ['ora B\t\t\t; A := A | B; set flags Z, S, P, CY, AC', []],
	b'\xB4': ['ora H\t\t\t; A := A | H; set flags Z, S, P, CY, AC', []],
	b'\xB8': ['cmp B\t\t\t; A - B; set flags Z, S, P, CY, AC', []],
	b'\xBE': ['cmp M\t\t\t; A - (HL); set flags Z, S, P, CY, AC' , []],

	b'\xC0': ['rnz\t\t\t; if NZ; return', []],
	b'\xC1': ['pop B\t\t\t; C := (SP); B := (SP + 1); SP := SP + 2', []],
	b'\xC2': ['jnz {0}\t\t; if NZ; PC := addr:{0}', [2]],
	b'\xC3': ['jmp {0} \t\t; PC := addr:{0}', [2]],
	b'\xC4': ['cnz {0}\t\t; if NZ; call addr:{0}', [2]],
	b'\xC5': ['push B\t\t\t; (SP - 2) := C; (SP - 1) := B; SP := SP - 2', []],
	b'\xC6': ['adi {0}\t\t\t; A := A + data:{0} (add immediate)', [1]],
	b'\xC8': ['rz\t\t\t; if Z; return', []],
	b'\xC9': ['ret\t\t\t; PC[0:8] := (SP); PC[8:16] := (SP + 1); SP := SP + 2', []],
	b'\xCA': ['jz {0}\t\t\t; if Z; PC := addr:{0}', [2]],
	b'\xCC': ['cz {0}\t\t\t; if Z; call addr:{0}', [2]],
	b'\xCD': ['call {0}\t\t; (SP - 1) := PC[8:16]; (SP - 2) := PC[0:8]; SP = SP + 2; PC = addr:{0}', [2]],
	
	b'\xD0': ['rnc\t\t\t; if NCY; return', []],
	b'\xD1': ['pop D\t\t\t; E := (SP); D := (SP - 1); SP = SP + 2', []],
	b'\xD2': ['jnc {0}\t\t; if NCY, PC := addr:{0}', [2]],
	b'\xD3': ['out {0}\t\t\t; special', [1]],
	b'\xD5': ['push D\t\t\t; (SP - 2) := E; (SP - 1) := D; SP := SP - 2', []],
	b'\xD6': ['sui {0}\t\t\t; A := A - data:{0}; set flags Z, S, P, CY, AC', [1]],
	b'\xDA': ['jc {0}\t\t\t; if CY, PC := addr:{0}', [2]],
	b'\xDB': ['in {0}\t\t\t; interrupt', [1]],
	b'\xDE': ['sbi {0}\t\t\t; A := A - data:{0} - CY; set flags Z, S, P, CY, AC', [1]],
	
	b'\xE1': ['pop H\t\t\t; L := (SP); H := (SP + 1); SP := SP + 2', []],
	b'\xE3': ['xthl\t\t\t; L <=> (SP); H <=> (SP + 1)', []],
	b'\xE5': ['push H\t\t\t; (SP - 2) := L; (SP - 1) := H; SP := SP - 2', []],
	b'\xE6': ['ani A, {0}\t\t; A := A & data:{0}; set flags Z, S, P, CY, AC', [1]],
	b'\xE9': ['pchl\t\t\t; PC[8:16] = H; PC[0:7] = L', []],
	b'\xEA': ['jpe {0}\t\t; if PE; PC := addr:{0}', [2]],
	b'\xEB': ['xchg\t\t\t; H <=> D, L <=> E', []],
	
	b'\xF1': ['pop psw\t\t\t; flags := (SP); A := (SP + 1); SP := SP + 2', []],
	b'\xF5': ['push psw\t\t; (SP - 2) := flags; (SP - 1) := A; SP := SP - 2', []],
	b'\xF6': ['ori {0}\t\t\t; A := A | data:{0}; set flags Z, S, P, CY, AC', [1]],
	b'\xFA': ['jm {0}\t\t\t; if M; PC := addr:{0}', [2]],
	b'\xFB': ['ei\t\t\t; "special"', []],
	b'\xFE': ['cpi {0}\t\t\t; A - data:{0} (compare immediate)', [1]],
}


# colorama.init(autoreset=True)

file = open('./roms/invaders.h', 'rb')


# Disassembly Loop
opcode = file.read(1)

while opcode:
	line = file.tell()

	try:
		dissasembly, argsizes = OPCODE_TABLE[opcode]

	except KeyError:
		print(f'\n[Disassembler Error] Unrecognized opcode: {opcode.hex()}')
		exit()

	args = tuple(map(lambda argsize: bytearray(file.read(argsize)).hex(), argsizes))
	print(f'{hex(line)}:\t\t' + (dissasembly.format(*args)))

	opcode = file.read(1)




file.close()