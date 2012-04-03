from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker       

class PlayerHUD(object):

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        cm = CardMaker('spritesMaker') 
        cm.setFrame(-0.5, 0.5, -0.5, 0.5) 
        sprite = cm.generate()    
        
        # crosshair init
        tex = loader.loadTexture('crosshair.png') 
        spriteNP = NodePath(sprite)    
        spriteNP.setTexture(tex) 
        spriteNP.setPos(0, 0, 0) 
        spriteNP.setScale(1.0, 1.0, 1.0)
        # enable transparency
        spriteNP.setTransparency(1)
