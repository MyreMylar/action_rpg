from game.base_monster import BaseMonster


class EntMonster(BaseMonster):
    def __init__(self, type_id, start_pos, sprite_map,
                 all_monster_sprites, play_area, tiled_level, collision_grid):
        super().__init__(type_id, start_pos, sprite_map, all_monster_sprites,
                         play_area, tiled_level, collision_grid)
        self.xp = 75
        self.score = 300
        self.idle_move_speed = self.set_average_speed(20)
        self.attack_move_speed = self.set_average_speed(100)
        self.move_speed = self.idle_move_speed
        self.health = 150
        self.attack_damage = 40
        self.attack_time_delay = 4.0
