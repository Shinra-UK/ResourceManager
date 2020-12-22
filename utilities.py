import numbers


# returns the first object found
def find(directory, attribute, value):
    for x in directory:
        if getattr(x, attribute) == value:
            return x
    else:
        return None


def create(entity, name):
    name = name.title()
    existing = find(entity.directory, "name", name)
    if existing is None:
        new = entity(name)
        print(new.name + " Has been created")
        entity.directory.append(new)
        Entity.directory.append(new)
        new.msg = f'{new.name} has arrived!'
        return new
    else:
        existing.msg = f'{existing.name} is already here.'
        return existing


class Entity:
    def __init__(self, name):
        self.name = name
        self.gp = 0

    AMENDABLE = "gp"
    directory = []

    def amend(self, attribute, mod):
        message = ""
        if attribute not in self.AMENDABLE:
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
