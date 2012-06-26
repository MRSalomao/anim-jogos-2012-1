
from pandac.PandaModules import *
from direct.actor.Actor import Actor

from Weapon import *

class Glock(Weapon):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        super(Glock, self).__init__(mainReference)
        
        # load our glock model
        self.weaponModel = Actor("../../models/model_glock/glock")
        
        # attaching to render
        self.weaponModel.wrtReparentTo(self.mainRef.render)
