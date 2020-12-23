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
    print(task1.msg)
    print(task2.msg)
    print(task3.msg)
    print(town1.tasks)
    for i in town2.tasks:
        print(i.name)
        print(i.duration)
        print(i.description)
    # print(t)
    #
    # search1 = utilities.find(town1.directory, "name", "test town one".title())
    # print(search1)
    #
    #
    # print(task1)
    # town3 = settlements.Settlement("Test")
    # print(dir(town3))
    # print(dir(task1))
    # print(task1.name)
    # print(task1.duration)
    # print(task1.description)
    # #print(task2)
    # #search2 = utilities.find(town1.tasks[0],"name","Work")
    # #print(search2)
    print("End of Task Tests\n")