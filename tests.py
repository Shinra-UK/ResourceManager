import characters
import settlements
import utilities

entities = {'Character': characters.Character,
            'Settlement': settlements.Settlement}


def character_tests():
    entity_type = entities['Character']
    print("Starting Character Tests")
    test_mc_gee = utilities.create(entity_type, "Test Mcgee")
    test_mo_jo = utilities.create(entity_type, "Test Mo Jo")
    test_mo_jo.amend("gp", 20)
    test_mo_jo.amend("gP", 200)
    test_mo_jo.amend("gp", -10)
    test_mo_jo.amend("gp", -640)
    test_mo_jo.amend("name", 540)
    test_mo_jo.amend("NaN", 540)
    print(test_mo_jo.directory)
    print(test_mc_gee.directory)
    print(utilities.find(characters.Character.directory, "name", "Test Mcgee"))
    print(utilities.find(characters.Character.directory, "gp", 2))
    print(utilities.find(characters.Character.directory, "gp", 0))
    bob = utilities.create(characters.Character, "bob")
    bob1 = utilities.create(characters.Character, "bob")
    bob2 = utilities.create(characters.Character, "bob")
    print(bob)
    print(bob.msg)
    print(bob1)
    print(bob2)
    print(utilities.Entity.directory)
    print("End of Character Tests\n")


def settlement_tests():
    print("Starting Settlement Tests")
    entity_type = entities['Settlement']
    town1 = utilities.create(entity_type, "test town one")
    town2 = utilities.create(entity_type, "test town two")
    print(town1)
    print(town2)
    town1.amend("gp", 20)
    town1.amend("gp", 20)
    print(utilities.Entity.directory)
    print("End of Settlement Tests")
