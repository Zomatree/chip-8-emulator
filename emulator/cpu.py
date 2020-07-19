from random import randint
import logging


class CPU:
    def __init__(self, display):
        self.memory = [0]*4096
        
        self.memory[0:0x200] = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,
            0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0,
            0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10,
            0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0,
            0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0,
            0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0,
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0,
            0xF0, 0x80, 0xF0, 0x80, 0x80,
        ]

        self.registers = [0]*16
        self.stack = [0]*16
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.index = 0
        self.pc = 0x200
        self.display = display

    def load_program(self, filename):
        with open(filename, "rb") as f:
            logging.info(f"Reading file {filename}")
            data = f.read()
            for index, byte in zip(range(len(data)), data):
                self.memory[0x200+index] = byte

    def add_overflow(a, b):
        result = a + b
        
        return result, bool(result % 8)

    def minus_overflow(a, b):
        result = a - b
        
        return result, not bool(result % 8)

    def read_word(self):
        return self.memory[self.pc] << 8 | self.memory[self.pc+1]

    def exec_cycle(self):
        opcode = self.read_word()
        self.process_opcode(opcode)

    def process_opcode(self, opcode):
        logging.info(f"processing opcode {opcode}")
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4

        logging.info(f"{x=}, {y=}")

        vx = int(str(self.registers[x]), 16)
        vy = int(str(self.registers[y]), 16)

        nnn = opcode & 0x0FFF
        nn = opcode & 0x00FF
        n = opcode & 0x000F

        op_1 = (opcode & 0xF000) >> 12
        op_2 = (opcode & 0x0F00) >> 8
        op_3 = (opcode & 0x00F0) >> 4
        op_4 = opcode & 0x000F

        self.pc += 2

        ops = (op_1, op_2, op_3, op_4)

        logging.info(f"{ops=}")

        if ops == (0, 0, 0xE, 0):
            self.display.clear()
        if ops == (0, 0, 0xE, 0xE):
            self.stack_pointer -= 1
            self.pc = self.stack[self.stack_pointer]
        if op_1 == 1:
            self.pc = nnn
        if op_1 == 2:
            self.stack[self.stack_pointer] = self.pc
            self.stack_pointer += 1
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
            collision = self.display.draw(vx, vy, self.memory[self.index:n*8])
            self.registers[0xF] = collision

        if op_1 == 0xE and op_3 == 0x9 and op_4 == 0xE:
            if vx == self.display.keypress:
                self.pc += 2

        if op_1 == 0xE and op_3 == 0x9 and op_4 == 0xE:
            if vx != self.display.keypress:
                self.pc += 2

        if op_1 == 0xF and op_3 == 0x0 and op_4 == 0x7:
            self.registers[x] = self.delay_timer

        if op_1 == 0xF and op_3 == 0x0 and op_4 == 0xA:
            self.registers[x] = self.display.wait_for_keypress()

        if op_1 == 0xF and op_3 == 0x0 and op_4 == 0x7:
            self.delay_timer = vx

        if op_1 == 0xF and op_3 == 0x1 and op_4 == 0x8:
            self.sound_timer = vx

        if op_1 == 0xF and op_3 == 0x1 and op_4 == 0xE:
            self.index += vx

        if op_1 == 0xF and op_3 == 0x1 and op_4 == 0xE:
            self.index = vx * 4
        
        if op_1 == 0xF and op_3 == 0x3 and op_4 == 0x3:
            self.memory[self.index] = vx / 100
            self.memory[self.index + 1] = (vx / 10) % 10
            self.memory[self.index + 2] = (vx % 100) % 10

        if op_1 == 0xF and op_3 == 0x5 and op_4 == 0x5: 
            v = self.registers[:x]
            self.memory[self.index:self.index+len(v)] = v

        if op_1 == 0xF and op_3 == 0x6 and op_4 == 0x5:
            self.registers[:x] = self.memory[self.index:self.index+x]

    def decrement_timer(self):
        if self.delay_timer:
            self.delay_timer -= 1

        if self.sound_timer:
            self.sound_timer -= 1
            self.display.beep()

    def mainloop(self):
        while True:
            self.exec_cycle()
            self.decrement_timer()

            self.index += 1

            self.display.update()
            self.display.sleep()
            self.display.clear()