import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 180, 255)
        self.hover_color = (0, 230, 255) 
        self.current_color = self.button_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #build the button's rect onject and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #the button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button and then draw message
        self.screen.fill(self.current_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_hover(self, mouse_pos):
        """Change color if mouse is over button."""
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.button_color        


