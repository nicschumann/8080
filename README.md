# Tiny 8080

A python-based Intel `8080` disassembler and emulator. All opcodes tested.

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