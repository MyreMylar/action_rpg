from game.base_weapon import BaseWeapon
from game.sword import Sword
import pygame


class SwordWeapon(BaseWeapon):
    def __init__(self, player, sprite_sheet, collision_grid, projectile_sprite_group):

        player_sprite_y_offset = 128
        super().__init__(player, sprite_sheet, player_sprite_y_offset)

        self.sword_image = pygame.image.load("images/sword.png")

        self.projectile_sprite_group = projectile_sprite_group
        self.collision_grid = collision_grid

        self.anim_set.fire_sprites[:] = []
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(0,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(64,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(128,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(192,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(256,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(320,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(384,
                                                                              player_sprite_y_offset + 64, 64, 128)))
        self.anim_set.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(448,
                                                                              player_sprite_y_offset + 64, 64, 128)))

        self.anim_set.firing_centre_offset = [0.0, 32.0]
        
        self.fire_rate = 0.6
        self.per_hit_damage = 50
        self.on_level_up()

        self.barrel_forward_offset = 32
        self.barrel_side_offset = 0

        self.fire_anim_speed = 0.35

    def on_level_up(self):
        self.per_hit_damage = 25 + (15 * self.player.level * (self.player.character.strength / 20))

    def fire(self, monsters):
        Sword(self.barrel_exit_pos,
              self.current_aim_vector,
              self.per_hit_damage,
              self.collision_grid,
              self.sword_image,
              self.projectile_sprite_group)
