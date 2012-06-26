from direct.task import Task
from panda3d.ai import *
from Enemy import *
from pathfind.PathPoint import *

import random

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
#        self.AIchar = []
#        self.AIbehaviors = []
        self.enemys = []
        
        # List of points 3-D space in which enemies can spawn at
        self.spawn_points = [(2, 2, 3),(-2,-2,3),(1,1,3),(-1,-1,3),(2,3,3),(-2,-1,3),(-1,-2,3),(-1,3,3)]

        # start
        taskMgr.doMethodLater(2.0, self.startInvasion, 'Start Invasion')
        
    def startRandomInvasion(self,n_enemies,mass=50,mov_force=1,max_force=5):
        "Spawns 'n_enemies' random enemies with mass 'mass', movement force 'mov_force' and max force 'max_force' in the stage, aiming for the player"
        
        # For each enemy required, spawn at different spawn point
        for i in range(n_enemies):
            # Choose spawn point
            random.seed()
            chosen_spawn_point = random.choice(self.spawn_points)

            # Creating enemy
            enemy = Enemy(self.mainRef,'enemy_'+str(i),chosen_spawn_point)
            self.enemys.append(enemy)
            
            # setting position that is valid for our path finder grid
            "self.spawnP = PathPoint(-94,0,-66,None,1,2,0)"
            #enemy.setPos(self.spawnP.X,self.spawnP.Y,self.spawnP.Z)
            "enemy.spawnP = self.spawnP"
            
            # enemy update for path finding pursue
            self.playerWorldCurrPos = None
            self.playerWorldPastPos = None
#            self.playerNP = self.mainRef.player.playerNP
            """def enemyUpdate(task):
                # getting player world position and verifying if has changed
                self.playerWorldCurrPos = self.playerNP.getPos()
                if (self.playerWorldPastPos == None):
                    enemy.pursue(self.mainRef.map.AIworld, self.mainRef.map.pathPoints, self.playerNP, self.mainRef.map.xPosInterval, self.mainRef.map.yPosInterval, self.mainRef.map.zPosInterval)
                    self.playerWorldPastPos = self.playerWorldCurrPos
                elif ( (self.playerWorldCurrPos.getX() != self.playerWorldPastPos.getX() ) or (self.playerWorldCurrPos.getY() != self.playerWorldPastPos.getY() ) or (self.playerWorldCurrPos.getZ() != self.playerWorldPastPos.getZ() ) ):
                    enemy.pursue(self.mainRef.map.AIworld, self.mainRef.map.pathPoints, self.playerNP, self.mainRef.map.xPosInterval, self.mainRef.map.yPosInterval, self.mainRef.map.zPosInterval)
                    self.playerWorldPastPos = self.playerWorldCurrPos
                return task.cont
            taskMgr.add(enemyUpdate, 'enemyUpdate')"""
            
            # pursue on path find
            enemy.pursue()
            
############# Old pursue algorithm           
            # Creating pursue behavior
#            self.AIchar.append(AICharacter('seeker_'+str(i),enemy.np, mass, mov_force, max_force))
#            self.mainRef.AIworld.addAiChar(self.AIchar[i])
#            self.AIbehaviors.append(self.AIchar[i].getAiBehaviors())
#            self.AIbehaviors[i].pursue(self.mainRef.player.playerNP)
#############
        
    def startInvasion(self,task):
        self.startRandomInvasion(6)
        
        return task.done

    def handleShot(self,rigid_node_target):
        "Handles how player shots affect zombies"
        # Erase zombies that are hit
        
        #global targettedEnemy
        targetNode = NodePath(rigid_node_target.getNode())
        targetNodeName = targetNode.getName(
                                            )
        #print NodePath(hit.getNode())
        #print NodePath(hit.getNode()).getParent()
        if ( targetNodeName.find('enemy') != -1):
            enemyIndex = int(targetNodeName[-1])
            attackedLimb = targetNodeName[:targetNodeName.rfind("_",0,targetNodeName.rfind("_"))]
            
            print "[Attack] Atacando Enemy_%d no membro %s" % (enemyIndex,attackedLimb)
            
            if (self.enemys[enemyIndex].lifePoints > 0):
                self.enemys[enemyIndex].lifePoints -= 10
            else:
                print "[Destroy] Destruindo Enemy_%d" % (enemyIndex)
                taskMgr.remove( str(self.enemys[enemyIndex].name) )
                self.enemys[enemyIndex].destroy()
            
        
            if ( attackedLimb == 'arm_lr'):
                if (self.enemys[enemyIndex].hitPoints['arm_lr'] > 0):
                    self.enemys[enemyIndex].hitPoints['arm_lr'] -= 1
                else:
                    self.enemys[enemyIndex].detachLimb(attackedLimb)
                    
            elif ( attackedLimb == 'arm_ll'):
                if (self.enemys[enemyIndex].hitPoints['arm_ll'] > 0):
                    self.enemys[enemyIndex].hitPoints['arm_ll'] -= 1
                else:
                    self.enemys[enemyIndex].detachLimb(attackedLimb)
                    
            elif ( attackedLimb == 'leg_lr'):
                if (self.enemys[enemyIndex].hitPoints['leg_lr'] > 0):
                    self.enemys[enemyIndex].hitPoints['leg_lr'] -= 1
                else:
                    self.enemys[enemyIndex].detachLimb(attackedLimb)
                    
            elif ( attackedLimb == 'leg_ll'):
                if (self.enemys[enemyIndex].hitPoints['leg_ll'] > 0):
                    self.enemys[enemyIndex].hitPoints['leg_ll'] -= 1
                else:
                    self.enemys[enemyIndex].detachLimb(attackedLimb)
          