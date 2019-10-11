import math
import pygame
from pygame.locals import *

from collision.collision_shapes import CollisionCircle
from collision.collision_handling import CollisionNoHandler, CollisionRubHandler
from game.game_collision_types import GameCollisionType
from collision.drawable_collision_shapes import DrawableCollisionCircle

# ------------------------------------------
# import your new weapon code file here
# ------------------------------------------
from game.bow_weapon import BowWeapon
from game.sword_weapon import SwordWeapon
from game.magic_weapon import MagicWeapon


class Scheme:
    def __init__(self):
        self.bow = K_1
        self.sword = K_2
        self.magic = K_3


class Player(pygame.sprite.Sprite):
    def __init__(self, character, start_pos, tiled_level, control_scheme, hud_buttons,
                 collision_grid, projectile_sprite_group, player_sprites):
        super().__init__(player_sprites)
        self.collision_grid = collision_grid
        self.player_sprites = player_sprites
        self.character = character
        self.xp = 0
        self.level = 1
        self.score = 0
        self.scheme = control_scheme
        self.image_name = "images/player_2.png"
        self.original_image = pygame.image.load(self.image_name)
        self.sprite_sheet = self.original_image.copy()

        self.hud_buttons = hud_buttons

        self.player_world_target = [0.0, 0.0]

        # ------------------------------------------
        # Add new weapon objects here
        # ------------------------------------------
        self.bow_weapon = BowWeapon(self, self.sprite_sheet, self.collision_grid, projectile_sprite_group)
        self.sword_weapon = SwordWeapon(self, self.sprite_sheet, self.collision_grid, projectile_sprite_group)
        self.magic_weapon = MagicWeapon(self, self.sprite_sheet)
        self.active_weapon = self.bow_weapon

        for button in self.hud_buttons:
            if button.button_image_name == "bow_icon":
                button.set_selected()
            else:
                button.clear_selected()

        # self.sprite = pygame.sprite.Sprite()
        self.test_collision_sprite = pygame.sprite.Sprite()
        self.flash_sprite = pygame.sprite.Sprite()
        self.image = self.active_weapon.anim_set.stand
        self.rect = self.active_weapon.anim_set.stand.get_rect()
        self.rect.center = start_pos

        self.sprite_rot_centre_offset = [0.0, 11.0]
        self.speed = 0.0
        self.acceleration = 200.0
        self.max_speed = 250.0

        self.collide_radius = 18

        self.max_health = 100 + (50 * self.level * (self.character.strength / 20))
        self.health = self.max_health

        self.max_mana = 50.0 + (50.0 * self.level * (self.character.magic / 20))
        self.mana = self.max_mana
        self.mana_recharge = 1.0 + (1.0 * self.level * (self.character.magic / 20))
        
        self.should_die = False

        self.move_accumulator = 0.0
       
        self.position = [float(self.rect.center[0]), float(self.rect.center[1])]
        self.player_move_target = self.position
        self.distance_to_move_target = 0.0
        self.current_vector = [0.0, -1.0]
        self.new_facing_angle = 0

        self.screen_position = [0, 0]
        self.screen_position[0] = self.position[0]
        self.screen_position[1] = self.position[1]

        self.update_screen_position(tiled_level.position_offset)

        direction_magnitude = math.sqrt(self.current_vector[0] ** 2 + self.current_vector[1] ** 2)
        if direction_magnitude > 0.0:
            unit_dir_vector = [self.current_vector[0] / direction_magnitude,
                               self.current_vector[1] / direction_magnitude]
            self.new_facing_angle = math.atan2(-unit_dir_vector[0], -unit_dir_vector[1]) * 180 / math.pi

        self.old_facing_angle = self.new_facing_angle

        self.rect.center = self.rot_point([self.screen_position[0],
                                           self.screen_position[1] + self.sprite_rot_centre_offset[1]],
                                          self.screen_position, -self.new_facing_angle)

        self.left_mouse_held = False
        self.right_mouse_held = False

        self.per_bullet_damage = 25
        
        self.player_fire_target = [10000, 10000]

        self.switch_to_bow = False
        self.switch_to_sword = False
        self.switch_to_magic = False
       
        self.sprite_flash_acc = 0.0
        self.sprite_flash_time = 0.15
        self.should_flash_sprite = False
        self.sprite_flashing = False

        self.is_collided = False

        self.firing = False
        self.firing_timer = 0.0

        self.has_new_high_score = False

        self.should_draw_collision_obj = False
        self.collision_obj_rects = []
        self.collision_obj_rect = pygame.Rect(0.0, 0.0, 2.0, 2.0)

        self.world_click_pos = [0, 0]

        # we do collisions in world space
        self.collision_circle = CollisionCircle(self.position[0], self.position[1], self.collide_radius,
                                                {GameCollisionType.MONSTER_WEAPON: CollisionNoHandler(),
                                                 GameCollisionType.TILE: CollisionRubHandler(),
                                                 GameCollisionType.MONSTER: CollisionRubHandler(),
                                                 GameCollisionType.PICKUP: CollisionNoHandler()},
                                                GameCollisionType.PLAYER,
                                                [GameCollisionType.MONSTER_WEAPON,
                                                 GameCollisionType.TILE,
                                                 GameCollisionType.MONSTER,
                                                 GameCollisionType.PICKUP])
        self.collision_circle.set_owner(self)
        self.collision_grid.add_new_shape_to_grid(self.collision_circle)

        self.drawable_circle = DrawableCollisionCircle(self.collision_circle)

    def draw_collision_shape(self, screen, camera_position, camera_half_dimensions):
        self.drawable_circle.update_collided_colours()
        self.drawable_circle.draw(screen, camera_position, camera_half_dimensions)

    def remove_from_grid(self):
        self.collision_grid.remove_shape_from_grid(self.collision_circle)

    def react_to_collision(self):
        for shape in self.collision_circle.collided_shapes_this_frame:
            if shape.game_type == GameCollisionType.MONSTER:
                self.position[0] = self.collision_circle.x
                self.position[1] = self.collision_circle.y
            elif shape.game_type == GameCollisionType.TILE:
                self.position[0] = self.collision_circle.x
                self.position[1] = self.collision_circle.y

    def add_xp(self, xp):
        self.xp += xp
        
    def add_score(self, score):
        self.score += score

    def xp_for_next_level(self):
        # 2 = 100
        # 3 = 250
        # 4 = 500
        # 5 = 850
        # 6 = 1300
        # 7 = 1850
        return 50 + (100 * ((self.level * self.level)/2))

    def update_screen_position(self, world_offset):
        self.screen_position[0] = self.position[0] - world_offset[0]
        self.screen_position[1] = self.position[1] - world_offset[1]
    
    def update_sprite(self, time_delta):
        if self.should_flash_sprite:
            self.should_flash_sprite = False
            self.player_sprites.add(self.flash_sprite)
            self.sprite_flashing = True

        if self.sprite_flashing:
            self.sprite_flash_acc += time_delta
            if self.sprite_flash_acc > self.sprite_flash_time:
                self.sprite_flash_acc = 0.0
                self.sprite_flashing = False
                self.flash_sprite.kill()
            else:
                lerp_value = self.sprite_flash_acc / self.sprite_flash_time
                flash_alpha = self.lerp(255, 0, lerp_value)
                flash_image = self.image.copy()
                flash_image.fill((0, 0, 0, flash_alpha), None, pygame.BLEND_RGBA_MULT)
                flash_image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_ADD)
                self.flash_sprite.image = flash_image
                self.flash_sprite.rect = self.flash_sprite.image.get_rect()
                
                anim_centre_offset = self.active_weapon.anim_set.centre_offset
                if self.firing:
                    anim_centre_offset = self.active_weapon.anim_set.firing_centre_offset
                y_pos = self.screen_position[1]+self.sprite_rot_centre_offset[1]+anim_centre_offset[1]
                self.flash_sprite.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                               self.screen_position, -self.new_facing_angle)

    def process_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_mouse_held = True
            if event.button == 3:
                self.right_mouse_held = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.left_mouse_held = False
            if event.button == 3:
                self.right_mouse_held = False
        if event.type == KEYDOWN:     
            if event.key == self.scheme.bow:
                self.switch_to_bow = True
            if event.key == self.scheme.sword:
                self.switch_to_sword = True
            if event.key == self.scheme.magic:
                self.switch_to_magic = True

    def check_and_save_high_score(self):
        if self.score > self.character.score:
            self.has_new_high_score = True
            self.character.score = self.score
            self.character.save()

    def on_level_up(self):
        self.level += 1
        old_max_health = self.max_health
        self.max_health = 100 + (50 * self.level * (self.character.strength / 20))
        self.health += (self.max_health - old_max_health)  # add change in health to current health
        self.max_mana = 50 + (50 * self.level * (self.character.magic / 20))
        self.acceleration = 200.0 + (25 * self.level * (self.character.dexterity/20))
        self.max_speed = 200.0 + (25 * self.level * (self.character.dexterity / 20))

        self.bow_weapon.on_level_up()
        self.sword_weapon.on_level_up()
        self.magic_weapon.on_level_up()
            
    def update_movement_and_collision(self, time_delta, tiled_level, monsters):
        if self.xp_for_next_level() <= self.xp:
            self.on_level_up()

        if self.health == 0:
            self.should_die = True
            self.check_and_save_high_score()

        self.mana += self.mana_recharge * time_delta
        if self.mana > self.max_mana:
            self.mana = self.max_mana

        if self.switch_to_bow:
            self.switch_to_bow = False
            self.active_weapon = self.bow_weapon

            for button in self.hud_buttons:
                if button.button_image_name == "bow_icon":
                    button.set_selected()
                else:
                    button.clear_selected()

            self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand, self.new_facing_angle)
            self.rect = self.image.get_rect()
            anim_centre_offset = self.active_weapon.anim_set.centre_offset
            y_pos = self.screen_position[1]+self.sprite_rot_centre_offset[1]+anim_centre_offset[1]
            self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                              self.screen_position, -self.new_facing_angle)
            
        if self.switch_to_sword:
            self.switch_to_sword = False
            self.active_weapon = self.sword_weapon

            for button in self.hud_buttons:
                if button.button_image_name == "sword_icon":
                    button.set_selected()
                else:
                    button.clear_selected()

            self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand, self.new_facing_angle)
            self.rect = self.image.get_rect()
            anim_centre_offset = self.active_weapon.anim_set.centre_offset
            y_pos = self.screen_position[1]+self.sprite_rot_centre_offset[1]+anim_centre_offset[1]
            self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                              self.screen_position, -self.new_facing_angle)
               
        if self.switch_to_magic:
            self.switch_to_magic = False
            self.active_weapon = self.magic_weapon

            for button in self.hud_buttons:
                if button.button_image_name == "magic_icon":
                    button.set_selected()
                else:
                    button.clear_selected()

            self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand, self.new_facing_angle)
            self.rect = self.image.get_rect()
            anim_centre_offset = self.active_weapon.anim_set.centre_offset
            y_pos = self.screen_position[1] + self.sprite_rot_centre_offset[1] + anim_centre_offset[1]
            self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                              self.screen_position, -self.new_facing_angle)
            
        fire_this_update = False
        if self.active_weapon.can_fire and self.right_mouse_held:
            fire_this_update = True
            self.player_move_target = self.position
            self.distance_to_move_target = 0.0
            self.active_weapon.fire_rate_acc = 0.0
            self.active_weapon.can_fire = False

            if self.player_fire_target != pygame.mouse.get_pos():
                new_target = pygame.mouse.get_pos()
                x_dist = float(new_target[0]) - float(self.screen_position[0])
                y_dist = float(new_target[1]) - float(self.screen_position[1])
                distance = math.sqrt((x_dist * x_dist) + (y_dist * y_dist))
                if distance > 0.0:
                    self.player_fire_target = new_target
                    self.current_vector = [x_dist / distance, y_dist / distance]
                    direction_magnitude = math.sqrt(self.current_vector[0] ** 2 + self.current_vector[1] ** 2)
                    if direction_magnitude > 0.0:
                        unit_dir_vector = [self.current_vector[0] / direction_magnitude,
                                           self.current_vector[1] / direction_magnitude]
                        self.new_facing_angle = math.atan2(-unit_dir_vector[0], -unit_dir_vector[1]) * 180 / math.pi

                self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand, self.new_facing_angle)
                self.rect = self.image.get_rect()
                anim_centre_offset = self.active_weapon.anim_set.centre_offset
                y_pos = self.screen_position[1]+self.sprite_rot_centre_offset[1]+anim_centre_offset[1]
                self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                  self.screen_position, -self.new_facing_angle)
            
        self.active_weapon.update(time_delta, self.position, self.current_vector)
        barrel_screen_x = float(self.active_weapon.barrel_exit_pos[0] - tiled_level.position_offset[0])
        barrel_screen_y = float(self.active_weapon.barrel_exit_pos[1] - tiled_level.position_offset[1])
        x_dist = float(self.player_fire_target[0]) - barrel_screen_x
        y_dist = float(self.player_fire_target[1]) - barrel_screen_y
        distance = math.sqrt(x_dist**2 + y_dist**2)
        if distance > 0.0:
            projectile_vector = [x_dist/distance, y_dist/distance]
            self.active_weapon.set_projectile_vector(projectile_vector)
        
        if fire_this_update:
            self.active_weapon.fire(monsters)
            self.firing_timer = self.active_weapon.fire_anim_speed
            self.firing = True

        if self.firing:
            anim_progress = self.active_weapon.fire_anim_speed - self.firing_timer
            fire_anim_percentage = anim_progress / self.active_weapon.fire_anim_speed

            number_of_anims = len(self.active_weapon.anim_set.fire_sprites)
            anim_index = max(1, int(fire_anim_percentage * number_of_anims)) - 1

            current_anim = self.active_weapon.anim_set.fire_sprites[anim_index]
            anim_centre_offset = self.active_weapon.anim_set.firing_centre_offset
            self.image = pygame.transform.rotate(current_anim, self.new_facing_angle)
            self.rect = self.image.get_rect()
            y_pos = self.screen_position[1] + self.sprite_rot_centre_offset[1] + anim_centre_offset[1]
            self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                              self.screen_position, -self.new_facing_angle)
                
            self.firing_timer -= time_delta
            if self.firing_timer <= 0.0:
                self.firing_timer = 0.0
                self.firing = False
                
        if self.left_mouse_held:
            self.firing = False
            self.firing_timer = 0.0
            self.world_click_pos = [pygame.mouse.get_pos()[0] + tiled_level.position_offset[0],
                                    pygame.mouse.get_pos()[1] + tiled_level.position_offset[1]]

            # fake quick distance, just to check we are away from target
            click_x_dist = abs(self.world_click_pos[0] - self.player_world_target[0])
            click_y_dist = abs(self.world_click_pos[1] - self.player_world_target[1])
            click_target_dist = click_x_dist + click_y_dist

            if click_target_dist > 2.0:
                new_target = pygame.mouse.get_pos()
                x_dist = float(new_target[0]) - float(self.screen_position[0])
                y_dist = float(new_target[1]) - float(self.screen_position[1])
                distance = math.sqrt((x_dist * x_dist) + (y_dist * y_dist))
                if distance > 0.0:
                    self.player_move_target = new_target
                    self.player_world_target = [self.player_move_target[0] + tiled_level.position_offset[0],
                                                self.player_move_target[1] + tiled_level.position_offset[1]]
                    self.distance_to_move_target = distance
                    self.current_vector = [x_dist / self.distance_to_move_target, y_dist / self.distance_to_move_target]
                    direction_magnitude = math.sqrt(self.current_vector[0] ** 2 + self.current_vector[1] ** 2)
                    if direction_magnitude > 0.0:
                        unit_dir_vector = [self.current_vector[0] / direction_magnitude,
                                           self.current_vector[1] / direction_magnitude]
                        self.new_facing_angle = math.atan2(-unit_dir_vector[0], -unit_dir_vector[1]) * 180 / math.pi

        if self.distance_to_move_target > 0.0:
            self.speed += self.acceleration * time_delta
            if self.speed > self.max_speed:
                self.speed = self.max_speed

            self.position[0] += (self.current_vector[0] * time_delta * self.speed)
            self.position[1] += (self.current_vector[1] * time_delta * self.speed)
            self.move_accumulator += self.speed * time_delta
            self.distance_to_move_target -= self.speed * time_delta

            self.update_screen_position(tiled_level.position_offset)
            
            if not self.firing:
                y_pos = self.screen_position[1] + self.sprite_rot_centre_offset[1]
                if abs(self.move_accumulator) > 64.0:
                    self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand,
                                                         self.new_facing_angle)
                    self.rect = self.image.get_rect()
                    self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                      self.screen_position, -self.new_facing_angle)
                    self.move_accumulator = 0.0
                elif abs(self.move_accumulator) > 48.0:
                    self.image = pygame.transform.rotate(self.active_weapon.anim_set.step_left,
                                                         self.new_facing_angle)
                    self.rect = self.image.get_rect()
                    self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                      self.screen_position, -self.new_facing_angle)
                elif abs(self.move_accumulator) > 32.0:
                    self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand,
                                                         self.new_facing_angle)
                    self.rect = self.image.get_rect()
                    self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                      self.screen_position, -self.new_facing_angle)
                elif abs(self.move_accumulator) > 16.0:
                    self.image = pygame.transform.rotate(self.active_weapon.anim_set.step_right,
                                                         self.new_facing_angle)
                    self.rect = self.image.get_rect()
                    self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                      self.screen_position, -self.new_facing_angle)
                else:
                    self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand,
                                                         self.new_facing_angle)
                    self.rect = self.image.get_rect()
                    self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                      self.screen_position, -self.new_facing_angle)

        else:
            self.update_screen_position(tiled_level.position_offset)
            self.speed = 0.0
            if not self.firing:
                self.image = pygame.transform.rotate(self.active_weapon.anim_set.stand, self.new_facing_angle)
                self.rect = self.image.get_rect()
                y_pos = self.screen_position[1] + self.sprite_rot_centre_offset[1]
                self.rect.center = self.rot_point([self.screen_position[0], y_pos],
                                                  self.screen_position, -self.new_facing_angle)

        self.collision_circle.set_position(self.position)

        if self.should_die:
            self.flash_sprite.kill()
            self.kill()
            self.collision_grid.remove_shape_from_grid(self.collision_circle)

    def add_health(self, health):
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health

    def add_mana(self, mana):
        self.mana += mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.should_flash_sprite = True

    @staticmethod
    def rot_point(point, axis, ang):
        """ Orbit. calculates the new loc for a point that rotates a given num of degrees around an axis point,
        +clockwise, -anticlockwise -> tuple x,y
        """
        ang -= 90
        x, y = point[0] - axis[0], point[1] - axis[1]
        radius = math.sqrt(x*x + y*y)  # get the distance between points

        r_ang = math.radians(ang)       # convert ang to radians.

        h = axis[0] + (radius * math.cos(r_ang))
        v = axis[1] + (radius * math.sin(r_ang))

        return [h, v]

    @staticmethod
    def lerp(a, b, c):
        return (c * b) + ((1.0 - c) * a)


class RespawnPlayer:
    def __init__(self, player):
        self.control_scheme = player.scheme
        self.respawn_timer = 2.0
        self.time_to_spawn = False
        self.has_respawned = False

    def update(self, frame_time_ms):
        self.respawn_timer -= (frame_time_ms / 1000.0)
        if self.respawn_timer < 0.0:
            self.time_to_spawn = True


class PlayerScore:
    def __init__(self, screen_position):
        self.screen_position = screen_position
        self.score = 0
