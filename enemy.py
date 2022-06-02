import pygame
# Import random for random numbers
import random

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )
        self.speed = random.randint(5, 20)
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
