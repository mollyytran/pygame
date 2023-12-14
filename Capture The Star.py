# Molly Tran
# CS 87 B- Assignment 9
# 11/19/2023
# The goal of the game is move the plane right, left, forward, or backward to capture the stars.
# However, if the plane collides with a bird, the game is over. You can remove the birds by clicking the birds


import pygame
from pygame.locals import *
from pygame.sprite import *
import random


# Character class to initialize the sprites
class Character(Sprite):
    def __init__(self, image_path, position):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)


# Method to handle key events and mouse click events, exits the loop if user clicks the close button
def handle_events(plane, birds, running):
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                plane.rect = plane.rect.move(0, -30)
            elif event.key == K_DOWN:
                plane.rect = plane.rect.move(0, 30)
            elif event.key == K_RIGHT:
                plane.rect = plane.rect.move(30, 0)
            elif event.key == K_LEFT:
                plane.rect = plane.rect.move(-30, 0)
        elif event.type == MOUSEBUTTONDOWN:
            for bird in birds:
                if bird.rect.collidepoint(pygame.mouse.get_pos()):
                    bird.kill()
    return running


def update_game(plane, star, birds, speed_x, speed_y, width, height, score):

    # Moves the position of the plane vertically and horizontally
    plane.rect.x += speed_x

    if random.randint(0, 1) == 0:
        plane.rect.y -= speed_y
    else:
        plane.rect.y += speed_y

    # Reset plane position if it goes off the screen
    if plane.rect.x > width:
        plane.rect.center = (0, plane.rect.y)

    # Moves the position of the birds vertically and horizontally
    for bird in birds:
        bird.rect.x -= speed_x
        if random.randint(0, 1) == 0:
            bird.rect.y -= speed_y
        else:
            bird.rect.y += speed_y

        if bird.rect.x < 0 or bird.rect.y < 0:
            bird.rect.center = (width, random.randint(0, height))

    # Check for plane collisions with birds
    if pygame.sprite.spritecollide(plane, birds, False):
        pygame.mixer.Sound("game_over.wav").play()
        return True, score

    # Check for plane collision with the star, increase the score, adds a new bird with every collision
    if pygame.sprite.collide_rect(plane, star):
        pygame.mixer.Sound("squeak.wav").play()
        score += 1
        star.rect.center = (random.randint(0, width), random.randint(0, height))
        birds.add(Character("bird.png", (random.randint(width - 50, 2 * width), random.randint(0, height))))

    return False, score


def main():
    pygame.init()
    pygame.mixer.init()

    width = 600
    height = 500
    speed_x = 1
    speed_y = 1
    score = 0
    game_over = False
    running = True

    # Set up the game window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Capture the Stars")
    clock = pygame.time.Clock()

    # Create player, star, and bird group
    plane = Character("plane.png", (50, 400))
    star = Character("star.png", (250, 350))
    birds = pygame.sprite.Group()

    # Load and scale the sky image
    sky = pygame.transform.scale(pygame.image.load("sky.png"), (width, height))
    sky_rect = sky.get_rect()
    second_sky_rect = sky.get_rect(left=width)

    # Load font for the score
    font = pygame.font.Font("pixeltype/Pixeltype.ttf", 60)

    while running:
        # Handle user input events
        running = handle_events(plane, birds, running)

        if not game_over:
            # Update game state
            game_over, score = update_game(plane, star, birds, speed_x, speed_y, width, height, score)

            # Move sky
            sky_rect.x -= speed_x
            second_sky_rect.x -= speed_x

            # Reset sky position if it goes off the screen
            if sky_rect.right <= 0:
                sky_rect.x = width

            if second_sky_rect.right <= 0:
                second_sky_rect.x = width

            # Display the sky, plane, star, and birds
            screen.blit(sky, sky_rect)
            screen.blit(sky, second_sky_rect)
            screen.blit(plane.image, plane.rect)
            screen.blit(star.image, star.rect)
            birds.draw(screen)

            # Display the score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        # Display game over screen
        if game_over:
            game_over_text = font.render(f"GAME OVER!", True, (255, 255, 255))
            screen.blit(game_over_text, (200, 225))

        # Update the display after each game loop
        pygame.display.update()

        # Control the frame rate of the game loop
        clock.tick(60)


main()
