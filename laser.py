import pygame

# Define a shotgun object by extending pygame.sprite.Sprite
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super(Laser, self).__init__()
        self.surf = pygame.Surface((20, 1))
        self.surf.fill((255, 255, 255))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )
        self.speed = 20

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > self.screen_width:
            self.kill()
