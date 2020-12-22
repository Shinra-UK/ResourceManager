import utilities


class Character(utilities.Entity):
    def __init__(self, name):
        self.name = name
        self.gp = 0
        self.mc = 0
        self.xp = -150
        self.msg = ""

    AMENDABLE = ("gp", "mc", "xp")
    directory = []
