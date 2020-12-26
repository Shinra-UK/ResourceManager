import characters
import settlements
import maps
import users
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
    nw = maps.create_fragment("",(-1,1,0), "Here there be dragons.")
    n = maps.create_fragment("",(0,1,0), "Here there be bear.  I hope we can tame him.")
    ne = maps.create_fragment("",(1,1,0), "Here there be swamp. Squelch")
    w = maps.create_fragment("",(-1,0,0), "Here there be a mirror.  I wonder who will come through next")
    c = maps.create_fragment("Haven",(0,0,0), "Here there be Haven")
    e = maps.create_fragment("Nothic Library",(1,0,0), "Here there be Nothic Library.  We stole lots of books and killed a nothic thing twice.")
    sw = maps.create_fragment("", (-1, -1, 0), "Here there be Robots.  They release thick smog that clogs up your airways.")
    s = maps.create_fragment("", (0, -1, 0), "Here there be Slimes. They eat boats!")
    se = maps.create_fragment("", (1, -1, 0), "Here there be Cows.  Moooooooooooooooooooooooooo")
    error = maps.create_fragment("Hillingdon",(-1,-1,0), "Here there be hills. Let's go over them and explore far away!")
    print(maps.Fragment.directory)
    # print(f"c.nw{c.nw}")
    # print(f"c.w{c.w}")
    c.update_neighbours()
    # print(f"c.nw{c.nw}")
    # print(f"c.w{c.w}")
    # for i in maps.Fragment.directory:
    #     print(f'{i.name} {i.description} {i.coordinates}')
    # for y in maps.neighbour_list:
    #     print(y)
    #     neighbour = getattr(c, y)
    #     print(neighbour)
    print("End of Map Tests\n")

def user_tests():
    print("End of User Tests\n")
    user1 = users.create_user(1)
    user2 = users.create_user(2)
    user3 = users.create_user(1)
    print(user1)
    print(user2)
    print(user3)
    print(users.User.directory)
    print(user1.used_character_slots)
    user2.characters.append("Bob")
    print(user2.used_character_slots)
    print("End of User Tests\n")


