#returns the first object found
def find(list, attribute, value):
    for x in list:
        if getattr(x,attribute) == value:
            return x
    else:
        return None
