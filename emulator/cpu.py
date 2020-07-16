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

    def decrement_timer(self):
        if self.delay_timer:
            self.delay_timer -= 1
