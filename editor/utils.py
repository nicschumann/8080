def int_to_hex(i, fill=2):
	return hex(i)[2:].zfill(fill)

def int_to_bin(i, fill=8):
	return bin(i)[2:].zfill(fill)