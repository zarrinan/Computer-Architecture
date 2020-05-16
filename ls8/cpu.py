"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # Memory
        self.reg = [0] * 8  # General-purpose numeric registers R0-R7
        self.pc = 0  # Program Counter
        self.ir = 0  # Instruction Register
        self.mar = 0  # Memory Address Register
        self.mdr = 0  # Memory Data Register
        self.fl = [0] * 8  # 8-bit Flags Register /elg
        self.sp = self.reg[7] = self.ram[0xF4]  # set stack pointer

        self.branchtable = {}
        self.branchtable[0b00000001] = self.handle_hlt
        self.branchtable[0b10000010] = self.handle_ldi
        self.branchtable[0b01000111] = self.handle_prn
        self.branchtable[0b10100010] = self.handle_mul
        self.branchtable[0b01000101] = self.handle_push
        self.branchtable[0b01000110] = self.handle_pop
        self.branchtable[0b01010000] = self.handle_call
        self.branchtable[0b00010001] = self.handle_ret
        self.branchtable[0b10100000] = self.handle_add
        self.branchtable[0b10100111] = self.handle_cmp
        self.branchtable[0b01010100] = self.handle_jmp
        self.branchtable[0b01010101] = self.handle_jeq
        self.branchtable[0b01010110] = self.handle_jne
        self.branchtable[0b01101001] = self.handle_not
        self.branchtable[0b10101010] = self.handle_or
        self.branchtable[0b10101011] = self.handle_xor
        self.branchtable[0b10101100] = self.handle_shl
        self.branchtable[0b10101101] = self.handle_shr
        self.branchtable[0b10100100] = self.handle_mod

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def handle_hlt(self):
        print("quit")
        running = False

    def handle_ldi(self):
        register = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.pc += 3
        self.reg[register] = value

    def handle_prn(self):
        print(self.reg[self.ram[self.pc + 1]])
        self.pc += 2

    def handle_add(self):
        self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_mul(self):
        self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_or(self):
        self.alu("OR", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_xor(self):
        self.alu("XOR", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_not(self):
        self.alu("NOT", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_shl(self):
        self.alu("SHL", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_shr(self):
        self.alu("SHR", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_mod(self):
        self.alu("MOD", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_push(self):
        self.sp -= 1
        register = self.ram[self.pc + 1]
        self.ram[self.sp] = self.reg[register]
        self.pc += 2

    def handle_pop(self):
        register = self.ram[self.pc + 1]
        self.reg[register] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def handle_call(self):
        self.sp -= 1
        current_address = self.pc + 2
        self.ram[self.sp] = current_address

        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]

    def handle_ret(self):
        self.pc = self.ram[self.sp]
        self.sp += 1

    def handle_cmp(self):
        self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def handle_jmp(self):
        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]

    def handle_jeq(self):
        register = self.ram[self.pc + 1]
        if self.fl & 0b00000001 > 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_jne(self):
        register = self.ram[self.pc + 1]
        if self.fl & 0b00000001 == 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def load(self, filepath, *args):
        """Load a program into memory."""
        address = 0
        with open(filepath, 'r') as f:
            program = f.read().splitlines()
            program = [
                line[:8] for line in program if line and line[0] in ['0', '1']
            ]
            f.close()

        for instruction in program:
            self.ram[address] = int(instruction, 2)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        # print(self.fl)
        print(
            f"TRACE: %02X | %02X %02X %02X |" % (
                self.pc,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2)),
            end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self, debug=False):
        """Run the CPU."""
        running = True

        while running:
            # if debug:
            #     self.trace()
            if self.ram[self.pc] == 0b00000001:
                running = False
            else:
                self.branchtable[self.ram[self.pc]]()
