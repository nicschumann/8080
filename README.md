# Tiny 8080

A python-based Intel `8080` disassembler and emulator. All opcodes tested.

## User Interface Notes

I want to build a UI into this emulator that makes it as easy as possible to understand what's going on in a given 8080 state. For now, I'll focus on just making the state legible. As a start, this means seeing 

*(Note for posterity: Started writing this right after I finished implemented and testing the 244 basic opcodes for the 8080. Now I have a rom, an emulator, and a super dumb state dump. I can step the state, and watch the register file update. I have no idea what it's doing, really. I need tools to make this system comprehensible.)*

### Understanding the Current State

To understand what's happening in a current state, you need to see what's happening in the register file and what's happening in memory. Ideally, you would also be able to how the two are connected... where the stack pointer points, where the program counter points, where the register pairs point.

One issue is that memory is just really, really big (even at the 8080's tiny 16-bit address space). How do we dump out memory? One option is to display it as a 2D array of lenth-k byte cells (depending on the zoom level). Then we could implement commands to reshape, or seek through memory. Good place to start?



## Running

The base directory needs to be part of the `PYTHONPATH`, so run this script as a module:

```sh
python -m main # rather than python main.py
```

Similarly, run `pytest` as a module to go test:

```sh
python -m pytest -v # -v optional; shows individual test identities
```

### Testing Note: Opcodes

The intel 8080 processor has `244` unique opcodes, out of a possible 256. The remaining 12 unallocated opcodes are aliases for `nop`, `jmp`, `call`, and `ret`. They should not be used. If you run `python -m pytest` to test all the opcodes, it will report `243` opcodes tested. This is because a test for the `daa` instruction (Decimal Adjust Accumulator, for doing 4-bit binary coded decimal math) is not implemented on this emulator as of yet. Once I have a compelling test case for `daa`, I'll add the test.

## References

- [Matrix of 256 possible 1-byte instructions for the 8080](https://pastraiser.com/cpu/i8080/i8080_opcodes.html). Super useful overview; useful reference for opcode coverage, disassembler, and emulator.
- [List of all 8080 opcodes, along with opcode size (1, 2, or, 3 bytes)](http://www.emulator101.com/8080-by-opcode.html). Another useful one; has information about the behavior of most (not all) opcodes.
- [Intel 8080 Data Book](http://bitsavers.trailing-edge.com/components/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf). The whole thing.