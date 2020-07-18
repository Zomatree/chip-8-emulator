import pygame
import sys

pygame.display.init()
fps = pygame.time.Clock()


class Display:
    def __init__(self, pixel_size=8):
        self.pixel_size = 8
        self.screen = self.blank_screen

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
        collision = False
    
        for i in range(0, len(pixels), 8):
            new_row = pixels[i:i+8]
            old_row = self.screen[vy + int(i / 8)][vx:vx+8]
            
            collision = any(True for before, after in zip(old_row, new_row) if before == 1 and after == 0)
            self.screen[vy + int(i / 8)][vx:vx+8] = pixels[i:i+8]
    
        return int(collision)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i, row in enumerate(self.screen):
            for j, value in enumerate(row):
                colour = (value*255, value*255, value*255)
                pygame.draw.rect(self.surface, colour, pygame.Rect(j*self.pixel_size, i*self.pixel_size, self.pixel_size, self.pixel_size))

        pygame.display.update()

    @property
    def blank_screen(self):
        return [[0 for _ in range(64)] for _ in range(32)]

    @staticmethod
    def sleep():
        fps.tick(60)

    def clear_screen(self):
        self.surface.fill((0,0,0))
