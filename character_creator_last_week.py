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
def save(character_file_name, name, attributes):
    with open(character_file_name, "w", newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(["name", name])
        for attr in attributes:
            writer.writerow([attr[0], str(attr[1])])
    

character_data = load("characters/editable_character.txt")
character_name = character_data[0]
character_attributes = character_data[1]

# print the current character data
while True:
    print("Character Name: " + character_name + "\n")
    attribute_id = 1
    for attribute in character_attributes:
        print(str(attribute_id) + ". " + attribute[0] + ": " + str(attribute[1]))
        attribute_id += 1

    number_entered = int(input("Pick number of attribute to edit: "))
    attribute_picked = character_attributes[number_entered - 1]
    new_value = int(input("Set new value for " + attribute_picked[0] + ": "))
    attribute_picked[1] = new_value

    save("characters/editable_character.txt", character_name, character_attributes)
