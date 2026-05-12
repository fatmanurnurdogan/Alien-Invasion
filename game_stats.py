import os
class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        try:
           with open("high_score.txt") as file:
               self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
          
          #start Alien Invasion in an inactive state.
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the time."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
