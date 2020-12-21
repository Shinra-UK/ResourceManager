
class Character:
    def __init__(self,name):
        self.name = name
        self.gp = 0
        self.mc = 0

def createCharacter():
    testChar = Character("Test")
    print(testChar.name)