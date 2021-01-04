import pickle

import maps
import users
import settlements
import characters
import utilities

directories = {'fragments.pkl': maps.Fragment,
               'users.pkl': users.User,
               'settlements.pkl': settlements.Settlement,
               'characters.pkl': characters.Character,
               'entities.pkl': utilities.Entity
               }

def save_all():
    for file_name in directories:
        _class = directories[file_name]
        directory = _class.directory
        print(f'Saving to {file_name}:\n{directory}')
        save(file_name, directory)

def load_all():
    for file_name in directories:
        _class = directories[file_name]
        _class.directory = load(file_name)
        print(f'Loading from {file_name}:\n{_class.directory}')


def save(file_name, directory):
    with open(file_name, "wb") as f:
        pickle.dump(directory, f)


def load(file_name):
    with open(file_name, "rb") as f:
        directory = pickle.load(f)
    return directory
