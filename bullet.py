import pygame
from pygame.sprite import Sprite
import random

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Creat a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create a bullet rect at (0, 0) and then set correct position
        self.image = pygame.image.load('images/fire.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""
        #update the decimal position of the bullet.""""
        self.y -= self.settings.bullet_speed
        #update the rect position.
        self.rect.y = self.y
        
        self.rect.x += random.randint(-1, 1)
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
        