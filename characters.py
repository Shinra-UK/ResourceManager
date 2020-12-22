import numbers
import utilities


class Character:
    def __init__(self, name):
        self.name = name
        self.gp = 0
        self.mc = 0
        self.xp = -150
        self.msg = ""

    def amend(self, attribute, mod):
        message = ""
        if attribute not in Character.AMENDABLE:
            message += f'{attribute} is not amendable\n'
        else:
            try:
                mod = int(mod)
            except ValueError as verr:
                print(verr)
                message += f'{mod} must be a number\n'
            if isinstance(mod, numbers.Real):
                old_value = getattr(self, attribute)
                new_value = old_value + mod
                message += f'{self.name} had {old_value} {attribute}.\n' \
                           f'Amending by {mod}\nNew value would be {new_value}\n'
                if new_value >= 0:
                    setattr(self, attribute, new_value)
                    message += f'{new_value} set'
                elif new_value <= 0:
                    message += f"They don't have {mod}{attribute} to lose."
        print(message)
        return message

    AMENDABLE = ("gp", "mc", "xp")
    character_list = []


def create_character(name):
    existing_character = utilities.find(Character.character_list, "name", name.title())
    if existing_character is None:
        name = name.title()
        new_character = Character(name)
        print(new_character.name + " Has been created")
        Character.character_list.append(new_character)
        new_character.msg = f'{new_character.name} has arrived!'
        return new_character
    else:
        existing_character.msg = f'{existing_character.name} is already here.'
        return existing_character
