import pygame
from laser import Laser

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height):
        super(Player, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                0,
                (screen_height /2) - self.surf.get_rect().height / 2,
            )
        )
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height

    def shoot(self):
        shoot_x = self.rect.x + self.rect.width
        shoot_y = (self.rect.y + (self.rect.height / 2))
        new_shotgun = Laser(shoot_x, shoot_y, self.screen_width, self.screen_height)
        return new_shotgun

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height
