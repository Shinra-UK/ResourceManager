import characters
import settlements
import maps
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
    print(characters.Character.directory)
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
    town1.edit("location", town1.name)
    bob = utilities.find(characters.Character.directory, "name", "Bob")
    bob.edit("location", town1.name)
    print(utilities.Entity.directory)
    print(settlements.Settlement.directory)
    print("End of Settlement Tests\n")


def task_tests():
    print("Starting Task Tests")
    entity_type = entities['Settlement']
    town1 = utilities.create(entity_type, "test town one")
    town2 = utilities.create(entity_type, "test town two")
    task1 = town1.create_task("Work", 10, "Work for food")
    task2 = town1.create_task("Work", 15, "Work for more food")
    task3 = town1.create_task("Build", 10, "Build a structure")
    town2.create_task("", "", "")
    print(task1.msg)
    print(task2.msg)
    print(task3.msg)
    print(town1.tasks)
    for i in town1.tasks:
        print(utilities.build_table(i, "name", "duration", "description", "error"))
    for i in town2.tasks:
        print(utilities.build_table(i, "name", "duration", "description"))
    print("End of Task Tests\n")


def map_tests():
    print("Starting Map Tests")
    nw = maps.create_fragment("",-1,1,0, "Here there be dragons")
    n = maps.create_fragment("",0,1,0, "Here there be bear")
    ne = maps.create_fragment("",1,1,0, "Here there be swamp")
    w = maps.create_fragment("",-1,0,0, "Here there be a mirror")
    c = maps.create_fragment("Haven",0,0,0, "Here there be Haven")
    e = maps.create_fragment("Nothic Library",1,0,0, "Here there be Nothic Library")
    sw = maps.create_fragment("", -1, -1, 0, "Here there be Robots")
    s = maps.create_fragment("", -1, -1, 0, "Here there be Slimes")
    se = maps.create_fragment("", -1, -1, 0, "Here there be Cows")
    error = maps.create_fragment("Hillingdon",-1,-1,0, "Here there be hills")
    print(maps.Fragment.directory)
    print("End of Map Tests\n")