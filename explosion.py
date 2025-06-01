import pygame
from settings import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.frames = self.game.assets.get("explosion_frames", [
            pygame.Surface([30, 30], pygame.SRCALPHA),
            pygame.Surface([40, 40], pygame.SRCALPHA),
            pygame.Surface([50, 50], pygame.SRCALPHA),
            pygame.Surface([60, 60], pygame.SRCALPHA),
            pygame.Surface([70, 70], pygame.SRCALPHA),
            pygame.Surface([80, 80], pygame.SRCALPHA),
            pygame.Surface([90, 90], pygame.SRCALPHA),
            pygame.Surface([100, 100], pygame.SRCALPHA)
        ])
        # If using placeholder surfaces, draw colored circles
        if "explosion_frames" not in self.game.assets:
            colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 255, 255)]
            for i, frame in enumerate(self.frames):
                color_index = i % len(colors)
                pygame.draw.circle(frame, colors[color_index], (frame.get_width() // 2, frame.get_height() // 2), frame.get_width() // 2 - 5)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Milliseconds per frame

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index == len(self.frames):
                self.kill()  # Remove the sprite when animation is done
            else:
                center = self.rect.center
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = center