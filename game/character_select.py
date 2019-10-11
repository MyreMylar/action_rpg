import pygame

from game.ui_text_button import UTTextButton
from game.ui_character_button import UTCharacterButton


class CharacterSelect:

    def __init__(self, fonts, screen_data, characters):

        self.menu_results = [0, 0]

        self.portraits = self.load_portrait_table("images/portraits_small.png", 32, 48, False)
        self.background_image = pygame.image.load("images/menu_background.png").convert()

        self.back_button = UTTextButton([437, 465, 150, 35], "Back", fonts, 1)

        self.title_text_render = fonts[3].render("Choose a character", True, pygame.Color("#000000"))
        self.title_text_render_rect = self.title_text_render.get_rect(centerx=screen_data.screen_size[0] * 0.5,
                                                                      centery=64)

        self.characters = characters

        self.character_buttons = []
        character_index = 0
        for character in self.characters:
            character_button = UTCharacterButton(
                [387, 128+(character_index * 64), 250, 52], character, fonts, character_index, self.portraits)

            self.character_buttons.append(character_button)
            character_index += 1

    def run(self, screen):
        self.menu_results = [0, 0]
        for event in pygame.event.get():
            self.back_button.handle_input_event(event)
            for button in self.character_buttons:
                button.handle_input_event(event)

        screen.blit(self.background_image, (0, 0))  # draw the background
        screen.blit(self.title_text_render, self.title_text_render_rect)

        self.back_button.update()
        if self.back_button.was_pressed():
            self.menu_results = [1, 0]
        self.back_button.draw(screen)

        for button in self.character_buttons:
            button.update()
            if button.was_pressed():
                self.menu_results = [2, button.index]
            button.draw(screen)

        return self.menu_results

    @staticmethod
    def load_portrait_table(filename, width, height, use_transparency):
        if use_transparency:
            image = pygame.image.load(filename).convert_alpha()
        else:
            image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, int(image_width/width)):
            line = []
            tile_table.append(line)
            for tile_y in range(0, int(image_height/height)):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table
