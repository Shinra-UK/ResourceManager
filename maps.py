import time
import utilities

class Log_Entry:
    def __init__(self, time_stamp, author, entry):
        self.time_stamp = time_stamp
        self.author = author
        self.entry = entry

class Fragment:
    def __init__(self, name, coordinates, description_log_entry):
        self.coordinates = coordinates
        self.name = name
        self.description_log = [description_log_entry]
        #self.description = description
        self.nw = False
        self.n = False
        self.ne = False
        self.w = False
        self.c = False
        self.e = False
        self.sw = False
        self.s = False
        self.se = False
        self.up = False
        self.dn = False

        # self.neighbour_list = {
        #     "nw": self.nw,
        #     "n": self.n,
        #     "ne": self.ne,
        #     "w": self.w,
        #     "c": self.c,
        #     "e": self.e,
        #     "sw": self.sw,
        #     "s": self.s,
        #     "se": self.se,
        #     "up": self.up,
        #     "dn": self.dn
        # }

    @property
    def description(self):
        return self.description_log[0].entry

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

    def set_neighbour(self, direction_coordinates):
        target_coordinates = Fragment.locate_neighbour(self, direction_coordinates)
        neighbour = find_fragment(target_coordinates)
        return neighbour

    def update_neighbours(self):
        self.nw = self.set_neighbour((-1, 1, 0))
        self.n = self.set_neighbour((0, 1, 0))
        self.ne = self.set_neighbour((1, 1, 0))
        self.w = self.set_neighbour((-1, 0, 0))
        self.c = self.set_neighbour((0, 0, 0))
        self.e = self.set_neighbour((1, 0, 0))
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
        new = Fragment(name, coordinates, Log_Entry(time.time(), "System", description))
        print(new.name + " Has been created")
        Fragment.directory.append(new)
        new.msg = f'{new.name} has been drawn!'
        return new


def print_cords(x, y, z):
    print(f"Coordinates {x, y, z}")


def find_fragment(target_coordinates):
    existing = utilities.find(Fragment.directory, "coordinates", target_coordinates)
    if existing:
        return existing
    else:
        return create_fragment("Unmapped Area", target_coordinates, "?????")
        #unmapped_fragment
        # return None


neighbour_list = ("nw", "n", "ne", "w", "c", "e", "sw", "s", "se", "up", "dn")

# unmapped_fragment = Fragment("Unmapped Area",
#                              (999, 999, 999),
#                              "Has anyone explored here yet?")
