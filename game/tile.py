import pygame
# import math
import csv
import os

from collision.drawable_collision_shapes import DrawableCompositeShape
from collision.collision_shapes import CompositeCollisionShape
from collision.collision_handling import CollisionNoHandler, CollisionRubHandler
from game.game_collision_types import GameCollisionType


class AISpawn(pygame.sprite.Sprite):
    def __init__(self, image, position, type_id, *groups):
        super().__init__(*groups)
        self.type_id = type_id
        self.position = [0, 0]
        self.position[0] = position[0]
        self.position[1] = position[1]

        self.world_position = [0, 0]
        self.world_position[0] = position[0]
        self.world_position[1] = position[1]
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update_offset_position(self, offset):
        self.position[0] = self.world_position[0] - offset[0]
        self.position[1] = self.world_position[1] - offset[1]
        self.rect.center = self.position


class TileData:
    def __init__(self, file_path, tile_map):
        self.file_path = file_path
        self.tile_map = tile_map
        self.tile_id = os.path.splitext(os.path.basename(file_path))[0]
        self.collidable = False
        self.collide_radius = 26
        self.collision_shapes = []
        self.tile_image = None

    def load_tile_data(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as tileFile:
                reader = csv.reader(tileFile)
                for line in reader:
                    data_type = line[0]
                    if data_type == "isCollidable":
                        self.collidable = bool(int(line[1]))
                    elif data_type == "tileImageCoords":
                        self.tile_image = self.tile_map[int(line[1])][int(line[2])]
                    elif data_type == "rect":
                        top_left_tile_offset = [int(line[1]), int(line[2])]
                        self.collision_shapes.append(["rect",
                                                      top_left_tile_offset,
                                                      pygame.Rect(int(line[1]),
                                                                  int(line[2]),
                                                                  int(line[3])-int(line[1]),
                                                                  int(line[4])-int(line[2]))])
                    elif data_type == "circle":
                        self.collision_shapes.append(["circle",
                                                      [int(line[1]), int(line[2])],
                                                      [int(line[1]), int(line[2])],
                                                      int(line[3])])

                        self.collide_radius = int(line[3])
                       

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, tile_angle, tile_data, layer, collision_grid, *groups):
        super().__init__(*groups)
        self.collision_grid = collision_grid
        self.group_tile_data = tile_data
        self.tile_data = tile_data
        self.world_position = [position[0], position[1]]
        self.position = [position[0], position[1]]
        self.angle = tile_angle
        self.collide_radius = self.group_tile_data.collide_radius
        self.collidable = self.group_tile_data.collidable
        self.tile_id = self.group_tile_data.tile_id
        self.image = pygame.transform.rotate(self.group_tile_data.tile_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.is_visible = False
        self.layer = layer

        self.drawable_collision_shape = None

        if self.collidable:
            self.collision_shape = CompositeCollisionShape(self.world_position[0],
                                                           self.world_position[1],
                                                           (self.rect.width, self.rect.height),
                                                           {GameCollisionType.MONSTER: CollisionRubHandler(),
                                                            GameCollisionType.PLAYER: CollisionRubHandler(),
                                                            GameCollisionType.PLAYER_WEAPON: CollisionNoHandler(),
                                                            GameCollisionType.MONSTER_WEAPON: CollisionNoHandler()},
                                                           GameCollisionType.TILE,
                                                           [GameCollisionType.MONSTER,
                                                            GameCollisionType.PLAYER,
                                                            GameCollisionType.PLAYER_WEAPON,
                                                            GameCollisionType.MONSTER_WEAPON]
                                                           )

            for shape in self.tile_data.collision_shapes:
                if shape[0] == "rect":
                    self.collision_shape.add_rotatable_rect(shape[2].copy(), 0)
                if shape[0] == "circle":
                    self.collision_shape.add_circle(shape[1][0], shape[1][1], shape[3])

            self.collision_shape.set_owner(self)
            self.collision_grid.add_new_shape_to_grid(self.collision_shape)

            self.drawable_collision_shape = DrawableCompositeShape(self.collision_shape)

    def react_to_collision(self):
        pass

    def update_collision_shapes_position(self):
        if self.collidable:
            self.collision_shape.set_position(self.world_position)
            # self.collision_shape.set_rotation(self.angle * math.pi / 180.0)

    def draw_collision_shapes(self, screen, camera_position, camera_half_dimensions):
        if self.drawable_collision_shape is not None:
            self.drawable_collision_shape.update_collided_colours()
            self.drawable_collision_shape.draw(screen, camera_position, camera_half_dimensions)

    def update_offset_position(self, offset, screen_data):
        should_update = False
        should_add_to_visible_tiles = False
        self.position[0] = self.world_position[0] - offset[0]
        self.position[1] = self.world_position[1] - offset[1]
        self.rect.center = self.position
        self.update_collision_shapes_position()
        if -32 <= self.position[0] <= screen_data.screen_size[0] + 32:
                if -32 <= self.position[1] <= screen_data.screen_size[1] + 32:
                    if not self.is_visible:
                        should_update = True
                    self.is_visible = True
                    should_add_to_visible_tiles = True
                else:
                    self.is_visible = False
        else:
            self.is_visible = False
        return should_update, should_add_to_visible_tiles

    def rotate_tile_right(self):
        self.angle -= 90
        if self.angle < 0:
            self.angle = 270
        self.image = pygame.transform.rotate(self.image, -90)

    def rotate_tile_left(self):
        self.angle += 90
        if self.angle > 270:
            self.angle = 0
        self.image = pygame.transform.rotate(self.image, 90)
