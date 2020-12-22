# returns the first object found
def find(_list, attribute, value):
    for x in _list:
        if getattr(x, attribute) == value:
            return x
    else:
        return None
