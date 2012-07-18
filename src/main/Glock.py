from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *

from Weapon import *

class Glock(Weapon):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        super(Glock, self).__init__(mainReference)
        
        # load our glock model
        self.weaponModel = Actor("../../models/model_glock/glock")
        # ****SCALE****
        self.weaponModel.setScale(0.1)
        # ***POS***
        self.weaponModel.setPos(0.6,3.0,1.5)
        # ****HPR****
        self.weaponModel.setHpr(280,0.3,2.3)
        # attaching to render
        self.weaponModel.wrtReparentTo(self.mainRef)
        
        # Number of bullets held by the gun
        self.bullets_max = 10
        self.bullets = self.bullets_max
        self.reloadTime = 2
        
    def shootAnim(self):
        super(Glock, self).shootAnim()
        
        seq=Sequence()
        seq.append( self.weaponModel.hprInterval(0.02,Point3(280,0,10), Point3(280,0,2) ) )
        seq.append( self.weaponModel.hprInterval(0.05,Point3(280,0, 2), Point3(280, 0, 10) ) )
        seq.start()

    def reloadAnim(self):
        old_pos = self.weaponModel.getPos()
        new_pos = Point3(self.weaponModel.getX(),self.weaponModel.getY(),self.weaponModel.getZ()-1)
        
        seq=Sequence()
        seq.append( self.weaponModel.posInterval(0.2,new_pos,startPos=old_pos))
        seq.append( self.weaponModel.posInterval(self.reloadTime-0.4,new_pos,startPos=new_pos))
        seq.append( self.weaponModel.posInterval(0.2,old_pos,startPos=new_pos))
        seq.start()
        
        