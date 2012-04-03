from pandac.PandaModules import TextureStage 
from pandac.PandaModules import NodePath 
from pandac.PandaModules import CardMaker       

class PlayerHUD(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference  
        
        SCREEN_WIDTH = 800 
        SCREEN_HEIGHT = 600 

        sprites_root = self.createSpritesNodeSetup(SCREEN_WIDTH, SCREEN_HEIGHT, self.mainRef.render2d)
        
        # crosshair init
        self.crosshairSprite = self.createSprite('../../textures/crosshair.png', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 16, 16, 1) 
        self.crosshairSprite.reparentTo(sprites_root)
        
    def createSpritesNodeSetup(self,screenWidth, screenHeight, parent): 
    
        aspect_ratio = parent.getScale()[0]    
         
        screenOrigin = parent.attachNewNode('screen_origin') 
        screenNode = screenOrigin.attachNewNode('screen_node') 
        
        screenOrigin.setPos(-1.0/aspect_ratio, 0.0, 1.0) 
        screenOrigin.setScale(2.0, 1.0, -2.0) 
        
        screenNode.setPos(0, 0, 0) 
         
        screenNode.setScale(1.0/(aspect_ratio*screenWidth), 1.0, 1.0/screenHeight) 
        screenNode.setTexScale(TextureStage.getDefault(), 1.0, -1.0) 
         
        # test some points    
        #   points = [(0,0), (screenWidth, 0), (screenWidth, screenHeight), (screenWidth/2.0, screenHeight/2.0), (0, screenHeight)] 
        #   for pt in points: 
        #      print '%s -> %s' % (pt, str(parent.getRelativePoint(screenNode, Vec3(pt[0], 0, pt[1])))) 
         
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