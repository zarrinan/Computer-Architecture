"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    # Memory     
        self.reg = [0] * 8      # General-purpose numeric registers R0-R7
        self.pc = 0             # Program Counter    
        self.ir = 0             # Instruction Register 
        self.mar = 0            # Memory Address Register       
        self.mdr = 0            # Memory Data Register    
        self.fl = [0] * 8       # 8-bit Flags Register  
        self.reg[7] = 0xF4      # set stack pointer   

    def load(self, filepath, *args):
        """Load a program into memory."""
        address = 0
        with open(filepath, 'r') as f:
            program = f.read().splitlines()
            program = [line[:8] for line in program if
                       line and line[0] in ['0', '1']]
            f.close()

        for instruction in program:
            self.ram[address] = int(instruction, 2)
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
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def run(self, debug=False):
        """Run the CPU."""
        running = True
       
        while running is True:
            if debug:
                self.trace()
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.ir = self.pc
            instruction = self.ram[self.ir]
            print(instruction)

            if instruction == 0b10100000:  # ADD
                pass   
            elif instruction == 0b10101000:  # AND
                pass   
            elif instruction == 0b01010000:  # CALL register
                pass 
            elif instruction == 0b10100111:  # CMP
                pass  
            elif instruction == 0b01100110:  # DEC
                pass   
            elif instruction == 0b10100011:  # DIV
                pass   
            elif instruction == 0b00000001:  # HLT
                print("quit")
                running = False                        
            elif instruction == 0b01100101:  # INC
                pass  
            elif instruction == 0b01010010:  # INT
                pass  
            elif instruction == 0b00010011:  # IRET
                pass   
            elif instruction == 0b01010101:  # JEQ
                pass  
            elif instruction == 0b01011010:  # JGE
                pass   
            elif instruction == 0b01010111:  # JGT
                pass  
            elif instruction == 0b01011001:  # JLE
                pass  
            elif instruction == 0b01011000:  # JLT
                pass  
            elif instruction == 0b01010100:  # JMP
                pass   
            elif instruction == 0b01010110: # JNE
                pass   
            elif instruction == 0b10000011:  # LD
                pass  
            elif instruction == 0b10000010:  # LDI
                self.reg[operand_a] = operand_b        
            elif instruction == 0b10100100:   # MOD
                pass  
            elif instruction == 0b10100010:  # MUL
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]     
            elif instruction == 0b00000000:  # NOP
                pass   
            elif instruction == 0b01101001:  # NOT
                pass   
            elif instruction == 0b10101010:   # OR
                pass  
            elif instruction == 0b01000110:  # POP
                self.reg[operand_a] = self.ram[self.reg[7]]
                self.reg[7] += 1
            elif instruction == 0b01001000:  # PRA
                pass   
            elif instruction == 0b01000111:   # PRN
                print(self.reg[operand_a])             
            elif instruction == 0b01000101:  # PUSH
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.reg[operand_a]
            elif instruction == 0b00010001:  # RET
                pass   
            elif instruction == 0b10101100:   # SHL
                pass  
            elif instruction == 0b10101101:  # SHR
                pass   
            elif instruction == 0b10000100:  # ST
                pass   
            elif instruction == 0b10100001:  # SUB
                pass   
            elif instruction == 0b10101011:  # XOR
                pass
            else:
                print("Didn't recognize the instruction")
                exit(1)
            # increment program counter
            if instruction < 64:
                self.pc += 1
            if instruction > 64 and instruction <= 127:
                self.pc += 2
            if instruction > 127:
                self.pc += 3
        exit()
