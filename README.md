# Tiny 8080

A python-based Intel `8080` disassembler and emulator. (All opcodes tested, with the exception of `daa`, because I don't have a good test routine for fixed-point decimal arithmetic).

## Editor

The editor module is a text-based, interactive `curses` application. It has a number of different windows and views into the state, and accepts a variety of different commands for manipulating both the trace of the program, and the editor state.

My goal is to have a flexible, bidirectional environment for navigating through a program state. Currently, my traces support bi-directional stepping: Obviously, you cans step the state forward by stepping the emulator. Whenever the emulator steps forward, a diff object is created. The program trace in itself is essentially a sequence of state-diffs; since we capture state diffs, navigating bidirectionally through the program is possible.

The editor is handled through text-based input. The following is a table of the commands available:

| implemented | input | command name | description |
| - | - | - | - |
| ✓ | `q` | quit | Stops the emulator running and quits the program. |
| ✓ | `s [steps]` | step | Steps the emulator forward by `[steps]` instruction. Records a diff between the state before the step command and the state after, and appends it to the trace. |




## Running

The base directory needs to be part of the `PYTHONPATH`, so run this script as a module:

```sh
python -m edit # rather than python edit.py
```

Similarly, run `pytest` as a module to go test:

```sh
python -m pytest -v # -v optional; shows individual test identities
```

### Testing Note: Opcodes

The intel 8080 processor has 244 unique opcodes, out of a possible 256. The remaining 12 unallocated opcodes are aliases for `nop`, `jmp`, `call`, and `ret`. They should not be used. If you run `python -m pytest` to test all the opcodes, it will report `243` opcodes tested. This is because a test for the `daa` instruction (Decimal Adjust Accumulator, for doing 4-bit binary coded decimal math) is not implemented on this emulator as of yet. Once I have a compelling test case for `daa`, I'll add the test.

## References

- [Matrix of 256 possible 1-byte instructions for the 8080](https://pastraiser.com/cpu/i8080/i8080_opcodes.html). Super useful overview; useful reference for opcode coverage, disassembler, and emulator.
- [List of all 8080 opcodes, along with opcode size (1, 2, or, 3 bytes)](http://www.emulator101.com/8080-by-opcode.html). Another useful one; has information about the behavior of most (not all) opcodes.
- [Intel 8080 Data Book](http://bitsavers.trailing-edge.com/components/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf). The whole thing.