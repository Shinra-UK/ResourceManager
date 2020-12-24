import utilities


class Fragment():
    def __init__(self, name, coordinates, description):
        self.coordinates = coordinates
        self.name = name
        self.description = description

    directory = []

    def locate_neighbour(self, direction=(0, 0, 0), distance=1):
        my_x = self.coordinates[0]
        my_y = self.coordinates[1]
        my_z = self.coordinates[2]
        target_x = my_x + (direction[0] * distance)
        target_y = my_y + (direction[1] * distance)
        target_z = my_z + (direction[2] * distance)
        target_coordinates = (target_x, target_y, target_z)
        return target_coordinates

    def find_fragment(self, target_coordinates):
        existing = utilities.find(Fragment.directory, "coordinates", target_coordinates)
        if existing:
            return existing
        else:
            return unmapped_fragment
            #return None

    def set_neighbour(self, direction_coordinates):
        target_coordinates = Fragment.locate_neighbour(self, direction_coordinates)
        neighbour = Fragment.find_fragment(self, target_coordinates)
        return neighbour

    def update_neighbours(self):
        self.nw = self.set_neighbour((-1, 1, 0))
        self.n = self.set_neighbour((0, 1, 0))
        self.ne = self.set_neighbour((1, 1, 0))
        self.w = self.set_neighbour((-1, 0, 0))
        self.e = self.set_neighbour((0, 1, 0))
        self.sw = self.set_neighbour((-1, -1, 0))
        self.s = self.set_neighbour((0, -1, 0))
        self.se = self.set_neighbour((1, -1, 0))
        self.up = self.set_neighbour((0, 0, 1))
        self.dn = self.set_neighbour((0, 0, -1))


def create_fragment(name, coordinates, description):
    name = name.title()
    existing = utilities.find(Fragment.directory, "coordinates", coordinates)
    if existing:
        existing.msg = f'{existing.name} is already here.'
        return existing
    else:
        new = Fragment(name, coordinates, description)
        # new.update_neighbours()
        print(new.name + " Has been created")
        Fragment.directory.append(new)
        new.msg = f'{new.name} has been drawn!'
        return new


def print_cords(x, y, z):
    print(f"Coordinates {x, y, z}")


unmapped_fragment = Fragment("Unmapped Area",
                             (999, 999, 999),
                             "Has anyone explored here yet?")
