import pygame

# Define explosion animation frames
# You would typically load these images from an assets folder
# For now, let's create simple placeholder rectangles
explosion_animation = [
    pygame.Surface([30, 30], pygame.SRCALPHA), # Frame 1 (transparent)
    pygame.Surface([40, 40], pygame.SRCALPHA), # Frame 2
    pygame.Surface([50, 50], pygame.SRCALPHA), # Frame 3
    pygame.Surface([60, 60], pygame.SRCALPHA), # Frame 4
    pygame.Surface([70, 70], pygame.SRCALPHA), # Frame 5
    pygame.Surface([80, 80], pygame.SRCALPHA), # Frame 6
    pygame.Surface([90, 90], pygame.SRCALPHA), # Frame 7
    pygame.Surface([100, 100], pygame.SRCALPHA) # Frame 8
]

# Draw something on the placeholder surfaces for visualization
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (255, 255, 255)] # Red, Orange, Yellow, White
for i, frame in enumerate(explosion_animation):
    color_index = i % len(colors)
    color = colors[color_index]
    pygame.draw.circle(frame, color, (frame.get_width() // 2, frame.get_height() // 2), frame.get_width() // 2 - 5)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.frames = explosion_animation
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # Milliseconds per frame

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index == len(self.frames):
                self.kill() # Remove the sprite when animation is done
            else:
                center = self.rect.center # Save the center before changing image
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = center # Set the center back 