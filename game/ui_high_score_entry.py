import pygame


class UIHighScoreEntry:
    def __init__(self, rect, character, fonts, index, portraits):
        self.fonts = fonts
        self.character = character

        self.portrait = portraits[character.portrait_index[0]][character.portrait_index[1]]
        self.rect = rect
        self.started_button_click = False
        self.clicked_button = False
        self.is_hovered = True
        
        self.is_enabled = True

        self.index = index

        self.button_colour = pygame.Color("#4B4B4B")
        self.text_colour = pygame.Color("#FFFFFF")
        self.score_colour = pygame.Color("#FFAF64")

        self.button_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3])

        self.pos_text_render = self.fonts[3].render(str(index + 1) + ".", True, self.text_colour)
        self.pos_text_rect = self.pos_text_render.get_rect(x=self.rect[0] + 2,
                                                           centery=self.rect[1] + self.rect[3] * 0.5)

        self.portrait_rect = self.portrait.get_rect(x=self.rect[0] + 52, y=self.rect[1] + 2)

        self.name_text_render = self.fonts[4].render(self.character.name, True, self.text_colour)
        self.name_text_rect = self.name_text_render.get_rect(x=self.rect[0] + 98,
                                                             centery=self.rect[1] + self.rect[3] * 0.3)

        score_label_string = "Score: "
        self.score_label_text_render = self.fonts[4].render(score_label_string, True, self.text_colour)
        self.score_label_text_rect = self.score_label_text_render.get_rect(x=self.rect[0] + 98,
                                                                           centery=self.rect[1] + self.rect[3]*0.75)
        
        score_string = "{:,}".format(character.score)
        self.score_text_render = self.fonts[4].render(score_string, True, self.score_colour)
        score_text_x_pos = self.score_label_text_rect[0] + self.score_label_text_rect[2]
        self.score_text_rect = self.score_text_render.get_rect(x=score_text_x_pos,
                                                               centery=self.rect[1] + self.rect[3]*0.75)

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_colour, self.button_rect, 0)
        screen.blit(self.pos_text_render, self.pos_text_rect)
        screen.blit(self.portrait, self.portrait_rect)
        screen.blit(self.name_text_render, self.name_text_rect)
        screen.blit(self.score_label_text_render, self.score_label_text_rect)
        screen.blit(self.score_text_render, self.score_text_rect)
