import characters
import settlements
import utilities


def character_tests():
    print("Starting Character Tests")
    test_mc_gee = characters.create_character("Test Mcgee")
    test_mo_jo = characters.create_character("Test Mo Jo")
    test_mo_jo.amend("gp", 20)
    test_mo_jo.amend("gp", 200)
    test_mo_jo.amend("gp", -640)
    test_mo_jo.amend("gp", -40)
    test_mo_jo.amend("name", 540)
    print(test_mo_jo.character_list)
    print(test_mc_gee.character_list)
    print(utilities.find(characters.Character.character_list, "gp", 0))
    print(utilities.find(characters.Character.character_list, "gp", 2))
    print("End of Character Tests")

def settlement_tests():
    print("Starting Settlement Tests")
    town1 = settlements.create_settlement("test town one")
    town2 = settlements.create_settlement("test town two")
    print(town1)
    print(town2)
    print("End of Character Tests")