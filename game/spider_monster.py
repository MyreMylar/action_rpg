from game.base_monster import BaseMonster


class SpiderMonster(BaseMonster):

    def __init__(self, type_id, start_pos, sprite_map, all_monster_sprites, play_area, tiled_level,
                 collision_grid):
        super().__init__(type_id, start_pos, sprite_map, all_monster_sprites, play_area, tiled_level,
                         collision_grid)
        self.xp = 40
        self.score = 150
        self.idle_move_speed = self.set_average_speed(75)
        self.attack_move_speed = self.set_average_speed(150)
        self.move_speed = self.idle_move_speed
        self.health = 50
        self.attack_damage = 10
        self.attack_time_delay = 2.0
