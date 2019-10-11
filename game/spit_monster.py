from game.base_monster import BaseMonster
# from game.spit import Spit

monsterID = "spit"
imagePath = "images/monsters/spit_monster.png"
pointCost = 1


class SpitMonster(BaseMonster):
    def __init__(self, start_pos, image_dictionary, monster_type_dict, all_monster_sprites,
                 play_area, collision_grid):
        image = image_dictionary[monsterID]
        monster_type = monster_type_dict[monsterID]
        super().__init__(start_pos, monsterID, image, monster_type.points,
                         all_monster_sprites, play_area, collision_grid)

        self.cash_value = 30
        self.idle_move_speed = self.set_average_speed(35)
        self.attack_move_speed = self.set_average_speed(75)
        self.move_speed = self.idle_move_speed
        self.health = 75
        self.attack_damage = 20
        self.attack_time_delay = 3.0

    def attack(self, time_delta, player):
        pass
        # Spit(self.position, self.current_aim_vector, 10, None)
