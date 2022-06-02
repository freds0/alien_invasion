# Import the pygame module
import pygame
from pygame import mixer
from player import Player
from enemy import Enemy
import os

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)
# Define constants for the screen width and height
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
FRAMES_PER_SEC = 60

PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75

ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30

SCORE_POSITION_X = 10
SCORE_POSITION_Y = 10

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Invasion")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

score_value = 0
font = pygame.font.Font(os.path.join("fonts", "FreeSansBold.ttf"), 32)

# Instantiate player. Right now, this is just a rectangle.
player = Player(PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

background_image = pygame.image.load(os.path.join("images", "space.jpg") )
spaceship_image = pygame.image.load(os.path.join("images", "player.png"))
spaceship_image = pygame.transform.scale(spaceship_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
spaceship_image = pygame.transform.rotate(spaceship_image, -90)

enemy_image = pygame.image.load(os.path.join("images", "enemy.png"))
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_image = pygame.transform.rotate(enemy_image, -90)


mixer.music.load(os.path.join('audios', "background.mp3"))
mixer.music.play(-1)

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

def show_score_message(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    SCREEN.blit(score, (x, y))

def show_gameover_message(x, y):
    message = font.render("Game Over!", True, (255,0,0))
    SCREEN.blit(message, (x - message.get_rect().width / 2, y - message.get_rect().height / 2))
    message = font.render("Press Enter To Continue", True, (255,255,0))
    SCREEN.blit(message, (x - message.get_rect().width / 2, 50 + y - message.get_rect().height / 2 ))

def check_colision_player_enemies(player, enemies):
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        return False
    else:
        return True

def check_colision_enemies_lasers(enemies, lasers):
    # Check if any enemies have collided with the player
    if pygame.sprite.groupcollide(enemies, lasers, True, True):
        return True
    else:
        return False

def draw_screen(player, enemies, lasers):
    global score_value
    game_over = False
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    # Update enemies positions
    enemies.update()
    # Update lasers positions
    lasers.update()
    # Fill the screen with white
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(background_image, (0, 0))
    SCREEN.blit(spaceship_image, (player.rect.centerx + spaceship_image.get_rect().x / 2 , player.rect.y ))

    show_score_message(SCORE_POSITION_X, SCORE_POSITION_Y)

    # Draw all sprites
    #for entity in all_sprites:
    #    SCREEN.blit(entity.surf, entity.rect)

    # Draw all enemies
    for enemy in enemies:
        SCREEN.blit(enemy_image, (enemy.rect.centerx + enemy_image.get_rect().x / 2 , enemy.rect.y ))

    # Draw all lasers
    for laser in lasers:
        SCREEN.blit(laser.surf, laser.rect)

    if ( not check_colision_player_enemies(player, enemies)):
        # Play sound
        game_over_sound = mixer.Sound(os.path.join("audios", "game_over.mp3"))
        game_over_sound.play(fade_ms=10)
        # Game over message
        show_gameover_message(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        score_value = 0
        game_over = True

    if check_colision_enemies_lasers(enemies, lasers):
        score_value += 1
        # Play sound
        explosion_sound = mixer.Sound(os.path.join("audios", "explosion1.mp3"))
        explosion_sound.play(fade_ms=10)

    # Update the display
    pygame.display.update()

    return game_over

def main():
    # Variable to keep the main loop running
    running = True
    # Main loop
    while running:
        game_over = False
        # Ensure program maintains a rate of 60 frames per second
        clock.tick(FRAMES_PER_SEC)

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    new_laser = player.shoot()
                    # Play sound
                    laser_sound = mixer.Sound(os.path.join("audios", "shoot.mp3" ))
                    laser_sound.play(fade_ms=10)
                    # Add to lists
                    lasers.add(new_laser)
                    all_sprites.add(new_laser)

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(ENEMY_WIDTH, ENEMY_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        game_over = draw_screen(player, enemies, lasers)

        if game_over:
            # Kill all enemies
            for enemy in enemies:
                enemy.kill ()
            waiting = True
            while (waiting):
                clock.tick(FRAMES_PER_SEC)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #pygame.quit()
                        waiting = False
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        game_over = False

        running = not(game_over)
        
    pygame.quit()


if __name__ == "__main__":
    main()
