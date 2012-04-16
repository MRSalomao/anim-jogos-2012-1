from pandac.PandaModules import TextureStage 
from pandac.PandaModules import NodePath 
from pandac.PandaModules import CardMaker       

class PlayerHUD(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.winSizeX = self.mainRef.win.getProperties().getXSize() 
        self.winSizeY = self.mainRef.win.getProperties().getYSize()  

        # parent of all sprites
        sprites_root = self.createSpritesNodeSetup()
        
        # crosshair init
        self.crosshairSprite = self.createSprite('../../textures/crosshair.png', self.winSizeX/2, self.winSizeY/2, 16, 16, 1) 
        self.crosshairSprite.reparentTo(sprites_root)

#---Panda collision for our crosshair---Incomplete        
#        # adding collision node to our crosshair. Based on camera.
#        self.pickerNode=CollisionNode('crosshairraycnode')
#        self.crosshairNP=base.camera.attachNewNode(self.pickerNode)
#        self.crosshairRay=CollisionRay(Point3(0,0,0),Vec3(0,1,0))
#        self.pickerNode.addSolid(self.crosshairRay)
#        self.pickerNode.setIntoCollideMask(BitMask32.allOff())
#        base.cTrav.addCollider(self.crosshairNP, collisionHandler)
#        
#        # collision handler methods
#        def collideStudentChairIn(entry):
#            print "colisao de entrada"
#        def collideStudentChairOut(entry):
#            print "colisao de saida"
#        
#        # adding a pattern - eases readability
#        collisionHandler.addInPattern('%fn-into-%in')
#        collisionHandler.addOutPattern('%fn-out-%in')
#
#        # accepting student chair collision
#        self.accept('crosshairraycnode-into-student_chaircnode', collideStudentChairIn)
#        self.accept('crosshairraycnode-out-student_chaircnode', collideStudentChairOut)
        
    def createSpritesNodeSetup(self): 
    
        aspect_ratio = self.mainRef.render2d.getScale()[0]    
         
        screenOrigin = self.mainRef.render2d.attachNewNode('screen_origin') 
        screenNode = screenOrigin.attachNewNode('screen_node') 
        
        screenOrigin.setPos(-1.0/aspect_ratio, 0.0, 1.0) 
        screenOrigin.setScale(2.0, 1.0, -2.0) 
        
        screenNode.setPos(0, 0, 0) 
         
        screenNode.setScale(1.0/(aspect_ratio*self.winSizeX), 1.0, 1.0/self.winSizeY) 
        screenNode.setTexScale(TextureStage.getDefault(), 1.0, -1.0)  
         
        return screenNode 


    def createSprite(self,filename, x, z, sx, sz, transparent = 1):
        
        cm = CardMaker('spritesMaker') 
        cm.setFrame(-0.5, 0.5, -0.5, 0.5) 
        sprite = cm.generate()    
        
        tex = loader.loadTexture(filename) 
        
        spriteNP = NodePath(sprite)    
        
        spriteNP.setTexture(tex) 
        spriteNP.setPos(x, 0, z) 
        spriteNP.setScale(sx, 1.0, sz) 
        spriteNP.setTransparency(transparent)
         
        return spriteNP