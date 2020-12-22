import utilities


class Settlement(utilities.Entity):
    def __init__(self, name):
        self.name = name
        self.wood = 0
        self.stone = 0
        self.ore = 0
        self.metal = 0
        self.gp = 0
        self.msg = ""

    AMENDABLE = ("wood", "stone", "ore", "metal", "gp")
    directory = []
