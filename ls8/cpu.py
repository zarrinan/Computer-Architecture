"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256        
        self.reg = [0] * 8          
        self.pc = 0                
        self.ir = 0                
        self.mar = 0                
        self.mdr = 0                
        self.fl = [0] * 8          
        self.reg[7] = 0xF4         

    def load(self, filepath, *args):
        """Load a program into memory."""

        address = 0

        with open(filepath, 'r') as f:
            program = f.read().splitlines()
            program = ['0b'+line[:8] for line in program if
                       line and line[0] in ['0', '1']]
            f.close()

        print(program)
        for instruction in program:
            self.ram[address] = eval(instruction)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(self.fl)
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

    def run(self):
        """Run the CPU."""
        pass
