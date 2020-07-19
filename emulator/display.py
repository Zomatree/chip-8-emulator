import os
import logging
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame

pygame.display.init()
pygame.mixer.init()

pygame.mixer.music.load('beep.wav')
fps = pygame.time.Clock()
pygame.display.set_caption("CHIP-8 Emulator")


class Display:
    def __init__(self, pixel_size, keyboard):
        self.pixel_size = pixel_size
        self.screen = self.blank_screen
        self.keypress = None
        self.keyboard = {getattr(pygame, f"{k[0].upper()}{k[1:]}"): v for k, v in keyboard.items()}

        self.surface = pygame.display.set_mode(size=(64*pixel_size, 32*pixel_size))
        self.beep = pygame.mixer.music.play

    def draw(self, vx, vy, pixels):
        """
        Draws a sprite at coordinate (VX, VY)
        that has a width of 8 pixels and a height of N pixels.
        Each row of 8 pixels is read as bitcoded starting from memory location I
        I value doesnt change after the execution of this instruction.
        As described above, VF is set to 1 if any screen pixels are flipped
        from set to unset when the sprite is drawn or to 0 if that doesnt happen
        """
        collision = 0
    
        for i in range(0, len(pixels)):
            for new_pixel in pixels[i * 8:(8 * i) + 8]:
                before = self.screen[vy + i][vx + (i * 8)]
                pixel = (new_pixel == 1) ^ before
                if before == 1 and pixel == 0:
                    collision = 1

                self.screen[vy + i][vx+(i*8)] = pixel
    
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
    
    def set_keypress(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        for key, hex_value in self.keyboard.items():
            if keys[key]:
                self.keypress = hex_value
                logging.info(f"Detected keypress {key} {hex_value=}")
 
    @property
    def blank_screen(self):
        return [[0 for _ in range(64)] for _ in range(32)]

    @staticmethod
    def sleep():
        fps.tick(60)

    def clear(self):
        self.surface.fill((0,0,0))

    def wait_for_keypress(self):
        self.keypress = None
        while not self.keypress:
            self.set_keypress()
            self.sleep()

        return self.keypress
