import utilities

class Fragment():
    def __init__(self, name, x, y, z, description):
        self.coordinates = (x, y, z)
        self.name = name
        self.description = description

    directory = []

def create_fragment(name, x, y, z, description):
    name = name.title()
    coordinates = (x, y, z)
    existing = utilities.find(Fragment.directory, "coordinates", coordinates)
    if existing:
        existing.msg =f'{existing.name} is already here.'
        return existing
    else:
        new = Fragment(name, x, y, z , description)
        print(new.name + " Has been created")
        Fragment.directory.append(new)
        new.msg = f'{new.name} has been drawn!'
        return new