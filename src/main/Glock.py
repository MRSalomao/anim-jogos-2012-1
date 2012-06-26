
from pandac.PandaModules import *

from Weapon import *

class Glock(Weapon):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        super(Glock, self).__init__(mainReference)
        
        # load our glock model
        self.weaponModel = loader.loadModel("../../models/model_glock/glock")
        # ****SCALE****
        self.weaponModel.setScale(0.1)
        # ***POS***
        self.weaponModel.setPos(0.2,1.5,0.5)
        # ****HPR****
        self.weaponModel.setHpr(280,0,0)
        # attaching to render
        self.weaponModel.wrtReparentTo(self.mainRef)
