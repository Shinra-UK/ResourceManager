import maps
import utilities

class User:
    def __init__(self, uid):
        self.uid = uid
        self.name = uid
        self.character_slots = 1
        self.characters = []
        self.selected_character = None
        self.viewing_fragment = maps.find_fragment((0, 0, 0))
        self.mobile = False


    AMENDABLE = ("character_slots",)
    #AMENDABLE = ("character_slots", "characters", "used_character_slots")
    EDITABLE = ("selected_character",)
    directory = []

    @property
    def used_character_slots(self):
        return len(self.characters)


def create_user(uid):
    existing = utilities.find(User.directory, "uid", uid)
    if existing is None:
        new = User(uid)
        User.directory.append(new)
        new.msg = f'{new.uid} Has been created'
        print(new.msg)
        return new
    else:
        existing.msg = f'{existing.uid} already exists'
        print(existing.msg)
        return existing
