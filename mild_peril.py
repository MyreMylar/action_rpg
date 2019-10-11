from collections import deque

from game.player import *
from game.player_health_bar import *
from game.mana_bar import *
from game.pick_up import PickUpSpawner
from game.hud_button import *
from game.main_menu import *
from game.map_editor import *
from game.character_select import *
import game.tiled_level as tiled_level_code

from game.high_scores import *

from collision.collision_grid import *

import util.character as character_code


class ScreenData:
    def __init__(self, hud_size: [int, int], editor_hud_size: [int, int], screen_size: [int, int]):
        self.screen_size = screen_size
        self.hud_dimensions = hud_size
        self.editor_hud_dimensions = editor_hud_size
        self.play_area = [self.screen_size[0], self.screen_size[1] - self.hud_dimensions[1]]

    def set_editor_active(self):
        self.play_area = [self.screen_size[0], self.screen_size[1] - self.editor_hud_dimensions[1]]


# noinspection PyUnresolvedReferences
def main():
    characters = []
    characters = character_code.reload_characters(characters)
    
    pygame.init()
    pygame.key.set_repeat()
    x_screen_size = 1024
    y_screen_size = 600
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen_data = ScreenData([x_screen_size, 112], [x_screen_size, 184], [x_screen_size, y_screen_size])
    screen = pygame.display.set_mode(screen_data.screen_size)
    pygame.display.set_caption('Mild Peril')
    background = pygame.Surface(screen.get_size())
    background.fill((95, 140, 95))
    background.convert(screen)

    player_sprites = pygame.sprite.OrderedUpdates()
    all_tile_sprites = pygame.sprite.Group()
    all_top_tile_sprites = pygame.sprite.Group()
    all_monster_sprites = pygame.sprite.OrderedUpdates()
    all_pick_up_sprites = pygame.sprite.Group()
    all_projectile_sprites = pygame.sprite.Group()
    hud_sprites = pygame.sprite.Group()

    fonts = []
    small_font = pygame.font.Font(None, 16)
    font = pygame.font.Font(None, 32)
    very_large_font = pygame.font.Font("data/MetalMania-Regular.ttf", 150)
    large_font = pygame.font.Font("data/MetalMania-Regular.ttf", 58)
    small_bold_font = pygame.font.Font(None, 24)
    small_bold_font.set_bold(True)
    small_fun_font = pygame.font.Font("data/MetalMania-Regular.ttf", 32)
    fonts.append(small_font)
    fonts.append(font)
    fonts.append(very_large_font)
    fonts.append(large_font)
    fonts.append(small_bold_font)
    fonts.append(small_fun_font)

    players = []
    monsters = []
    onscreen_monsters = []
    hud_buttons = []

    grid_square_size = 64
    world_filling_number_of_grid_squares = [64, 64]
    collision_grid = CollisionGrid(world_filling_number_of_grid_squares, grid_square_size)

    tiled_level = tiled_level_code.TiledLevel([64, 64],
                                              all_tile_sprites,
                                              all_top_tile_sprites,
                                              all_monster_sprites,
                                              monsters,
                                              screen_data,
                                              collision_grid)

    tiled_level.load_tiles()
    tiled_level.reset_guards()

    main_menu = MainMenu(fonts)

    character_select = CharacterSelect(fonts, screen_data, characters)
    view_high_score_menu = HighScores(fonts, screen_data, characters)
    
    hud_rect = pygame.Rect(0,
                           screen_data.screen_size[1] - screen_data.hud_dimensions[1],
                           screen_data.hud_dimensions[0],
                           screen_data.hud_dimensions[1])

    editor_hud_rect = pygame.Rect(0,
                                  screen_data.screen_size[1] - screen_data.editor_hud_dimensions[1],
                                  screen_data.editor_hud_dimensions[0],
                                  screen_data.editor_hud_dimensions[1])
    editor = MapEditor(tiled_level, editor_hud_rect, fonts, collision_grid)
    
    health_bar = HealthBar([screen_data.hud_dimensions[0] - (screen_data.hud_dimensions[0] * 0.20),
                            screen_data.screen_size[1] - (0.75 * screen_data.hud_dimensions[1])],
                           (screen_data.hud_dimensions[0] * 0.15), 16)

    mana_bar = ManaBar([screen_data.hud_dimensions[0] - (screen_data.hud_dimensions[0] * 0.20),
                        screen_data.screen_size[1] - (0.55 * screen_data.hud_dimensions[1])],
                       (screen_data.hud_dimensions[0] * 0.15), 16)
 
    rifle_button = HUDButton([48,
                              screen_data.screen_size[1] - screen_data.hud_dimensions[1] + 48],
                             "bow_icon",
                             hud_sprites)

    shotgun_button = HUDButton([144,
                                screen_data.screen_size[1] - screen_data.hud_dimensions[1] + 48],
                               "sword_icon",
                               hud_sprites)

    launcher_button = HUDButton([240,
                                 screen_data.screen_size[1] - screen_data.hud_dimensions[1] + 48],
                                "magic_icon",
                                hud_sprites)

    hud_buttons.append(rifle_button)
    hud_buttons.append(shotgun_button)
    hud_buttons.append(launcher_button)

    pick_up_spawner = PickUpSpawner(all_pick_up_sprites, collision_grid)
    default_scheme = Scheme()

    player = None

    frame_rates = deque([])
    clock = pygame.time.Clock()        
    running = True
    
    is_main_menu = True
    is_editor = False
    is_character_select = False
    is_view_high_scores = False

    is_game_over = False
    restart_game = False
    win_message = ""

    chosen_character = None

    new_high_score = 0
    has_new_high_score = False

    while running:
        frame_time = clock.tick(60)
        time_delta = frame_time/1000.0

        if is_main_menu:
            is_main_menu_and_index = main_menu.run(screen, fonts, screen_data)
            if is_main_menu_and_index[0] == 0:
                is_main_menu = True
            elif is_main_menu_and_index[0] == 1:
                is_main_menu = False
                is_character_select = True
            elif is_main_menu_and_index[0] == 3:
                is_main_menu = False
                is_view_high_scores = True
            elif is_main_menu_and_index[0] == 2:
                is_main_menu = False
                is_editor = True
            
        elif is_character_select:
            results = character_select.run(screen)
            if results[0] == 1:  # back
                is_main_menu = True
                is_character_select = False
            elif results[0] == 2:  # picked character
                is_main_menu = False
                is_character_select = False
                selected_character_index = results[1]
                chosen_character = characters[selected_character_index]
                player = Player(chosen_character,
                                tiled_level.find_player_start(),
                                tiled_level, default_scheme,
                                hud_buttons,
                                collision_grid,
                                all_projectile_sprites,
                                player_sprites)

                players.append(player)
            else:
                pass

        elif is_view_high_scores:
            results = view_high_score_menu.run(screen)
            if results[0] == 1:  # back
                is_main_menu = True
                is_view_high_scores = False
            else:
                pass

        elif is_editor:
            screen_data.set_editor_active()
            running = editor.run(screen,
                                 background,
                                 all_tile_sprites,
                                 all_top_tile_sprites,
                                 editor_hud_rect,
                                 time_delta)
            
        else:
            if restart_game:
                restart_game = False

                new_high_score = 0

                for monster in monsters:
                    monster.remove_from_grid()

                for player in players:
                    player.remove_from_grid()

                for projectile in all_projectile_sprites.sprites():
                    projectile.remove_from_grid()

                for pick_up in all_pick_up_sprites.sprites():
                    pick_up.remove_from_grid()

                # clear all stuff
                players[:] = []
                monsters[:] = []
                onscreen_monsters[:] = []
                all_monster_sprites.empty()
                all_projectile_sprites.empty()
                all_pick_up_sprites.empty()
                player_sprites.empty()

                is_game_over = False

                player = Player(chosen_character,
                                tiled_level.find_player_start(),
                                tiled_level,
                                Scheme(),
                                hud_buttons,
                                collision_grid,
                                all_projectile_sprites,
                                player_sprites)

                players.append(player)
                tiled_level.reset_guards()
                  
            elif is_game_over:
                pass
            else:
                pass

            if player is not None and player.health <= 0:
                is_game_over = True
                win_message = "You have been defeated!"
                
            if len(monsters) == 0 and not player.should_die:
                player.check_and_save_high_score()
                if player.has_new_high_score:
                    new_high_score = player.score
                    has_new_high_score = True
                is_game_over = True
                win_message = "You survived!"

            # handle UI and inout events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if is_game_over:
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            restart_game = True
                for player in players:
                    player.process_event(event)

            health_bar.update(player.health, player.max_health)
            mana_bar.update(player.mana, player.max_mana)

            tiled_level.update_offset_position(player.position, all_tile_sprites, all_top_tile_sprites)

            all_pick_up_sprites.update(tiled_level)

            for player in players:
                player.update_sprite(time_delta)
                player.update_movement_and_collision(time_delta, tiled_level, monsters)
                if player.should_die and player.has_new_high_score:
                    new_high_score = player.score
                    has_new_high_score = True
                
            players[:] = [player for player in players if not player.should_die]

            for monster in monsters:
                monster.update_movement_and_collision(time_delta, player, pick_up_spawner)
                monster.update_sprite(time_delta)
            monsters[:] = [monster for monster in monsters if not monster.is_dead]
            onscreen_monsters[:] = [monster for monster in monsters if monster.is_on_screen]

            all_projectile_sprites.update(tiled_level, time_delta)

            collision_grid.update_shape_grid_positions()
            collision_grid.check_collisions()

            for collided_shape in collision_grid.shapes_collided_this_frame:
                if collided_shape.owner is not None:
                    collided_shape.owner.react_to_collision()
            
            screen.blit(background, (0, 0))  # draw the background

            all_tile_sprites.draw(screen)
            all_pick_up_sprites.draw(screen)
            all_monster_sprites.draw(screen)
            player_sprites.draw(screen)
            all_projectile_sprites.draw(screen)
            all_top_tile_sprites.draw(screen)

            # player.draw_collision_shape(screen, player.position, (screen_data.play_area[0]/2,
            #                                                       screen_data.play_area[1]/2))
            #
            # for monster in monsters:
            #     monster.draw_collision_shape(screen, player.position, (screen_data.play_area[0]/2,
            #                                                            screen_data.play_area[1]/2))
            #
            # for tile in tiled_level.all_tile_sprites.sprites():
            #     tile.draw_collision_shapes(screen, player.position, (screen_data.play_area[0]/2,
            #                                                            screen_data.play_area[1]/2))

            # noinspection PyArgumentList
            pygame.draw.rect(screen, pygame.Color(100, 100, 100), hud_rect, 0)  # draw the hud
            hud_sprites.draw(screen)
            health_bar.draw(screen, small_font)
            mana_bar.draw(screen, small_font)
            # noinspection PyArgumentList
            player_name_hud_text = small_font.render(chosen_character.name, True, pygame.Color(255, 255, 255))
            screen.blit(player_name_hud_text,
                        player_name_hud_text.get_rect(x=screen_data.hud_dimensions[0] * 0.8,
                                                      centery=screen_data.screen_size[1] * 0.835))
            # noinspection PyArgumentList
            player_level_hud_text = small_font.render("Level: " + str(player.level), True, pygame.Color(255, 255, 255))
            screen.blit(player_level_hud_text,
                        player_level_hud_text.get_rect(x=screen_data.hud_dimensions[0] * 0.8,
                                                       centery=screen_data.screen_size[1] * 0.95))
            # noinspection PyArgumentList
            player_xp_hud_text = small_font.render("XP: " + str(player.xp) + "/" + str(int(player.xp_for_next_level())),
                                                   True,
                                                   pygame.Color(255, 255, 255))
            screen.blit(player_xp_hud_text, player_xp_hud_text.get_rect(x=screen_data.hud_dimensions[0] * 0.875,
                                                                        centery=screen_data.screen_size[1] * 0.95))

            score_string = "Score: " + "{:,}".format(player.score)
            # noinspection PyArgumentList
            score_text_render = fonts[5].render(score_string, True, pygame.Color(255, 255, 255))
            screen.blit(score_text_render, score_text_render.get_rect(x=screen_data.hud_dimensions[0] * 0.05,
                                                                      centery=screen_data.screen_size[1] * 0.05))

            monsters_string = "Monsters Left: " + "{:,}".format(len(monsters))
            # noinspection PyArgumentList
            monsters_text_render = fonts[5].render(monsters_string, True, pygame.Color(255, 255, 255))
            screen.blit(monsters_text_render, monsters_text_render.get_rect(x=screen_data.hud_dimensions[0] * 0.7,
                                                                            centery=screen_data.screen_size[1] * 0.05))

            if time_delta > 0.0:
                if len(frame_rates) < 20:
                    frame_rates.append(1.0/time_delta)
                else:
                    frame_rates.popleft()
                    frame_rates.append(1.0/time_delta)
                    
                fps = sum(frame_rates)/len(frame_rates)
                fps_string = "FPS: " + "{:.2f}".format(fps)
                # noinspection PyArgumentList
                fps_test_render = fonts[1].render(fps_string, True, pygame.Color(255, 255, 255))
                screen.blit(fps_test_render, fps_test_render.get_rect(centerx=screen_data.hud_dimensions[0] * 0.5,
                                                                      centery=24))

            if is_game_over:
                # noinspection PyArgumentList
                win_message_text_render = large_font.render(win_message, True, pygame.Color(255, 255, 255))
                win_message_text_render_rect = win_message_text_render.get_rect(centerx=x_screen_size/2,
                                                                                centery=(y_screen_size/2)-128)

                if has_new_high_score:
                    # noinspection PyArgumentList
                    high_score_text_render = font.render("New High Score: " + str(new_high_score),
                                                         True, pygame.Color(255, 200, 150))
                    high_score_text_render_rect = high_score_text_render.get_rect(centerx=x_screen_size/2,
                                                                                  centery=(y_screen_size/2)-76)
                    screen.blit(high_score_text_render, high_score_text_render_rect)
                # noinspection PyArgumentList
                play_again_text_render = font.render("Play Again? Press 'Y' to restart",
                                                     True, pygame.Color(255, 255, 255))
                play_again_text_render_rect = play_again_text_render.get_rect(centerx=x_screen_size/2,
                                                                              centery=(y_screen_size/2)-40)
                screen.blit(win_message_text_render, win_message_text_render_rect)
                
                screen.blit(play_again_text_render, play_again_text_render_rect)

        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
