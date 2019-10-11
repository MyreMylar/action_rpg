import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def draw_collision_shape(self, screen):
        pass

    def update(self, tiled_level, time_delta):
        pass

    def remove_from_grid(self):
        pass
