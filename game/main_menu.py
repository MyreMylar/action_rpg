import pygame

from game.ui_text_button import UTTextButton


class MainMenu:

    def __init__(self, fonts):
        self.background_image = pygame.image.load("images/menu_background.png").convert()
        self.play_game_button = UTTextButton([402, 415, 220, 35], "Character Select", fonts, 1)
        self.view_high_scores_button = UTTextButton([427, 465, 170, 35], "High Scores", fonts, 1)
        self.edit_map_button = UTTextButton([437, 515, 150, 35], "Edit Map", fonts, 1)

    def run(self, screen, fonts, screen_data):
        is_main_menu_and_index = [0, 0]
        for event in pygame.event.get():
            self.play_game_button.handle_input_event(event)
            self.edit_map_button.handle_input_event(event)
            self.view_high_scores_button.handle_input_event(event)

        self.play_game_button.update()
        self.view_high_scores_button.update()
        self.edit_map_button.update()
        
        if self.play_game_button.was_pressed():
            is_main_menu_and_index[0] = 1
        if self.view_high_scores_button.was_pressed():
            is_main_menu_and_index[0] = 3
        if self.edit_map_button.was_pressed():
            is_main_menu_and_index[0] = 2
                    
        screen.blit(self.background_image, (0, 0))  # draw the background
        
        main_menu_title_string = "Mild Peril"
        main_menu_title_text_render = fonts[2].render(main_menu_title_string, True, pygame.Color("#000000"))
        screen.blit(main_menu_title_text_render,
                    main_menu_title_text_render.get_rect(centerx=screen_data.screen_size[0] * 0.5, centery=128))

        self.play_game_button.draw(screen)
        self.view_high_scores_button.draw(screen)
        self.edit_map_button.draw(screen)

        return is_main_menu_and_index
