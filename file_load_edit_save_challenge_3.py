"""
-------------------------------------------------------------------
Challenge 3
--------------

This time we are going to load some character data from a file,
make a change to it and then save it back to the same file.

We are also going to use the 'csv' library to interpret the file.
You could work directly on the file text and parse the lines
yourself, but the csv library makes it easier.

You will need to use the input() function to get user input.

To Do:

---------
Part A
---------
 - Add to the code below to ask the user to input
   the ID number of an attribute. Store this number in a variable.
 - Use the entered number to find the right attribute data to edit
   by indexing into our list. Remember that list indexes start at 0!
   Store the found attribute data in another variable.
 - Using the found data, ask the user to input a new value for the
   attribute with a prompt like this:
   'Enter a new value for Charisma: "
 - Set the attribute to the newly entered value.

--------
Part B
--------
 - Now we need to finish, and call, the save function.
 - We can use a for loop to save the whole attributes list to our file.
   To write a row to the file with the csv library use .writerow()
 - Check your changes were made in the file

----------------
Bonus challenge
----------------
 - Loop the whole editing part of the program so that users
   can make many changes without having to restart.
-------------------------------------------------------------------------
"""
import csv


# Load a character function
def load(character_file_name):
    char_name = ""
    char_attributes = []
    character = [char_name, char_attributes]
    with open(character_file_name, "r") as data_file:
        # load the data in the file into a list
        reader = csv.reader(data_file)
        for row in reader:
            if row[0] == "name":
                character[0] = row[1]
            else:
                character[1].append([row[0], int(row[1])])
                
    return character


# Incomplete save a character function
def save(character_file_name):
    with open(character_file_name, "w", newline='') as data_file:
        pass
        # writer = csv.writer(data_file)
    

character_data = load("editable_character.txt")
character_name = character_data[0]
character_attributes = character_data[1]

# print the current character data
print("Character Name: " + character_name + "\n")
attribute_id = 1
for attribute in character_attributes:
    print(str(attribute_id) + ". " + attribute[0] + ": " + str(attribute[1]))
    attribute_id += 1

# START ENTERING YOUR ATTRIBUTE EDITING CODE HERE

# save("editable_character.txt")
