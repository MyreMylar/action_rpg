import os
import csv


class Character:
    def __init__(self, file_name):
        self.fileName = file_name
        self.name = ""
        self.portrait_index = [0, 0]
        self.strength = 0
        self.dexterity = 0
        self.magic = 0
        self.score = 0

    def load(self):
        with open(self.fileName, "r") as characterFile:
            reader = csv.reader(characterFile)
            for line in reader:
                self.name = line[0]
                self.portrait_index = [int(line[1]), int(line[2])]
                self.strength = int(line[3])
                self.dexterity = int(line[4])
                self.magic = int(line[5])
                self.score = int(line[6])

    def save(self):
        with open(self.fileName, "w", newline='') as character_file:
            writer = csv.writer(character_file)
            writer.writerow([self.name, str(self.portrait_index[0]), str(self.portrait_index[1]),
                             str(self.strength), str(self.dexterity), str(self.magic), str(self.score)])
            

def reload_characters(characters):
    characters[:] = []
    for character_file in os.listdir("characters/"):
        full_file_name = "characters/" + character_file
        character_to_load = Character(full_file_name)
        character_to_load.load()
        characters.append(character_to_load)

    return characters
