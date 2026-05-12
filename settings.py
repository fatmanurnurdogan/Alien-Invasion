class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (5, 5, 20) 
        self.speedup_scale = 1.1

        #ship settings
        self.ship_limit= 3

        #bullet settings
        self.bullet_width = 7
        self.bullet_height = 15
        self.bullet_color = (0, 250, 255)
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 2

        #how quickly the game speeds up
        self.speedup_scale = 1.3

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialie setting that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        #sağ =1, sol=-1
        self.fleet_direction = 1

        #fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #scoring 
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale    

        self.alien_points = int(self.alien_points * self.score_scale)
