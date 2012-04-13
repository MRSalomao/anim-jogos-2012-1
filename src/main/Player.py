from main import Creature

class Player(Creature):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
