from operator import attrgetter

from game.base_weapon import BaseWeapon
from game.damage import Damage, DamageType


# ----------------------------------------------------------------------------------
# Challenge 2 - Using loops and class variables
# ----------------------------------------------
#
# Improve the magic weapon so that it:
#
# A: flings away ALL monsters in range rather than
#    just the closest one.
# B: Makes use of the player's magic stat and current level to effect
#    fling distance, mana_cost and damage.
#
# - Use a for loop!
# - Check out the other weapons for ideas on how to use the player level and stat to
#   upgrade your magic.
# ----------------------------------------------------------------------------------
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
        pass

    def fire(self, monsters: list):
        self.deduct_mana_cost()
        if len(monsters) > 0:

            # find the closest monster with a sort function
            sorted_monsters = sorted(monsters, key=attrgetter('player_distance'))
            closest_monster = sorted_monsters[0]

            # check if the closest monster is in range of our spell
            if closest_monster.player_distance <= self.magic_range:
                # if in range blast the monster with damage...
                closest_monster.take_damage(Damage(self.magic_damage, DamageType.MAGIC))

                # ...then fling it away from the player.
                x_dist = float(closest_monster.position[0]) - float(self.player_position[0])
                y_dist = float(closest_monster.position[1]) - float(self.player_position[1])
                away_from_player_dir = [(x_dist / closest_monster.player_distance) * self.distance_to_fling_per_second,
                                        (y_dist / closest_monster.player_distance) * self.distance_to_fling_per_second]
                closest_monster.fling_monster(away_from_player_dir, self.time_to_fling)
