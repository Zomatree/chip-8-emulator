import pygame

pygame.display.init()


class Display:
    def __init__(self, pixel_size=8):
        self.pixel_size = 8
        self.surface = pygame.display.set_mode(size=(64*pixel_size, 32*pixel_size))
    
    def draw(self, vx, vy, pixels):
        """
        Draws a sprite at coordinate (VX, VY)
        that has a width of 8 pixels and a height of N pixels.
        Each row of 8 pixels is read as bitcoded starting from memory location I
        I value doesnt change after the execution of this instruction.
        As described above, VF is set to 1 if any screen pixels are flipped
        from set to unset when the sprite is drawn or to 0 if that doesnt happen
        """

    def update(self):
        pygame.display.update()