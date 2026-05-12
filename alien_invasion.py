import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star 
import random 
import os

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.stars = []
        self._create_stars() 

        self._create_fleet()

        #make the play button
        self.play_button = Button(self, "Play")

        #set the background color.
        self.bg_color = self.settings.bg_color
        self.menu_bg = pygame.image.load("images/menu.bmp") 
        self.menu_bg = pygame.transform.scale( 
            self.menu_bg, #
            (self.settings.screen_width, self.settings.screen_height) 
        )
        self.font = pygame.font.SysFont(None, 80) 

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

                for star in self.stars: 
                    star["y"] += 0.3 

                    if star["y"] > self.settings.screen_height: 
                        star["y"] = 0 
                        star["x"] = random.randint(0, self.settings.screen_width) #

            self._update_screen()
            

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() 
                self._check_play_button(mouse_pos) 

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) #
        if button_clicked and not self.stats.game_active: 
            #reset the game settings
            self.settings.initialize_dynamic_settings() 

            #reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True  
            self.stats.ships_left = self.settings.ship_limit
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



    def _update_bullets(self):
        self.bullets.update()

        #get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
            """Respond to bullet-alien collisions."""
            #remove any bullets and aliens that have collided.
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  

            if collisions:  
                for aliens in collisions.values(): 
                    self.stats.score += self.settings.alien_points * len(aliens) 
                self.sb.prep_score()  
                self.sb.check_high_score()        

            if not self.aliens: 
                #destroy existing bullets and create new fleet.
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()

                #increase level.
                self.stats.level += 1
                self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens): 
            self._ship_hit()

        self._check_alien_bottom()    

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        #decrement ships_left.
        if self.stats.ships_left > 0:
           #decrement ships left.
           self.stats.ships_left -= 1
           #decrement ships_left, and update scoreboard.
           self.sb.prep_ships()

            #get rid of any remaining aliens and bullets.
           self.aliens.empty()
           self.bullets.empty()

           #create a new fleet and center the ship.
           self._create_fleet()
           self.ship.center_ship()

        #pause
           sleep(0.5) 
        else:
         self.stats.game_active = False
         pygame.mouse.set_visible(True)
             
    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit.
                self._ship_hit()
                break

    
    def _create_fleet(self):
     self.aliens.empty()

     for _ in range(30):
        alien = Alien(self)

        # X tam genişlikte dağılsın
        alien.rect.x = random.randrange(0, self.settings.screen_width - alien.rect.width)

        # Y sadece üst kısımda ama daha geniş aralıkta
        alien.rect.y = random.randrange(0, int(self.settings.screen_height * 0.5))
        alien.x = float(alien.rect.x)

        self.aliens.add(alien)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_stars(self): 
        import random 
        for _ in range(100): 
            star = { 
                "x":random.randint(0, self.settings.screen_width),
                "y":random.randint(0, self.settings.screen_height) 
            } 
            self.stars.append(star) 

    def _show_game_over(self):
        text = self.font.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, rect)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += 5  #aşağı inme
        self.settings.fleet_direction *= - 1    

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        if self.stats.game_active:
            self.screen.fill(self.settings.bg_color)
        else:
            self.screen.blit(self.menu_bg, (0, 0))    
        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen) 
            for star in self.stars:
                pygame.draw.circle(self.screen, (255, 255, 255), (star["x"], star["y"]), 1)   

        #draw the score information
            self.sb.show_score() 

        else:
            if self.stats.ships_left <= 0:
                #oyun bittiyse
                self._show_game_over()
            else:
                #oyun başlamadıysa
                self.play_button.draw_button()    


        pygame.display.flip()    

if __name__ == '__main__':
    #make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()