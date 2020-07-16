from . import CPU, Display

display = Display()
cpu = CPU(display)
cpu.memory[0] = 0x00
cpu.memory[1] = 0xE0
cpu.mainloop()

