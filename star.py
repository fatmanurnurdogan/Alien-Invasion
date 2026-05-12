import pygame
import random

class Star:
    """A simple star for background animation."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # random position
        self.x = random.randint(0, self.screen_rect.width)
        self.y = random.randint(0, self.screen_rect.height)

        self.speed = random.uniform(0.2, 1.0)

        self.speed = random.uniform(0.1, 1.5)
        self.radius = 1 if self.speed < 0.8 else 2

    def update(self):
        """Move star downward (space moving effect)."""
        self.y += self.speed

        if self.y > self.screen_rect.height:
            self.y = 0
            self.x = random.randint(0, self.screen_rect.width)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)