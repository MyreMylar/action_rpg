from game.base_monster import BaseMonster


class GoblinMonster(BaseMonster):

    def __init__(self, type_id, start_pos, sprite_map, all_monster_sprites, play_area, tiled_level,
                 collision_grid):
        super().__init__(type_id, start_pos, sprite_map, all_monster_sprites, play_area, tiled_level,
                         collision_grid)
        self.xp = 25
        self.score = 100
        self.idle_move_speed = self.set_average_speed(35)
        self.attack_move_speed = self.set_average_speed(75)
        self.move_speed = self.idle_move_speed
        self.health = 75
        self.attack_damage = 20
        self.attack_time_delay = 3.0
