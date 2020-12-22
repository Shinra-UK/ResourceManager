import numbers
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

    # def amend(self, attribute, mod):
    #     message = ""
    #     if attribute not in Settlement.AMENDABLE:
    #         message += f'{attribute} is not amendable\n'
    #     else:
    #         try:
    #             mod = int(mod)
    #         except ValueError as verr:
    #             print(verr)
    #             message += f'{mod} must be a number\n'
    #         if isinstance(mod, numbers.Real):
    #             old_value = getattr(self, attribute)
    #             new_value = old_value + mod
    #             message += f'{self.name} had {old_value} {attribute}.\n' \
    #                        f'Amending by {mod}\nNew value would be {new_value}\n'
    #             if new_value >= 0:
    #                 setattr(self, attribute, new_value)
    #                 message += f'{new_value} set'
    #             elif new_value <= 0:
    #                 message += f"They don't have {mod}{attribute} to lose."
    #     print(message)
    #     return message

    AMENDABLE = ("wood", "stone", "ore","metal","gp")
    settlement_list = []


# def create_settlement(name):
#     existing_settlement = utilities.find(Settlement.settlement_list, "name", name.title())
#     if existing_settlement is None:
#         name = name.title()
#         new_settlement = Settlement(name)
#         print(new_settlement.name + " Has been created")
#         Settlement.settlement_list.append(new_settlement)
#         new_settlement.msg = f'{new_settlement.name} has been founded!'
#         return new_settlement
#     else:
#         existing_settlement.msg = f'{existing_settlement.name} already exists.'
#         return existing_settlement
