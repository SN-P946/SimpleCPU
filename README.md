# 8-Bit CPU Simulator

A software-based emulator of a simplified 8-bit Central Processing Unit (CPU). This project demonstrates the fundamental **Fetch-Decode-Execute** cycle used in modern computer architecture, simulating hardware components like the ALU, Program Counter, and General Purpose Registers using object-oriented Python.

## Overview

This simulator mimics the behavior of a physical CPU at the logic level. Instead of running compiled binary from an OS, it runs a custom machine code loaded directly into a simulated 256-byte memory array.

* **Von Neumann Architecture:** Instructions and data are stored in the same memory array.
* **ALU Operations:** Simulating logic gates (AND, OR, NOT) and arithmetic (ADD, SUB) with 8-bit overflow handling.
* **Register Manipulation:** Moving data between general-purpose registers and memory.
* **The Control Unit:** Decoding opcodes to drive CPU behavior.

## Architecture Specs

* **Word Size:** 8-bit (Values 0-255).
* **Memory:** 256 Bytes of RAM.
* **Registers:** 4 General Purpose Registers (A, B, C, D).
* **Program Counter (PC):** Tracks the current instruction address.

## Instruction Set Architecture (ISA)

The CPU utilizes a custom, simplified opcode set.

| Opcode (Hex) | Mnemonic | Operands | Description |
| :--- | :--- | :--- | :--- |
| `0x01` | **LOAD** | `[Reg], [Val]` | Load an immediate 8-bit integer into a register. |
| `0x02` | **ADD** | `[Dest], [Src]` | Add value of Src Reg to Dest Reg. Store result in Dest. |
| `0x03` | **AND** | `[Dest], [Src]` | Bitwise AND of Src and Dest. Store result in Dest. |
| `0x04` | **OUT** | `[Reg]` | Output the current value of the register to the console. |
| `0xFF` | **HLT** | `None` | Halt the CPU operation. |

### Register Mapping
When defining operands in machine code, registers are mapped to integers:
* `0`: Register A
* `1`: Register B
* `2`: Register C
* `3`: Register D

## Usage

### Prerequisites
* Python 3.8+

### Running the Simulator
1.  Clone the repository or download `SimpleCPU.py`.
2.  Run the script:
    ```bash
    python SimpleCPU.py
    ```

### Writing a Program
You can modify the `program` list in the `__main__` block of the Python script. Programs are written in raw machine code (integers/hex).

**Example: Adding two numbers**
```python
# Assembly Logic:
# LOAD A, 10
# LOAD B, 20
# ADD A, B
# OUT A
# HLT

program = [
    0x01, 0x00, 10,   # Opcode 0x01 (LOAD), Reg 0 (A), Value 10
    0x01, 0x01, 20,   # Opcode 0x01 (LOAD), Reg 1 (B), Value 20
    0x02, 0x00, 0x01, # Opcode 0x02 (ADD), Dest 0 (A), Src 1 (B)
    0x04, 0x00,       # Opcode 0x04 (OUT), Reg 0 (A)
    0xFF              # Opcode 0xFF (HLT)
]
