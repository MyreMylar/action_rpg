import pygame


class HUDButton(pygame.sprite.Sprite):
    def __init__(self, start_pos, button_image_name, hud_sprites, *groups):
        super().__init__(*groups)
        self.clicked = False
        self.button_image_name = button_image_name
        self.image_unselected = pygame.image.load("images/hud_icons/" + self.button_image_name + "_unselected.png")
        self.image_selected = pygame.image.load("images/hud_icons/" + self.button_image_name + "_selected.png")
        # self.sprite = pygame.sprite.Sprite()
        self.image = self.image_unselected
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        hud_sprites.add(self)

        # value text
        self.text_value = 0
        self.font = pygame.font.Font(None, 16)
        cost_string = "{:,}".format(self.text_value)
        self.cost_text_render = self.font.render(cost_string, True, pygame.Color("#FFFFFF"))
        self.text_pos = [start_pos[0], start_pos[1] + 42]

        self.selected = False

    def update_text_values(self, value):
        self.text_value = value
        cost_string = ""
        text_colour = pygame.Color("#FFFFFF")
        if self.text_value > 0:
            cost_string = "{:,}".format(self.text_value)
        elif self.text_value == 0:
            cost_string = "{:,}".format(self.text_value)
            text_colour = pygame.Color("#FA3232")
        elif self.text_value == -1:
            cost_string = "infinite"
        self.cost_text_render = self.font.render(cost_string, True, text_colour)
        
    def set_selected(self):
        self.selected = True
        self.image = self.image_selected

    def clear_selected(self):
        self.selected = False
        self.image = self.image_unselected

    def draw_text(self, screen):
        pass
