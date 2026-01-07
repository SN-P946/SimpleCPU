import time

class SimpleCPU:
    def __init__(self):
        # --- 1. MEMORY & REGISTERS ---
        # 256 bytes of RAM (8-bit addressable)
        self.memory = [0] * 256 
        
        # General Purpose Registers (8-bit)
        self.registers = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        
        # Program Counter (Points to the current instruction address)
        self.pc = 0 
        
        # Control flag to keep the CPU running
        self.running = False

    def load_program(self, program_data):
        """Loads a list of machine code into memory starting at address 0."""
        for i, byte in enumerate(program_data):
            if i < len(self.memory):
                self.memory[i] = byte
        print(f"Program loaded ({len(program_data)} bytes).")

    # --- 2. FETCH STAGE ---
    def fetch(self):
        """Retrieves the byte at the current PC and increments PC."""
        if self.pc >= len(self.memory):
            raise Exception("Program Counter out of bounds!")
        
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    # --- 3. ALU (Arithmetic Logic Unit) ---
    def alu_compute(self, operation, val1, val2=None):
        """Performs arithmetic and logic operations. Returns 8-bit result."""
        result = 0
        if operation == 'ADD':
            result = val1 + val2
        elif operation == 'SUB':
            result = val1 - val2
        elif operation == 'AND':
            result = val1 & val2
        elif operation == 'OR':
            result = val1 | val2
        elif operation == 'NOT':
            result = ~val1
            
        # Ensure 8-bit wrap-around (0-255)
        return result & 0xFF

    # --- 4. DECODE & EXECUTE STAGE ---
    def execute(self, opcode):
        """Decodes the opcode and performs the specific operation."""
        
        # OPCODE MAP (Our Custom ISA)
        # 0x01: LOAD reg, value  (Move immediate value into register)
        # 0x02: ADD reg, reg     (Add source reg to dest reg)
        # 0x03: AND reg, reg     (Bitwise AND)
        # 0x04: OUT reg          (Print register value)
        # 0xFF: HLT              (Halt/Stop)

        if opcode == 0x01:  # LOAD [Reg] [Value]
            reg_name = self.fetch_register_name() # Fetch next byte as reg ID
            value = self.fetch()                  # Fetch next byte as value
            self.registers[reg_name] = value
            print(f"EXEC: LOAD {reg_name}, {value}")

        elif opcode == 0x02: # ADD [Dest], [Src]
            dest = self.fetch_register_name()
            src = self.fetch_register_name()
            val1 = self.registers[dest]
            val2 = self.registers[src]
            
            # Use ALU
            result = self.alu_compute('ADD', val1, val2)
            self.registers[dest] = result
            print(f"EXEC: ADD {dest}, {src} (Result: {result})")

        elif opcode == 0x03: # AND [Dest], [Src]
            dest = self.fetch_register_name()
            src = self.fetch_register_name()
            val1 = self.registers[dest]
            val2 = self.registers[src]
            
            # Use ALU
            result = self.alu_compute('AND', val1, val2)
            self.registers[dest] = result
            print(f"EXEC: AND {dest}, {src} (Result: {result})")
            
        elif opcode == 0x04: # OUT [Reg]
            reg_name = self.fetch_register_name()
            print(f"--> OUTPUT: Register {reg_name} = {self.registers[reg_name]}")

        elif opcode == 0xFF: # HLT
            print("EXEC: HLT (Halt)")
            self.running = False
            
        else:
            print(f"Unknown Opcode: {hex(opcode)}")

    def fetch_register_name(self):
        """Helper to map a byte 0-3 to A-D."""
        reg_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
        reg_id = self.fetch()
        return reg_map.get(reg_id, 'A')

    # --- MAIN LOOP ---
    def run(self):
        self.running = True
        self.pc = 0
        print("--- CPU START ---")
        while self.running:
            # 1. Fetch
            opcode = self.fetch()
            # 2. Decode & Execute
            self.execute(opcode)
            # Sleep to visualize speed
            time.sleep(0.5) 
        print("--- CPU STOPPED ---")
        self.dump_registers()

    def dump_registers(self):
        print("\nFinal Register State:")
        for reg, val in self.registers.items():
            print(f"{reg}: {val} (0x{val:02X})")

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    cpu = SimpleCPU()

    # Define Register IDs for our code: A=0, B=1, C=2, D=3
    
    # WRITING THE PROGRAM:
    # 1. LOAD A with 10
    # 2. LOAD B with 20
    # 3. ADD A, B  (A = 10 + 20 = 30)
    # 4. OUT A
    # 5. HLT
    
    program = [
        0x01, 0x00, 10,  # LOAD A, 10
        0x01, 0x01, 20,  # LOAD B, 20
        0x02, 0x00, 0x01, # ADD A, B
        0x04, 0x00,       # OUT A
        0xFF              # HLT
    ]

    cpu.load_program(program)
    cpu.run()
