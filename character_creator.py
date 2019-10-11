import os

"""
------------------------------------------------
READ ME: 
--------
If you run this file first
you will get an error. This is because you need
to create a 'Character' class in the 'character'
python file first.
------------------------------------------------
"""
from character import Character
from utility_code.utility import has_valid_input_range, make_valid_filename


is_running = True
while is_running:
    # first we try to load all the characters in the characters directory
    characters = []
    for character_file in os.listdir("characters/"):
        full_file_name = "characters/" + character_file
        character_to_load = Character(full_file_name)
        character_to_load.load()
        characters.append(character_to_load)

    print("\nWelcome to RPG Character Creator version 1.0!")

    if len(characters) > 0:
        print("Please;\n - Enter a character number to edit,\n"
              " - Enter 'new' to create a new one\n - Or enter 'q' to quit:")

        print("\nCharacters")
        print("-------------")
        number = 1
        for character in characters:
            print(str(number) + ". " + character.name)
            number += 1
    else:
        print("There are no existing characters;\n - enter 'new' to create one\n - Or enter 'q' to quit")

    menu_input = input(">")

    character_to_edit = None
    if menu_input == "new":
        character_name = input("Please enter a character name: ")
        full_file_name = "characters/" + make_valid_filename(character_name) + ".txt"
        character_to_edit = Character(full_file_name)
        character_to_edit.name = character_name
    elif menu_input == "q":
        is_running = False
    elif has_valid_input_range(menu_input, [1, len(characters)]):
        character_to_edit = characters[int(menu_input) - 1]

    if character_to_edit is not None:
        print("\nEditing character named: " + character_to_edit.name)
        is_editing = True
        while is_editing:
            print("\nCurrent Stats")
            print("-------------")
            print("1. Strength: " + str(character_to_edit.strength) + "/18")
            print("2. Dexterity: " + str(character_to_edit.dexterity) + "/18")
            print("3. Intelligence: " + str(character_to_edit.intelligence) + "/18\n")

            menu_input = input("Enter a number to edit stat, or type 's' to save and stop editing : ")

            if menu_input == "s":
                character_to_edit.save()
                print("Saved character")
                is_editing = False
            elif has_valid_input_range(menu_input, [1, 3]):
                # -----------------------------------------------------
                # Bonus Challenge!
                # -----------------
                # The code called by each of these three if statements
                # below is almost identical. That is usually a sign
                # that what the code does could be made into a function
                # with the passed in parameter used to account for the
                # minor differences.
                #
                # See if you can replace some of the code below with a function
                # that gets called three times instead. Then use your new function
                # and a few edits to this program and your character class,
                # to add the other three traditional D&D stats; constitution,
                # wisdom and charisma.
                # -----------------------------------------------------
                if int(menu_input) == 1:
                    print("Editing Strength")
                    new_value = input("Enter new value: ")
                    if has_valid_input_range(new_value, [0, 18]):
                        character_to_edit.strength = int(new_value)
                    else:
                        print("Invalid input")
                if int(menu_input) == 2:
                    print("Editing Dexterity")
                    new_value = input("Enter new value: ")
                    if has_valid_input_range(new_value, [0, 18]):
                        character_to_edit.dexterity = int(new_value)
                    else:
                        print("Invalid input")
                if int(menu_input) == 3:
                    print("Editing Intelligence")
                    new_value = input("Enter new value: ")
                    if has_valid_input_range(new_value, [0, 18]):
                        character_to_edit.intelligence = int(new_value)
                    else:
                        print("Invalid input")
            else:
                print("Invalid input")

    elif is_running:
        print("invalid input, please try again")
    else:
        print("Game Over")
