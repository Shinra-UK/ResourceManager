class Character:
    def __init__(self, name):
        self.name = title(name)
        self.gp = 0
        self.mc = 0
        self.xp = -150

    def amend(self, attribute, mod):
        if not attribute in Character.AMENDABLE:
            # raise ValueError(f'{attribute} is not amendable')
            message = f'{attribute} is not amendable'
        else:
            old_value = getattr(self, attribute)
            new_value = old_value + mod
            message = f'{self.name} had {old_value} {attribute}.\nAmending by {mod}\nNew value would be {new_value}\n'
            if (new_value >= 0):
                setattr(self, attribute, new_value)
                message += f'{new_value} set'
            elif (new_value <= 0):
                message += f"They don't have {mod}{attribute} to lose."
        print(message)
        return message

    AMENDABLE = ("gp", "mc", "xp")
    character_list = []


def create_character(name):
    new_character = Character(name)
    print(new_character.name + " Has been created")
    Character.character_list.append(new_character)
    return new_character
