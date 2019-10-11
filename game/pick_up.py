import pygame
import random
from collision.collision_shapes import CollisionCircle
from collision.collision_handling import CollisionNoHandler
from game.game_collision_types import GameCollisionType


class PickUpSpawner:
    def __init__(self, all_pick_up_sprites, collision_grid):
        self.collision_grid = collision_grid
        self.all_pick_up_sprites = all_pick_up_sprites
        self.mana_image = pygame.image.load("images/pick_ups/mana.png")
        self.health_image = pygame.image.load("images/pick_ups/health.png")

    def try_spawn(self, spawn_position):
        random_roll = random.randint(0, 100)
        if random_roll < 10:
            PickUp(spawn_position, self.health_image, "health",
                   self.collision_grid, self.all_pick_up_sprites)
        elif 10 < random_roll <= 20:
            PickUp(spawn_position, self.mana_image, "mana",
                   self.collision_grid, self.all_pick_up_sprites)


class PickUp(pygame.sprite.Sprite):
    def __init__(self, start_pos, image, type_name, collision_grid, *groups):
        super().__init__(*groups)
        self.collision_grid = collision_grid
        self.world_position = [start_pos[0], start_pos[1]]
        self.type_name = type_name
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        self.position = [float(self.rect.center[0]), float(self.rect.center[1])]

        self.should_die = False

        self.collide_radius = 8
        self.collision_circle = CollisionCircle(self.position[0], self.position[1], self.collide_radius,
                                                {GameCollisionType.PLAYER: CollisionNoHandler()},
                                                GameCollisionType.PICKUP,
                                                [GameCollisionType.PLAYER])
        self.collision_circle.set_owner(self)
        self.collision_grid.add_new_shape_to_grid(self.collision_circle)

    def remove_from_grid(self):
        self.collision_grid.remove_shape_from_grid(self.collision_circle)

    def react_to_collision(self):
        for shape in self.collision_circle.collided_shapes_this_frame:
            if shape.game_type == GameCollisionType.PLAYER:
                self.should_die = True
                player = shape.owner
                if self.type_name == "health":
                    player.add_health(0.25 * player.max_health)
                elif self.type_name == "mana":
                    player.add_mana(25)

    def update(self, tiled_level):
        self.position[0] = self.world_position[0] - tiled_level.position_offset[0]
        self.position[1] = self.world_position[1] - tiled_level.position_offset[1]
        self.rect.center = self.position

        self.collision_circle.set_position(self.world_position)
        if self.should_die:
            self.collision_grid.remove_shape_from_grid(self.collision_circle)
            self.kill()
