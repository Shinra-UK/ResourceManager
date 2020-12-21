class Character:
    def __init__(self,name):
        self.name = name
        self.gp = 0
        self.mc = 0

    character_list = []



def createCharacter(name):
    newCharacter = Character(name)
    print(newCharacter.name + " Has been created")
    Character.character_list.append(newCharacter)
    return newCharacter

