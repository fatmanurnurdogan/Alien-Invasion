import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
       """Initialize the alien and set its starting position."""
       super().__init__()
       self.screen = ai_game.screen
       self.settings = ai_game.settings

       #load the alien image and set its rect attributive.
       self.image = pygame.image.load('images/alien.bmp')
       self.image.set_colorkey((0, 0, 0)) 
       self.rect = self.image.get_rect()

       self.direction = random.choice([-1, 1])

       # aşağı düşme için
       self.drop_speed = random.uniform(0.1, 0.5)
       self.should_drop = random.choice([True, False])

       #start each alien near the top left or the screen.
       self.rect.x = self.rect.width
       self.rect.y = self.rect.height

       #store the alien's exact horizontal position.
       self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x

        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            self.rect.right = screen_rect.right
            self.direction *= -1

        elif self.rect.left <= 0:
             self.rect.left = 0
             self.direction *= -1

