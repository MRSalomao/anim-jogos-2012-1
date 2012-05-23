

class Creature(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        self.healthPoints = 0 # needs to be overridden
        