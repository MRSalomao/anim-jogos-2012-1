from direct.task import Task
from Enemy import *
from pathfind.SpawnPoint import *

import random

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # array containing enemy objects
        self.enemys = []
        
        # list of spawn points available
        self.spawnPointsList = []
        
        self.spawnPointGeometry = loader.loadModel("../../models/H_Block/H_Block_SpawnPts")
        
        for spawnPoint in self.spawnPointGeometry.getChild(0).getChildren():
            self.spawnPointsList.append( SpawnPoint( Point3(spawnPoint.getPos()) + Vec3(0,0,1), int( spawnPoint.getNode(0).getTag("prop") ) ) ) # creates new spawn point with specified coordinate and regionID
#            print self.spawnPointsList[-1].regionID, self.spawnPointsList[-1].position

        # start
        taskMgr.doMethodLater(5.0, self.startInvasion, 'Start Invasion')
        
    def startRandomInvasion(self,n_enemies,mass=50,mov_force=1,max_force=5):
        "Spawns 'n_enemies' random enemies with mass 'mass', movement force 'mov_force' and max force 'max_force' in the stage, aiming for the player"
        
        # For each enemy required, spawn at different spawn point
        for i in range(n_enemies):
            # Choose spawn point
            chosenSpawnPoint = self.spawnPointsList[ random.randrange( 1, len(self.spawnPointsList) ) ]

            # Creating enemy
            if(len(self.enemys) < 4):
                enemy = Enemy(self.mainRef,'enemy_' + str(i), chosenSpawnPoint.position, chosenSpawnPoint.regionID)
                self.enemys.append(enemy)  
    
    def disseminateTargetNewRegion(self):
        print "disseminate"
        self.enemyIndex = 0
        disseminationStep = 0.04 # time between each zombie updatePath call
        self.mainRef.taskMgr.remove('region_dissemination') # removes an old disseminate task if exists one
        self.mainRef.taskMgr.doMethodLater(disseminationStep, self.newRegionDissemination, 'region_dissemination')
    
    def newRegionDissemination(self,task):
        print "disseminate step"
        self.enemys[self.enemyIndex].updatePath()
        if (self.enemyIndex < (len(self.enemys) - 1) ):
            self.enemyIndex += 1
        else:
            return task.done
        return task.again
        
#        for enemy in self.enemys:
#            enemy.updatePath()
    
    # TODO: do BFS on each region from where player is trying to find spawn_points
    # TODO: distribute enemys randomly from first possible region based on previous BFS
    def startInvasion(self,task):
#        self.exploredRegions = []
#        self.exploredRegions.append(self.mainRef.map.convexRegions[self.mainRef.player.currentRegion - 1])
#        
#        while (self.exploredRegions):
#            region = self.exploredRegions.pop()
#            for (neighbor in region.)
        self.startRandomInvasion(1)
        
        return task.again

    def handleShot(self,rigid_node_target):
        # Handles how player shots affect zombies
        
        # global targettedEnemy
        targetNode = NodePath(rigid_node_target.getNode())
        targetNodeName = targetNode.getName()
#        print NodePath(hit.getNode())
#        print NodePath(hit.getNode()).getParent()
        if ( targetNodeName.find('enemy') != -1):
            enemyIndex = int(targetNodeName[-1])
            attackedLimb = targetNodeName[:targetNodeName.rfind("_",0,targetNodeName.rfind("_"))]
            
#            print "[Attack] Atacando Enemy_%d no membro %s" % (enemyIndex,attackedLimb)
            
            if (self.enemys[enemyIndex].lifePoints > 0):
                self.enemys[enemyIndex].lifePoints -= 10
            else:
#                print "[Destroy] Destruindo Enemy_%d" % (enemyIndex)
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