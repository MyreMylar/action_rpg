import math
import pygame

from game.projectile import Projectile
from game.damage import Damage, DamageType
from collision.collision_shapes import CollisionRect
from collision.collision_handling import CollisionNoHandler
from game.game_collision_types import GameCollisionType


class Sword(Projectile):
    def __init__(self, start_pos, initial_heading_vector, damage, collision_grid, sword_image, *groups):

        super().__init__(*groups)
        self.collision_grid = collision_grid
        self.original_image = sword_image
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.world_rect = self.rect.copy()
        self.rect.center = start_pos

        self.current_vector = [initial_heading_vector[0], initial_heading_vector[1]]

        self.position = [float(self.rect.center[0]), float(self.rect.center[1])]
        self.world_position = [float(self.rect.center[0]), float(self.rect.center[1])]

        self.should_die = False

        self.bullet_speed = 300.0
        self.damage = damage

        self.shot_range = 32.0

        self.collision_rect = CollisionRect(self.rect, 0, {GameCollisionType.MONSTER: CollisionNoHandler(),
                                                           GameCollisionType.TILE: CollisionNoHandler()},
                                            GameCollisionType.PLAYER_WEAPON, [GameCollisionType.MONSTER,
                                                                              GameCollisionType.TILE])
        self.collision_rect.set_owner(self)
        self.collision_grid.add_new_shape_to_grid(self.collision_rect)

    def remove_from_grid(self):
        self.collision_grid.remove_shape_from_grid(self.collision_rect)

    def react_to_collision(self):
        if not self.should_die:
            if len(self.collision_rect.collided_shapes_this_frame) > 0:
                self.should_die = True
                for shape in self.collision_rect.collided_shapes_this_frame:
                    if shape.game_type == GameCollisionType.MONSTER:
                        shape.owner.take_damage(Damage(self.damage, DamageType.PHYSICAL))

    def update_sprite(self, all_bullet_sprites):
        all_bullet_sprites.add(self)
        return all_bullet_sprites

    def calc_facing_angle_rad(self):
        direction_magnitude = math.sqrt(self.current_vector[0] ** 2 + self.current_vector[1] ** 2)
        unit_dir_vector = [0, 0]
        if direction_magnitude > 0.0:
            unit_dir_vector = [self.current_vector[0] / direction_magnitude,
                               self.current_vector[1] / direction_magnitude]
        facing_angle = math.atan2(-unit_dir_vector[0], -unit_dir_vector[1])  # *180/math.pi
        return facing_angle

    def update(self, tiled_level, time_delta):
        if not self.should_die:
            self.shot_range -= time_delta * self.bullet_speed
            self.world_position[0] += (self.current_vector[0] * time_delta * self.bullet_speed)
            self.world_position[1] += (self.current_vector[1] * time_delta * self.bullet_speed)
            self.world_rect.center = self.world_position

            self.position[0] = self.world_position[0] - tiled_level.position_offset[0]
            self.position[1] = self.world_position[1] - tiled_level.position_offset[1]
            self.rect.center = self.position

            # calc facing angle & convert to degrees
            facing_angle = self.calc_facing_angle_rad() * 180 / math.pi

            bullet_centre_position = self.rect.center
            self.image = pygame.transform.rotate(self.original_image, facing_angle)
            self.rect = self.image.get_rect()
            self.rect.center = bullet_centre_position

            # update collision shape position and rotation
            self.collision_rect.set_rotation(facing_angle * math.pi / 180.0)
            self.collision_rect.set_position(self.world_position)

        if self.shot_range <= 0.0:
            self.should_die = True

        if self.should_die:
            self.collision_grid.remove_shape_from_grid(self.collision_rect)
            self.kill()
