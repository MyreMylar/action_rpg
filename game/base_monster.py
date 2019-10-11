import math
import random
import pygame

from collision.collision_shapes import CollisionCircle
from collision.collision_handling import CollisionNoHandler, CollisionRubHandler
from game.game_collision_types import GameCollisionType
from collision.drawable_collision_shapes import DrawableCollisionCircle


class MonsterPath:
    def __init__(self):
        self.start_waypoint = [0, 0]
        self.waypoints = []
        self.waypoint_radius = 32


class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, monster_id, start_pos, sprite_map, all_monster_sprites, play_area, tiled_level,
                 collision_grid, *groups):

        super().__init__(*groups)
        self.id = monster_id
        self.start_pos = start_pos
        self.play_area = play_area
        self.tiled_level = tiled_level
        self.score = 100
        self.xp = 25
        self.collision_grid = collision_grid

        self.point_cost = 10  # point cost
        if self.id == "goblin":
            self.sprite_map_row = 0
            self.walk_cycle_length = 4
        elif self.id == "ent":
            self.sprite_map_row = 1
            self.walk_cycle_length = 8
        elif self.id == "spider":
            self.sprite_map_row = 2
            self.walk_cycle_length = 7

        self.anim_stand = sprite_map[0][self.sprite_map_row]
        self.walk_anim_speed = 64.0 / self.walk_cycle_length
        self.walk_cycle = []
        for anim_index in range(0, self.walk_cycle_length):
            self.walk_cycle.append(sprite_map[anim_index][self.sprite_map_row])

        self.attack_time_delay = 0.5

        self.sprite_rot_centre_offset = [0.0, 0.0]

        self.image = self.anim_stand.copy()
        # self.sprite = pygame.sprite.Sprite()
        self.test_collision_sprite = pygame.sprite.Sprite()

        self.rect = self.image.get_rect()

        self.rect.center = self.start_pos

        self.position = [float(self.rect.center[0]), float(self.rect.center[1])]

        self.screen_position = [0, 0]
        self.screen_position[0] = self.position[0]
        self.screen_position[1] = self.position[1]

        self.collide_radius = 20

        # we do collisions in world space
        self.collision_circle = CollisionCircle(self.position[0], self.position[1], self.collide_radius,
                                                {GameCollisionType.PLAYER_WEAPON: CollisionNoHandler(),
                                                 GameCollisionType.TILE: CollisionRubHandler(),
                                                 GameCollisionType.PLAYER: CollisionRubHandler(),
                                                 GameCollisionType.MONSTER: CollisionRubHandler()},
                                                GameCollisionType.MONSTER,
                                                [GameCollisionType.PLAYER_WEAPON,
                                                 GameCollisionType.TILE,
                                                 GameCollisionType.PLAYER,
                                                 GameCollisionType.MONSTER])
        self.collision_circle.set_owner(self)
        self.collision_grid.add_new_shape_to_grid(self.collision_circle)

        self.drawable_circle = DrawableCollisionCircle(self.collision_circle)

        self.update_screen_position(self.tiled_level.position_offset)

        self.change_direction_time = 5.0
        self.change_direction_accumulator = 0.0

        self.next_way_point = self.get_random_point_in_radius_of_point([500, 400], 96)

        x_dist = float(self.next_way_point[0]) - float(self.position[0])
        y_dist = float(self.next_way_point[1]) - float(self.position[1])
        self.distance_to_next_way_point = math.sqrt((x_dist * x_dist) + (y_dist * y_dist))
        self.current_vector = [x_dist / self.distance_to_next_way_point,
                               y_dist / self.distance_to_next_way_point]

        self.old_facing_angle = 0.0
        self.rotate_sprite(self)

        self.should_die = False
        self.is_dead = False

        self.sprite_needs_update = True
        self.all_monster_sprites = all_monster_sprites
        self.is_on_screen = False

        self.health = 100

        self.slow_down_percentage = 1.0

        self.is_wandering_aimlessly = True
        self.random_target_change_time = random.uniform(3.0, 15.0)
        self.random_target_change_acc = 0.0

        self.time_to_home_in_on_player = False
        self.monster_home_on_target_time = random.uniform(0.3, 1.5)
        self.monster_home_on_target_acc = 0.0

        self.is_time_to_start_attack = True
        self.attack_time_acc = 0.0
        self.attack_time_delay = 3.0

        self.is_attacking = False
        self.should_do_attack_damage = False
        self.attack_anim_acc = 0.0
        self.attack_anim_total_time = 0.8

        self.attack_damage = 15

        self.sprite_flash_acc = 0.0
        self.sprite_flash_time = 0.15
        self.should_flash_sprite = False
        self.active_flash_sprite = False

        self.flash_sprite = pygame.sprite.Sprite()

        self.player_distance = 1000

        self.air_timer = 0.0
        self.air_velocity_vector = [0.0, 0.0]

        self.attack_range = 86.0

        self.collision_obj_rects = []
        self.collision_obj_rect = pygame.Rect(0.0, 0.0, 2.0, 2.0)
        self.max_coll_handling_attempts = 10

        self.move_accumulator = 0.0

        self.move_speed = 0.0
        self.idle_move_speed = 0.0
        self.attack_move_speed = 0.0

    def draw_collision_shape(self, screen, camera_position, camera_half_dimensions):
        self.drawable_circle.update_collided_colours()
        self.drawable_circle.draw(screen, camera_position, camera_half_dimensions)

    def react_to_collision(self):
        for shape in self.collision_circle.collided_shapes_this_frame:
            if shape.game_type == GameCollisionType.TILE or shape.game_type == GameCollisionType.PLAYER \
                    or shape.game_type == GameCollisionType.MONSTER:
                self.position[0] = self.collision_circle.x
                self.position[1] = self.collision_circle.y

    def fling_monster(self, vector, time):
        self.air_timer = time
        self.air_velocity_vector = vector

    def update_sprite(self, time_delta):
        if self.sprite_needs_update:
            self.sprite_needs_update = False
            self.image = self.image

        if self.should_flash_sprite and not self.should_die and not self.is_dead:
            self.sprite_flash_acc += time_delta
            if self.sprite_flash_acc > self.sprite_flash_time:
                self.sprite_flash_acc = 0.0
                self.should_flash_sprite = False
                self.active_flash_sprite = False
                self.all_monster_sprites.remove(self.flash_sprite)
            else:
                lerp_value = self.sprite_flash_acc / self.sprite_flash_time
                flash_alpha = self.lerp(255, 0, lerp_value)
                flash_image = self.image.copy()
                flash_image.fill((0, 0, 0, flash_alpha), None, pygame.BLEND_RGBA_MULT)
                flash_image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_ADD)
                self.flash_sprite.image = flash_image
                self.flash_sprite.rect = self.flash_sprite.image.get_rect()
                self.flash_sprite.rect.center = self.screen_position
                if not self.active_flash_sprite:
                    self.all_monster_sprites.add(self.flash_sprite)
                    self.active_flash_sprite = True

    def attack(self, time_delta, player):
        self.attack_anim_acc += time_delta
        if self.attack_anim_acc > self.attack_anim_total_time:
            self.attack_anim_acc = 0.0
            self.is_attacking = False
        elif self.attack_anim_acc > (self.attack_anim_total_time * 0.75):
            pass  # finish attack frame
        elif self.attack_anim_acc > (self.attack_anim_total_time * 0.5):
            if self.should_do_attack_damage:
                self.should_do_attack_damage = False
                player.take_damage(self.attack_damage)
        elif self.attack_anim_acc > (self.attack_anim_total_time * 0.25):
            pass  # start attack frame

    def update_movement_and_collision(self, time_delta, player, pick_up_spawner):
        if player is not None:
            player_x_dist = float(player.position[0]) - float(self.position[0])
            player_y_dist = float(player.position[1]) - float(self.position[1])
            self.player_distance = math.sqrt((player_x_dist ** 2) + (player_y_dist ** 2))

        if self.health <= 0:
            self.should_die = True

        if self.air_timer > 0.0:
            self.distance_to_next_way_point = 0.0
            self.air_timer -= time_delta
            if self.air_timer < 0.0:
                self.air_timer = 0.0

            self.position[0] += (self.air_velocity_vector[0] * time_delta)
            self.position[1] += (self.air_velocity_vector[1] * time_delta)

        elif self.is_wandering_aimlessly and player is not None and not player.should_die:
            self.move_speed = self.idle_move_speed

            if self.player_distance < 256.0:
                self.is_wandering_aimlessly = False
            elif self.random_target_change_acc < self.random_target_change_time:
                self.random_target_change_acc += time_delta
            else:
                self.random_target_change_acc = 0.0
                self.random_target_change_time = random.uniform(3.0, 15.0)

                self.next_way_point = self.get_random_point_in_world()

                x_dist = float(self.next_way_point[0]) - float(self.position[0])
                y_dist = float(self.next_way_point[1]) - float(self.position[1])
                self.distance_to_next_way_point = math.sqrt((x_dist * x_dist) + (y_dist * y_dist))
                self.current_vector = [x_dist / self.distance_to_next_way_point,
                                       y_dist / self.distance_to_next_way_point]

                self.rotate_sprite(self)

        elif not self.is_wandering_aimlessly and player is not None and not player.should_die:
            self.move_speed = self.attack_move_speed

            if self.monster_home_on_target_acc < self.monster_home_on_target_time:
                self.monster_home_on_target_acc += time_delta
            else:
                self.monster_home_on_target_acc = 0.0
                self.monster_home_on_target_time = random.uniform(0.3, 1.5)
                self.time_to_home_in_on_player = True

            if self.time_to_home_in_on_player:
                self.time_to_home_in_on_player = False

                if self.player_distance > 384.0:
                    self.is_wandering_aimlessly = True
                else:
                    x_dist = float(player.position[0]) - float(self.position[0])
                    y_dist = float(player.position[1]) - float(self.position[1])
                    self.distance_to_next_way_point = (math.sqrt((x_dist * x_dist) + (y_dist * y_dist)))
                    self.current_vector = [x_dist / self.distance_to_next_way_point,
                                           y_dist / self.distance_to_next_way_point]
                    # calculate a position in attack range minus the rough size
                    # of the sprites radius so we are going from edge to edge
                    self.distance_to_next_way_point -= (self.attack_range - self.collide_radius - player.collide_radius)
                    self.rotate_sprite(self)

            if self.attack_time_acc < self.attack_time_delay:
                self.attack_time_acc += time_delta
            else:
                self.attack_time_acc = 0.0
                self.is_time_to_start_attack = True

            if self.player_distance <= self.attack_range and self.is_time_to_start_attack:
                self.is_time_to_start_attack = False
                self.is_attacking = True
                self.should_do_attack_damage = True

        if self.air_timer == 0.0 and self.is_attacking:
            self.attack(time_delta, player)

        if self.air_timer == 0.0 and self.distance_to_next_way_point > 0.0:
            self.position[0] += (self.current_vector[0] * time_delta * self.move_speed)
            self.position[1] += (self.current_vector[1] * time_delta * self.move_speed)
            self.distance_to_next_way_point -= time_delta * self.move_speed
            self.move_accumulator += time_delta * self.move_speed

        # move
        if self.on_screen():
            if not self.is_on_screen:
                self.is_on_screen = True
                self.all_monster_sprites.add(self)

            self.update_screen_position(self.tiled_level.position_offset)

            # if walking about
            walk_cycle_index = int(self.move_accumulator / self.walk_anim_speed)
            if walk_cycle_index >= len(self.walk_cycle):
                self.move_accumulator = 0.0
                walk_cycle_index = 0
            self.image = pygame.transform.rotate(self.walk_cycle[walk_cycle_index], self.old_facing_angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.rot_point([self.screen_position[0],
                                               self.screen_position[1] + self.sprite_rot_centre_offset[1]],
                                              self.screen_position, -self.old_facing_angle)

        else:
            if self.is_on_screen:
                self.is_on_screen = False
                self.all_monster_sprites.remove(self)
                if self.active_flash_sprite:
                    self.all_monster_sprites.remove(self.flash_sprite)
                    self.active_flash_sprite = False

        self.collision_circle.set_position(self.position)

        if self.should_die:
            self.should_die = False
            self.is_dead = True
            if self.active_flash_sprite:
                self.all_monster_sprites.remove(self.flash_sprite)
                self.active_flash_sprite = False
            self.all_monster_sprites.remove(self)
            self.try_pick_up_spawn(pick_up_spawner)
            player.add_score(self.score)
            player.add_xp(self.xp)
            self.collision_grid.remove_shape_from_grid(self.collision_circle)

    def remove_from_grid(self):
        self.collision_grid.remove_shape_from_grid(self.collision_circle)

    def on_screen(self):
        if self.position[0] + self.rect[2] / 2 > self.tiled_level.position_offset[0] and self.position[0] - \
                self.rect[2] / 2 < self.tiled_level.position_offset[0] + self.play_area[0]:
            if self.position[1] + self.rect[3] / 2 > self.tiled_level.position_offset[1] and self.position[1] - \
                    self.rect[3] / 2 < self.tiled_level.position_offset[1] + self.play_area[1]:
                return True
        return False

    def update_screen_position(self, world_offset):
        self.screen_position[0] = self.position[0] - world_offset[0]
        self.screen_position[1] = self.position[1] - world_offset[1]

        self.collision_circle.x = self.screen_position[0]
        self.collision_circle.y = self.screen_position[1]

    @staticmethod
    def get_random_point_in_radius_of_point(point, radius):
        t = 2 * math.pi * random.random()
        u = random.random() + random.random()
        if u > 1:
            r = 2 - u
        else:
            r = u
        return [point[0] + radius * r * math.cos(t), point[1] + radius * r * math.sin(t)]

    def set_average_speed(self, average_speed):
        self.move_speed = random.randint(int(average_speed * 0.75), int(average_speed * 1.25))
        return self.move_speed

    def take_damage(self, damage):
        self.health -= damage.amount
        self.should_flash_sprite = True

    def get_random_point_in_world(self):
        random_x = random.randint(32, self.tiled_level.level_pixel_size[0] - 32)
        random_y = random.randint(32, self.tiled_level.level_pixel_size[1] - 32)
        return [random_x, random_y]

    def rotate_sprite(self, sprite_to_rot):
        direction_magnitude = math.sqrt(
            self.current_vector[0] * self.current_vector[0] + self.current_vector[1] * self.current_vector[1])

        if direction_magnitude > 0.0:
            unit_dir_vector = [self.current_vector[0] / direction_magnitude,
                               self.current_vector[1] / direction_magnitude]
            self.old_facing_angle = math.atan2(-unit_dir_vector[0], -unit_dir_vector[1]) * 180 / math.pi

        return sprite_to_rot

    def try_pick_up_spawn(self, pickup_spawner):
        pickup_spawner.try_spawn(self.position)

    @staticmethod
    def rot_point(point, axis, ang):
        """ Orbit. calculates the new loc for a point that rotates a given num of degrees around an axis point,
        +clockwise, -anticlockwise -> tuple x,y
        """
        ang -= 90
        x, y = point[0] - axis[0], point[1] - axis[1]
        radius = math.sqrt(x * x + y * y)  # get the distance between points

        r_ang = math.radians(ang)  # convert ang to radians.

        h = axis[0] + (radius * math.cos(r_ang))
        v = axis[1] + (radius * math.sin(r_ang))

        return [h, v]

    @staticmethod
    def lerp(a, b, c):
        return (c * b) + ((1.0 - c) * a)

    @staticmethod
    def get_distance(from_x, from_y, to_x, to_y):
        dx = from_x - to_x
        dy = from_y - to_y
        return math.sqrt((dx ** 2) + (dy ** 2))
