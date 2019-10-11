import pygame
from pygame.locals import *


class UTCharacterButton:
    def __init__(self, rect, character, fonts, index, portraits):
        self.fonts = fonts
        self.character = character

        self.portrait = portraits[character.portrait_index[0]][character.portrait_index[1]]
        self.rect = rect
        self.started_button_click = False
        self.clicked_button = False
        self.is_hovered = True
        
        self.is_enabled = True

        self.base_button_colour = pygame.Color("#4b4b4b")
        self.base_text_colour = pygame.Color("#FFFFFF")
        self.disabled_button_colour = pygame.Color("#323232")
        self.disabled_text_colour = pygame.Color("#000000")
        self.hovered_button_colour = pygame.Color("#646464")

        self.button_colour = self.base_button_colour
        self.text_colour = self.base_text_colour

        self.button_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3])

        self.portrait_rect = self.portrait.get_rect(x=self.rect[0] + 2, y=self.rect[1] + 2)

        self.name_text_render = self.fonts[4].render(self.character.name, True, self.text_colour)
        self.name_text_rect = self.name_text_render.get_rect(x=self.rect[0] + 48,
                                                             centery=self.rect[1] + self.rect[3] * 0.3)

        stat_string = "STR: " + str(character.strength) + " DEX: " \
                      + str(character.dexterity) + " INT: " + str(character.magic)
        self.stats_text_render = self.fonts[0].render(stat_string, True, self.text_colour)
        self.stats_text_rect = self.name_text_render.get_rect(x=self.rect[0] + 48,
                                                              centery=self.rect[1] + self.rect[3] * 0.75)

        self.index = index

    def handle_input_event(self, event):
        if self.is_enabled and self.is_inside(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked_button = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and self.started_button_click:
                    self.clicked_button = True
                    self.started_button_click = False

    def disable(self):
        self.is_enabled = False
        self.button_colour = self.disabled_button_colour
        self.text_colour = self.disabled_text_colour

    def enable(self):
        self.is_enabled = True
        self.button_colour = self.base_button_colour
        self.text_colour = self.base_text_colour

    def was_pressed(self):
        was_pressed = self.clicked_button
        self.clicked_button = False
        return was_pressed
    
    def update(self):
        if self.is_enabled and self.is_inside(pygame.mouse.get_pos()):
            self.is_hovered = True
            self.button_colour = self.hovered_button_colour
        elif self.is_enabled:
            self.is_hovered = False
            self.button_colour = self.base_button_colour

    def is_inside(self, screen_pos):
        is_inside = False
        if self.rect[0] <= screen_pos[0] <= self.rect[0]+self.rect[2]:
            if self.rect[1] <= screen_pos[1] <= self.rect[1]+self.rect[3]:
                is_inside = True
        return is_inside

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_colour, self.button_rect, 0)
        screen.blit(self.portrait, self.portrait_rect)
        screen.blit(self.name_text_render, self.name_text_rect)
        screen.blit(self.stats_text_render, self.stats_text_rect)
