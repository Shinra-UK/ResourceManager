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
    directory = []
    pass