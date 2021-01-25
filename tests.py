import characters
import settlements
import maps
import users
import utilities
import persistance
import re
import pickle
import time

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
    print("Start of User Tests")
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

def persistance_tests():
    print("Start of Persistance Tests")

    # file_name = "test_file2.pkl"
    # print(file_name)
    # # persistance.save(file_name, maps.Fragment.directory)
    #
    # directory = persistance.load(file_name)
    # print(directory)
    # maps.Fragment.directory = directory

    # test_save = persistance.save_all()

    test_load = persistance.load_all()
    print(users.User.directory)
    print(settlements.Settlement.directory)
    print(utilities.Entity.directory)
    print(maps.Fragment.directory)
    print(characters.Character.directory)

    # with open(file_name, "wb") as f:
    #     pickle.dump(users.User.directory, f)
    #
    # time.sleep(5)
    #
    # with open(file_name, "rb") as f:
    #     directory = pickle.load(f)
    # print(directory)




    # test_file = open("test_file.pkl", "wb")
    # user_save = persistance.save(test_file, users.User.directory)
    # print(user_save)
    # # test_file.close()
    #
    # test_load = "test_file.pkl"
    # test_dir = []
    # print("test_dir")
    # print(test_dir)
    # print("test_load")
    # print(test_load)
    # print("user_load")
    # user_load = persistance.load(test_load)
    # print(user_load)
    # # print("pickle.load")
    # loaded = pickle.load(test_load)
    # loaded2 = pickle.load(test_load)
    # print(loaded)
    # print(loaded2)
    print("End of Persistance Tests\n")

def re_tests():
    print("Start of re Tests")
    string = "fxdbxd fcbxd  (1ghftgh)(2ftgch)"
    print(string)

    #user
    usereg = re.findall(r'^[a-zA-Z].+?(?=\()', string)
    print(usereg)
    if len(usereg) > 0:
        print(usereg[0].strip())

    #characters
    reg = re.findall(r'\(.*?\)', string)
    print(len(reg))
    print(reg)
    for i in reg:
        currentstring = i
        substring = i[1:-1]
        print(currentstring)
        print(substring)
    print("End of re Tests\n")

def menu_tests():
    print("Start of menu Tests")
    test_user = users.User.directory[0]
    test_user.character_slots = 4
    print(test_user)
    print("End of menu Tests\n")
