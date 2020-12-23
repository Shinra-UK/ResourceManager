import utilities


class Character(utilities.Entity):
    def __init__(self, name):
        self.name = name
        self.player = ""
        self.location = ""
        self.gp = 0
        self.mc = 0
        self.xp = -150
        self.msg = ""

    AMENDABLE = ("gp", "mc", "xp")
    EDITABLE = ("player", "location")
    directory = []
