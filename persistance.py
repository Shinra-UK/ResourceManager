import pickle

import maps
import users
import settlements


def save(file_name, directory):
    with open(file_name, "wb") as f:
        pickle.dump(directory, f)


def load(file_name):
    with open(file_name, "rb") as f:
        directory = pickle.load(f)
    print(directory)
    return directory
