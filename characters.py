class Character:
    def __init__(self,name):
        self.name = name
        self.gp = 0
        self.mc = 0
        self.xp = -150

    def ammend(self, attribute, mod):
        if (not attribute in Character.AMMENDABLE):
            #raise ValueError(f'{attribute} is not ammendable')
            message = f'{attribute} is not ammendable'
        else:
            old_value = getattr(self,attribute)
            new_value = old_value + mod
            message = f'{self.name} had {old_value} {attribute}.\nAmmending by {mod}\nNew value would be {new_value}\n'
            if(new_value >= 0):
                setattr(self,attribute,new_value)
                message += f'{new_value} set'
            elif(new_value <= 0):
                message+=f"They don't have {mod}{attribute} to lose."
        print(message)
        return message

    AMMENDABLE = ("gp","mc","xp")
    character_list = []



def create_character(name):
    new_character = Character(name)
    print(new_character.name + " Has been created")
    Character.character_list.append(new_character)
    return new_character

#retruns the first object found
def find(list, attribute, value):
    for x in list:
        if getattr(x,attribute) == value:
            print("i found it!")
            print(x)
            break
    else:
        x = None