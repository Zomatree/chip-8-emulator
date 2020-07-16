import numpy
from random import randint
import time


class CPU:
    def __init__(self, display):
        self.memory = [0]*4096
        self.registers = [0]*16
        self.stack = [0]*16
        self.stack_pointer = 0
        self.delay_timer = 0
        self.index = 0
        self.pc = 0
        self.display = display

    def add_overflow(a, b):
        rangeMax = 2 ** 3
        result = a + b
        
        return result, bool(result % 8)

    def minus_overflow(a, b):
        rangeMax = 2 ** 3
        result = a - b
        
        return result, not bool(result % 8)

    def read_word(self):
        return self.memory[self.index] << 8 | self.memory[self.index+1]

    def exec_cycle(self):
        opcode = self.read_word()
        self.process_opcode(opcode)

    def process_opcode(self, opcode):
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x0F00) >> 4

        vx = self.registers[x]
        vy = self.registers[y]

        nnn = opcode & 0x0FFF
        nn = opcode & 0x00FF
        n = opcode & 0x000F

        op_1 = (opcode & 0xF000) >> 12
        op_2 = (opcode & 0x0F00) >> 8
        op_3 = (opcode & 0x00F0) >> 4
        op_4 = opcode & 0x000F

        self.pc += 2

        ops = (op_1, op_2, op_3, op_4)

        if ops == (0, 0, 0xE, 0):
            self.display.clear()
        if ops == (0, 0, 0xE, 0xE):
            self.stack_pointer -= 1
        if op_1 == 1:
            self.pc = nnn
        if op_1 == 2:
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = nnn
        if op_1 == 3:
            if vx == nn:
                self.pc += 2
        if op_1 == 4:
            if vx != nn:
                self.pc += 2
        if op_1 == 5:
            if vx == vy:
                self.pc += 2
        if op_1 == 6:
            self.registers[x] = nn
        if op_1 == 7:
            self.registers[x] += nn
        if op_1 == 8 and op_4 == 0:
            self.registers[x] = self.registers[y]
        if op_1 == 8 and op_4 == 1:
            self.registers[x] = vx | vy
        if op_1 == 8 and op_4 == 2:
            self.registers[x] = vx & vy
        if op_1 == 8 and op_4 == 3:
            self.registers[x] = vx ^ vy
        if op_1 == 8 and op_4 == 4:
            result, overflow = self.add_overflow(vx, vy)

            self.registers[0xF] = overflow
            self.registers[x] = result            

        if op_1 == 8 and op_4 == 5:
            result, overflow = self.minus_overflow(vx, vy)

            self.registers[0xF] = overflow
            self.registers[x] = result

        if op_1 == 8 and op_4 == 6:
            self.registers[0xF] = vx & 1
            self.registers[x] >>= 1

        if op_1 == 8 and op_4 == 7:
            result, overflow = self.minus_overflow(vy, vx)

            self.registers[0xF] = overflow
            self.registers[x] = result

        if op_1 == 8 and op_4 == 0xE:
            self.registers[0xF] = vx & 0x80
            self.registers[x] <<= 1
        
        if op_1 == 9 and op_4 == 0:
            if vx != vy:
                self.pc += 2

        if op_1 == 0xA:
            self.index = nnn

        if op_1 == 0xB:
            self.pc = nnn + self.registers[0]

        if op_1 == 0xC:
            self.registers[x] = randint(0, 255) & nn

        if op_1 == 0xD:
            self.display.draw(vx, vy, self.memory[self.index:n*8])

    def decrement_timer(self):
        if self.delay_timer:
            self.delay_timer -= 1

    def mainloop(self):
        while True:
            self.exec_cycle()
            self.decrement_timer()
            print(bin(self.index))
            self.index += 1
            self.display.update()
            time.sleep(1/60)