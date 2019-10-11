from game.base_weapon import BaseWeapon
from game.arrow import Arrow

import math
import pygame


class BowWeapon(BaseWeapon):
    def __init__(self, player, sprite_sheet, collision_grid, projectile_sprite_group):

        player_sprite_y_offset = 0
        super().__init__(player, sprite_sheet, player_sprite_y_offset)

        self.projectile_sprite_group = projectile_sprite_group
        self.collision_grid = collision_grid
        self.max_fire_rate = 0.1
        self.fire_rate = 0.8
        self.per_bullet_damage = 25

        self.arrow_image = pygame.image.load("images/arrow.png")

        self.on_level_up()

        # set the offset position where the projectiles should leave the weapon
        #  (this is from the centre of the player sprite)
        self.barrel_forward_offset = 0
        self.barrel_side_offset = 16

    def on_level_up(self):
        self.fire_rate = 0.8 - (0.15 * math.log1p(self.player.level) * (20.0 / self.player.character.dexterity))
        if self.fire_rate < self.max_fire_rate:
            self.fire_rate = self.max_fire_rate

    def fire(self, monsters):
        Arrow(self.barrel_exit_pos, self.projectile_vector,
              self.per_bullet_damage, self.collision_grid, self.arrow_image, self.projectile_sprite_group)
