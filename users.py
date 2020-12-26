import utilities

class User:
    def __init__(self, uid):
        self.uid = uid
        self.character_slots = 1
        self.characters = []
        self.selected_character = None

    directory = []


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
