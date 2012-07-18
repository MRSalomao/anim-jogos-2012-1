from pandac.PandaModules import TextureStage 
from pandac.PandaModules import NodePath 
from pandac.PandaModules import CardMaker
from pandac.PandaModules import TextNode      

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
        
        # health points
        hpText=TextNode('hp')
        hpText.setText( "HP: "+str(self.mainRef.player.healthPoints) )
        self.guiHp = self.mainRef.aspect2d.attachNewNode(hpText)
        self.guiHp.setScale(0.07)
        self.guiHp.setPos(-1.2,0,-0.9)
        
        # Ammo
        ammoText=TextNode('ammo')
        ammoText.setText( "AMMO: "+str(self.mainRef.player.activeWeapon.bullets) )
        self.guiAmmo = self.mainRef.aspect2d.attachNewNode(ammoText)
        self.guiAmmo.setScale(0.07)
        self.guiAmmo.setPos(-1.2,0,-0.9+0.1)
        
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
    
    def reloadTxt(self):
        "Reload text elements"
        self.guiHp.node().setText("HP: "+ str(self.mainRef.player.healthPoints) )
        self.guiAmmo.node().setText("AMMO: "+ str(self.mainRef.player.activeWeapon.bullets))
