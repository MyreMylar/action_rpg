from util.character import Character, reload_characters
from util.utility import has_valid_input_range, make_valid_filename
import random


def rerolling_stat_display(stat_name, character_to_edit):
    print("Re-rolling 3d6 for " + stat_name + "...")
    new_roll = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
    print("New roll is " + str(new_roll))
    if has_valid_input_range(new_roll, [0, 18]):
        if stat_name == "Strength":
            character_to_edit.strength = new_roll
        elif stat_name == "Dexterity":
            character_to_edit.dexterity = new_roll
        elif stat_name == "Magic":
            character_to_edit.magic = new_roll
    else:
        print("Invalid input")

    input("\nPress any key to return to edit menu")


# ----------------------------------------------------
# Challenge 3
#
# Sort the characters by their names alphabetically
# before displaying the list.
#
# - BONUS CHALLENGE: Can you think of a way to sort characters
#   by their last name using the current character file format?
# 
#   (As a tip you can split strings into separate words using the .split()
#   method.)
# ----------------------------------------------------
def edit_character_display(characters):
    is_editing_characters = True
    while is_editing_characters:
        characters = reload_characters(characters)
        if len(characters) > 0:
            # Add your sorting code here
            
            print("Please;\n"
                  " - Enter a character number to edit,\n"
                  " - Enter 'new' to create a new one\n"
                  " - Or enter 'b' to go back:")

            print("\nCharacters")
            print("-------------")
            number = 1
            for character in characters:
                print(str(number) + ". " + character.name)
                number += 1

        else:
            print("There are no existing characters;\n"
                  " - enter 'new' to create one\n"
                  " - Or enter 'b' to go back")

        menu_input = input(">")

        character_to_edit = None
        if menu_input == "new":
            character_name = input("Please enter a character name: ")
            full_file_name = "characters/" + make_valid_filename(character_name) + ".txt"
            character_to_edit = Character(full_file_name)
            character_to_edit.name = character_name
        elif menu_input == "b":
            is_editing_characters = False
        elif has_valid_input_range(menu_input, [1, len(characters)]):
            character_to_edit = characters[int(menu_input)-1]

        if character_to_edit is not None:
            print("\nEditing character named: " + character_to_edit.name)
            is_editing = True
            while is_editing:
                menu_values = ["Strength", "Dexterity", "Magic"]
                print("\nCurrent Stats")
                print("-------------")
                print("1. Strength: " + str(character_to_edit.strength) + "/18")
                print("2. Dexterity: " + str(character_to_edit.dexterity) + "/18")
                print("3. Magic: " + str(character_to_edit.magic) + "/18\n")

                menu_input = input("Enter a number to re-roll stat, or type 's' to save and stop editing : ")

                if menu_input == "s":
                    character_to_edit.save()
                    print("Saved character")
                    is_editing = False
                elif has_valid_input_range(menu_input, [1, 3]):
                    stat_name = menu_values[int(menu_input)-1]
                    rerolling_stat_display(stat_name, character_to_edit)
                else:
                    print("Invalid input")
        if not is_editing_characters:
            print("Returning to main menu")
        else:
            print("Invalid input")
