from pandac.PandaModules import *

class Map(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # fog experiment
        myFog = Fog("Mist")
        myFog.setColor(0.6, 0.6, 0.6)
        myFog.setExpDensity(0.0007)
        render.setFog(myFog)

        # loading h_208 room
        self.h208Room = loader.loadModel("../../models/model_h208/h_208")
        self.h208Room.reparentTo(self.mainRef.render)
        self.h208Room.setPos(0, 0, -27)
        self.h208Room.setScale(34, 34, 34)
