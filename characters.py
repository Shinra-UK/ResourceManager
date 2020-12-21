import numbers

class Character:
    def __init__(self, name):
        self.name = name
        self.gp = 0
        self.mc = 0
        self.xp = -150

    def amend(self, attribute, mod):
        message = ""
        if not attribute in Character.AMENDABLE:
            message += f'{attribute} is not amendable\n'
        else:
            try:
                mod = int(mod)
            except ValueError as verr:
                print(verr)
                message += f'{mod} must be a number\n'
            if isinstance(mod,numbers.Real):
                old_value = getattr(self, attribute)
                new_value = old_value + mod
                message += f'{self.name} had {old_value} {attribute}.\nAmending by {mod}\nNew value would be {new_value}\n'
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
    name = name.title()
    new_character = Character(name)
    print(new_character.name + " Has been created")
    Character.character_list.append(new_character)
    return new_character
