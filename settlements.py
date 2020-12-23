import utilities
import tasks


class Settlement(utilities.Entity):
    def __init__(self, name):
        self.name = name
        self.leader = ""
        self.importing = ""
        self.exporting = ""
        self.inventory = ""
        self.food = 0
        self.wood = 0
        self.stone = 0
        self.ore = 0
        self.metal = 0
        self.gp = 0
        self.tasks = []
        self.msg = ""

    AMENDABLE = ("food", "wood", "stone", "ore", "metal", "gp")
    EDITABLE = ("leader", "importing", "exporting", "inventory")
    directory = []

    def create_task(self, name, duration, description):
        name = name.title()
        existing = utilities.find(self.tasks, "name", name)
        if existing is None:
            new = tasks.Task(name, duration, description)
            self.tasks.append(new)
            new.msg = f'{new.name} Has been created'
            print(new.msg)
            return new
        else:
            existing.msg = f'{existing.name} already exists'
            return existing
