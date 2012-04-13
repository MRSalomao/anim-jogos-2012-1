from main import Creature

class Enemy(Creature):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
