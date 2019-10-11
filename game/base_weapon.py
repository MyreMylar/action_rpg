import pygame


class WeaponAnimation:
    def __init__(self, sprite_sheet, y_start):
        self.step_left = sprite_sheet.subsurface(pygame.Rect(0, y_start, 64, 64))
        self.stand = sprite_sheet.subsurface(pygame.Rect(64, y_start, 64, 64))
        self.step_right = sprite_sheet.subsurface(pygame.Rect(128, y_start, 64, 64))

        # self.fire_1 = sprite_sheet.subsurface(pygame.Rect(0, yStart+64, 64, 64))
        # self.fire_2 = sprite_sheet.subsurface(pygame.Rect(64, yStart+64, 64, 64))
        # self.fire_3 = sprite_sheet.subsurface(pygame.Rect(128, yStart+64, 64, 64))

        self.fire_sprites = []
        self.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(0, y_start + 64, 64, 64)))
        self.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(64, y_start + 64, 64, 64)))
        self.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(128, y_start + 64, 64, 64)))

        self.fire_sprites.append(sprite_sheet.subsurface(pygame.Rect(0, y_start + 64, 64, 64)))

        self.centre_offset = [0.0, 0.0]
        self.firing_centre_offset = [0.0, 0.0]


class BaseWeapon:
    def __init__(self, player, sprite_sheet, y_sheet_start):
        self.anim_set = WeaponAnimation(sprite_sheet, y_sheet_start)

        self.player = player

        self.fire_rate_acc = 0.0
        self.fire_rate = 1.0
        self.can_fire = True
        self.fire_anim_speed = 0.5

        self.player_position = [0, 0]
        self.current_aim_vector = [0, 0]

        self.barrel_forward_offset = 32
        self.barrel_side_offset = 6

        self.ammo_count = -1
        self.mana_cost = -1

        self.projectile_vector = [0.0, 0.0]
        self.barrel_exit_pos = [0.0, 0.0]

    def deduct_mana_cost(self):
        self.player.mana -= self.mana_cost

    def on_level_up(self):
        pass

    def update(self, time_delta, player_position, current_aim_vector):
        if self.fire_rate_acc < self.fire_rate:
            self.fire_rate_acc += time_delta
        else:
            if self.ammo_count != 0:
                if self.mana_cost == -1:
                    self.can_fire = True
                elif self.mana_cost <= self.player.mana:
                    self.can_fire = True

        self.player_position = player_position
        self.current_aim_vector = current_aim_vector

        # calculate the position where the projectiles should leave the weapon
        b_x_fwd_offset = self.current_aim_vector[0] * self.barrel_forward_offset
        b_x_side_offset = self.current_aim_vector[1] * self.barrel_side_offset
        barrel_x_pos = self.player_position[0] + b_x_fwd_offset - b_x_side_offset

        b_y_fwd_offset = self.current_aim_vector[1] * self.barrel_forward_offset
        b_y_side_offset = self.current_aim_vector[0] * self.barrel_side_offset
        barrel_y_pos = self.player_position[1] + b_y_fwd_offset + b_y_side_offset
        self.barrel_exit_pos = [barrel_x_pos, barrel_y_pos]

    def set_projectile_vector(self, projectile_vec):
        self.projectile_vector = projectile_vec

    def fire(self, monsters):
        pass
