from pandac.PandaModules import *
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pathfind import *

from panda3d.core import loadPrcFileData

#loadPrcFileData('', 'fullscreen #t')


import sys
from PlayerHUD import *
from Player import *
from EnemyManager import *
from Map import *   


class Main(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)

        # disabling Panda's default cameraHandler
        self.disableMouse()
                
        # fullscreen and hi dden cursor
        wp = WindowProperties() 
#        wp.setFullscreen(True) 
        wp.setCursorHidden(True) 
        self.win.requestProperties(wp)
        
        # esc kills our game
        self.accept("escape",sys.exit)
        
        #- Setup some default values for jump position and a key map
        self.jump = 0
        self.keyM = {
                    'left': [False, False],
                    'right':[False, False],
                    'down': [False, False],
                    'up': [False, False],
                    'jump': [False, False],
                    'inst': [False,False],
                    'about': [False,False],
                    'quit': [False,False],
                    'start': [False,False]
                    }
        
        #Dictionary containing all images used
        self.images = {}
        
        # Flag for game over
        self.gameIsOver = 0
        # Image Scale used
        self.imageScale = 1.4

        # activating fps
        base.setFrameRateMeter(True)

        # Enable particles
        base.enableParticles()
        
        # Game main FSM
        #Validate initial splash screen
        self.validateSplash = True

        #Validate Game Over
        self.validateEndGame = True

        #Define the game as a Finite State Machine
        # 'splash-screen' - for splash screen
        # 'main-menu' - for main menu
        # 'main-stage' - for the main stage
        self.state = 'splash-screen'


        #Start splash screen
        taskMgr.add(self.splashScreen, 'splash-screen')
        

        #taskMgr.add(self.mainMenu, 'main-menu')
        
        #taskMgr.add(self.endGame, 'end-game')
        
        
        ###################################################### SPLASH SCREEN ##################################################

    def splashScreen(self,task):
        "Defines the splash screen state"

        if (self.validateSplash): #Indicate first time run
            #Load required images
            self.images = {"black_screen":OnscreenImage('../../pictures/intro.jpg',color=(0,0,0,1),scale=(self.imageScale,1,1)),
                    "intro_image": OnscreenImage('../..//pictures/intro.jpg',color=(1,1,1,0),scale=(self.imageScale,1,1)),
                    "sponsor_image":OnscreenImage('../..//pictures/sponsors.png',color=(1,1,1,0),scale=(self.imageScale,1,1))}

            #Set transparency attribute
            self.images["intro_image"].setTransparency(TransparencyAttrib.MAlpha)
            self.images["sponsor_image"].setTransparency(TransparencyAttrib.MAlpha)


            #Define fade intervals
            intro_in = LerpFunc(        lambda x: self.images["intro_image"].setColor(1,1,1,x),
                                duration = 3.0,
                                toData = 1,
                                fromData = 0,
                                blendType = 'easeIn'
                                )
            intro_out = LerpFunc(        lambda x: self.images["intro_image"].setColor(1,1,1,x),
                                duration = 3.0,
                                toData = 0,
                                fromData = 1,
                                blendType = 'easeIn'
                                )
            sponsor_in = LerpFunc(        lambda x: self.images["sponsor_image"].setColor(1,1,1,x),
                                duration = 2.0,
                                toData = 1,
                                fromData = 0,
                                blendType = 'easeIn'
                                )
            sponsor_out = LerpFunc(        lambda x: self.images["sponsor_image"].setColor(1,1,1,x),
                                duration = 2.0,
                                toData = 0,
                                fromData = 1,
                                blendType = 'easeIn'
                                )
            #Play sequence
            self.splash_seq = Sequence(intro_in,intro_out,sponsor_in,sponsor_out)
            self.splash_seq.start()

            self.validateSplash = False #dont run this part of the splash again    

        #Wait splash screen
        if not self.splash_seq.isPlaying():
            #Allow next state
            self.state = 'main-menu'

            #Clean garbage
            for image in self.images.keys():
                self.images[image].destroy()
                
            #Start main menu
            taskMgr.add(self.mainMenu, 'main-menu')

            return task.done
        
        return task.cont
        
    def mainMenu(self,task):
        "Defines the main menu state"
        print "Comecei o Menu"
        # Load Music
        self.bg_music = self.loader.loadSfx("../../sounds/h_block_themesound_2.mp3")
        self.bg_music.setLoop(True)
        self.bg_music.play()

        # Show picture
        self.images["main_menu"] = OnscreenImage('../../pictures/menu.jpg',scale=(self.imageScale,1,1))

        #Define messages to be displayed
        inst_msg = "- Instructions -\n\nUse the arrow keys to move\nUse the space bar to jump\n    Press Space + Down_Arrow while on a step to fall\nSome steps are suspicious, BE CAREFUL!\n\nKill as many zombies as possible!!\n\n Hope we can have maximum degree at this game Project!\n\nAnd of course HAVE FUN! ;D\n"

        about_msg = "- About -\n\nH-Block v 0.0.0.0.1\nProgrammed by: Guilherme S. - Marcello R. - Victor T."
        
        #title_msg = "H-Block"

        options_msg = "[z]: Instructions      [x]: About      [enter]: Start      [escape]:Quit"     

        self.inst_txt = OnscreenText(text = inst_msg, pos = (0, 0.3), scale = 0.07, bg = (1, 1, 1, 0.7),align = TextNode.ACenter)
        self.about_txt = OnscreenText(text = about_msg, pos = (0, 0), scale = 0.07, bg = (1, 1, 1, 0.7),align = TextNode.ACenter)

        #self.title_txt = OnscreenText(text = title_msg, pos = (0, 0.7), scale = 0.07, bg = (1, 1, 1, 0.8),align = TextNode.ACenter)
        #self.title_txt.setScale(0.2)
        self.options_txt = OnscreenText(text = options_msg, pos = (0, -0.7), scale = 0.07, bg = (1, 1, 1, 0.3),align = TextNode.ACenter)

        self.inst_txt.hide()
        self.about_txt.hide()

        #Bind keys to key-map
        self.accept('x', self.setKey, ['inst', True])
        self.accept('x-up', self.setKey, ['inst', False])
        #self.accept('escape', self.setKey, ['quit', True])
        #self.accept('escape-up', self.setKey, ['quit', False])
        self.accept('z', self.setKey, ['about', True])
        self.accept('z-up', self.setKey, ['about', False])
        self.accept('enter', self.setKey, ['start', True])
        self.accept('enter-up', self.setKey, ['start', False])
        #Add funcion to handle the key input
        self.taskMgr.add(self.mainMenuKeys, "mainMenuKeysTask")
        
        

    def mainStage(self,task):
        "Defines the main stage state of the game"
        
        ###################################################### VARIABLES ######################################################

        #- Make a help message and hide it when the user presses the "h" key
        help_msg = "- H-Bloc -\nUse the W-A-S-D keys to move\nUse the space bar to jump\nPress shift to run faster!\nThere are Marcello-Zombies-Clones around, BE CAREFUL!\n\nPress 'h' to hide/show this help message\nGood luck!\n"

        #- Make dialog showing options of keys to press

        options_msg = "[esc]: Quit\n[h]: Help"

        #Set up time limit message and score
        self.score = 0 #points
        self.time_limit = 200 #in seconds
        time_score_message = "Remaining Time = %.1f \nScore: %i" % (self.time_limit,self.score)
        self.time_score_message = OnscreenText(text = time_score_message, pos = (-1.33, 0.94), scale = 0.07, bg = (1, 1, 1, 0.7), mayChange=1,align=TextNode.ALeft)

        #Set up help message
        self.helpMessage = OnscreenText(text = help_msg, pos = (-1.1, -0.1), scale = 0.07, bg = (1, 1, 1, 0.7),align=TextNode.ALeft)
        self.helpMessage.hide()
        self.accept('h', self.hideHelp)

        #set up options message
        self.optionsMessage = OnscreenText(text = options_msg, pos = (-1.325, 0.790), scale = 0.07, bg = (1, 1, 1, 0.7),align=TextNode.ALeft)
        
        ######################### CODE ############################
        # Bullet debug purposes
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)

        # initializing Bullet physics
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(debugNP.node())
                
        # activate bullet contact notification
        loadPrcFileData('', 'bullet-enable-contact-events true')
        
        # initializing player
        self.player = Player(self)
        # allow player collision contact handling
        self.accept('bullet-contact-added', self.player.onContactAdded)
        # setting positional audio reference to player camera
        # sounds close to camera will play louder than far ones 
        self.audio3d = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.camera)     
        
        # initializing map
        self.map = Map(self)
        
        # initializing enemy manager
        self.enemyManager = EnemyManager(self)
        
        # initializing HUD
        self.playerHUD = PlayerHUD(self)
        
        # loading theme sounds
        themeSoundShort = self.loadSfx("../../sounds/h_block_themesound_1.mp3")
        themeSoundShort.setVolume(0.2)
        themeSoundLong = self.loadSfx("../../sounds/h_block_themesound_2.mp3")
        themeSoundLong.setVolume(0.2)   
        # boolean responsible for theme sound switch
        self.switchSound = False
        # starting theme
        themeSoundLong.play()
    
        # on/off debug mode
        def toggleDebug():
            if debugNP.isHidden():
                debugNP.show()
            else:
                debugNP.hide()
        
        def update(task):
            # updating Bullet physics engine
            dt = globalClock.getDt()
            self.world.doPhysics(dt, 4, 1./120.)
            
            # theme sound check and play
            self.switchSound
            if (themeSoundLong.status() != themeSoundLong.PLAYING and not self.switchSound):
                themeSoundShort.play()
                self.switchSound = True
            elif (themeSoundShort.status() != themeSoundLong.PLAYING and self.switchSound):
                themeSoundLong.play()
                self.switchSound = False
                
            return task.cont
        
        #- Add time limit count task
        taskMgr.doMethodLater(1,self.timeLimitCount, 'time-limit-count')
        taskMgr.add(self.gameOverWatcher, 'game-over-watcher')
        taskMgr.add(update, 'update')  
        self.accept('f1', toggleDebug)
        
    def exitMainMenu(self):
        "Finishes main menu and starts game"
        #Unregister tasks
        self.taskMgr.remove("mainMenuKeysTask")
        
        # Set new state
        self.state = "main-stage"

        #Destroy texts
        self.inst_txt.destroy()
        #self.title_txt.destroy()
        self.about_txt.destroy()
        self.options_txt.destroy()
        #Stop bgm
        self.bg_music.stop()
        self.images["main_menu"].destroy()
        
        #Start main stage loop
        taskMgr.add(self.mainStage, 'main-stage')
        
            # Task to handle key input in main menu
    def mainMenuKeys(self,task):

        #Key handling
        if(self.keyM['about'][1]):
            self.about_txt.show()
        else:
            self.about_txt.hide()
            
        if(self.keyM['start'][1]):
            self.exitMainMenu()
            return        

        #if(self.keyM['quit'][1]):
        #    #Exit program
        #    sys.exit(1)

        if(self.keyM['inst'][1]):
            self.inst_txt.show()
        else:
            self.inst_txt.hide()
        return task.cont    
        # Task to handle key input in main stage
        
    #- Simple method to hide the help message on the screen
    def hideHelp(self):
        if self.helpMessage.isHidden():
            self.helpMessage.show()
        else:
            self.helpMessage.hide()

    #- Simple method to help setting keys when they are pressed/released
    def setKey(self, key, value):
        shift_value = self.keyM[key][1]
        self.keyM[key][0] = shift_value
        self.keyM[key][1] = value
        
    def timeLimitCount(self,task):
        "Counts time limit to end stage"
        #dt = globalClock.getDt()
        self.time_limit = self.time_limit - 1
        self.time_score_message.setText("Remaining Time = %.1f \nScore: %i" % (self.time_limit,self.score))

        if self.time_limit <= 0:
            #End game
            self.gameIsOver = -1
            return task.done
    
        return task.again
    
    def gameOverWatcher(self,task):
        "Watches for game over"
        if(self.gameIsOver):
            taskMgr.add(self.endGame, 'end-game')
            return task.done
        
        return task.cont    
    
    def exitMainStage(self):
        "Destroys the main stage"
        pass
    
    def endGame(self,task):
        "Handles the game over state"

        if self.gameIsOver:
            
            #Exit main Stage
            self.exitMainStage()
            
            if (self.validateEndGame):
                #First time running, do all stuff

                #Define images to make transition
                self.images["black_screen"] = OnscreenImage('../../pictures/end_screen.png',color=(0,0,0,1),scale=(self.imageScale,1,1))
                self.images["end_screen"] = OnscreenImage('../../pictures/end_screen.png',color=(1,1,1,0),scale=(self.imageScale,1,1))
                #Set transparency attribute
                self.images["end_screen"].setTransparency(TransparencyAttrib.MAlpha)

                # Destroy zombies
                for zombie in self.enemyManager.enemys:
                    if zombie.alive:
                        zombie.destroy()

                #Unregister Callbacks
                #taskMgr.remove('time-limit-count')
                #taskMgr.remove('character-movetask')
                #taskMgr.remove('loop-coins')
                #taskMgr.remove('end-sign')
                #taskMgr.remove('game-control')
                #taskMgr.remove('troll-time-count')

                #Unload Models
                #self.mapCol.removeNode()
                #self.node.removeNode()
                #self.char.delete()

                #Load Victory/Defeat sounds
                #victory_sound = self.loader.loadSfx("./music/music_zelda_victory.ogg")
                #defeat_sound = self.loader.loadSfx("./music/trombone_fail_sound.ogg")

                #Choose proper music
                chosen_music = 0
                #if self.gameIsOver == 1:
                #    chosen_sound = victory_sound
                #else:
                #    chosen_sound = defeat_sound

                #Stop bgm
                #self.bg_music.stop()


                #Define lerp function for transition
                end_in = LerpFunc(        lambda x: self.images["end_screen"].setColor(1,1,1,x),
                                    duration = 5.0,
                                    toData = 1,
                                    fromData = 0,
                                    blendType = 'easeIn'
                                    )

                end_out = LerpFunc(        lambda x: self.images["end_screen"].setColor(1,1,1,x),
                                    duration = 3.0,
                                    toData = 0,
                                    fromData = 1,
                                    blendType = 'easeIn'
                                    )

                self.end_seq = Sequence(end_in,end_out)
                self.end_seq.start()
                self.validateEndGame = False

            #Check if transition ended
            if(self.end_seq.isPlaying()):
                return task.cont


            #All finished, terminate
            sys.exit(1)

        else:
            return task.cont

main = Main()
# Starting mainLoop
main.run()