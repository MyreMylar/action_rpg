from game.base_weapon import BaseWeapon
from game.damage import Damage, DamageType


class MagicWeapon(BaseWeapon):
    def __init__(self, player, sprite_sheet):
        player_sprite_y_offset = 384
        super().__init__(player, sprite_sheet, player_sprite_y_offset)
        self.fire_rate = 0.3
        self.fire_anim_speed = 0.25
        self.magic_damage = 1
        self.magic_range = 188
        self.mana_cost = 25
        self.distance_to_fling_per_second = 320
        self.time_to_fling = 0.5

        self.on_level_up()

    def on_level_up(self):
        self.mana_cost -= (1 * self.player.character.magic/10)
        self.magic_range += (8 * self.player.character.magic/10)
        self.magic_damage += (3 * self.player.character.magic/10)
        self.time_to_fling += (0.05 * self.player.character.magic/10)

    def fire(self, monsters: list):
        self.deduct_mana_cost()
        if len(monsters) > 0:
            for monster in monsters:
                # check if the closest monster is in range of our spell
                if monster.player_distance <= self.magic_range:
                    # if in range blast the monster with damage...
                    monster.take_damage(Damage(self.magic_damage, DamageType.MAGIC))

                    # ...then fling it away from the player.
                    x_dist = float(monster.position[0]) - float(self.player_position[0])
                    y_dist = float(monster.position[1]) - float(self.player_position[1])
                    away_from_player_dir = [(x_dist/monster.player_distance) * self.distance_to_fling_per_second,
                                            (y_dist/monster.player_distance) * self.distance_to_fling_per_second]
                    monster.fling_monster(away_from_player_dir, self.time_to_fling)
