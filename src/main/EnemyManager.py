from direct.task import Task
from Enemy import *
from pathfind.SpawnPoint import *

import random

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # array containing enemy objects
        self.enemys = []
        self.activeEnemys = 0
        self.maxEnemys = 5
        # list of spawn points available
        self.spawnPointsList = []
        
        self.spawnPointGeometry = loader.loadModel("../../models/H_Block/H_Block_SpawnPts")
        
        for spawnPoint in self.spawnPointGeometry.getChild(0).getChildren():
            self.spawnPointsList.append( SpawnPoint( Point3(spawnPoint.getPos()) + Vec3(0,0,1), int( spawnPoint.getNode(0).getTag("prop") ) ) ) # creates new spawn point with specified coordinate and regionID
            # Debug
#            print self.spawnPointsList[-1].regionID, self.spawnPointsList[-1].position

        # start
        taskMgr.doMethodLater(1.0, self.startInvasion, 'Start Invasion')
        
    def spawnEnemy(self,mass=50,mov_force=1,max_force=5):
        "Spawns 'n_enemies' random enemies with mass 'mass', movement force 'mov_force' and max force 'max_force' in the stage, aiming for the player"
        
        # New enemy index
        enemy_index = len(self.enemys)
 
        # Choose spawn point
        randSpawnPointIndex = random.randrange( 0, len(self.spawnPointsList) )
        chosenSpawnPoint = self.spawnPointsList[ randSpawnPointIndex ]
        
        # Creating enemy
        if(self.activeEnemys < self.maxEnemys):
            # Debug
#            print "[Spawn] Enemy %d spawned at point (%f,%f,%f) in Region %d" % (enemy_index,chosenSpawnPoint.position.getX(),chosenSpawnPoint.position.getY(),chosenSpawnPoint.position.getZ(),chosenSpawnPoint.regionID)
            enemy = Enemy(self.mainRef,'enemy_' + str(enemy_index), chosenSpawnPoint.position, chosenSpawnPoint.regionID)
            self.activeEnemys+=1
            self.enemys.append(enemy)  
    
    def disseminateTargetNewRegion(self):
        self.enemyIndex = 0
        disseminationStep = 0.04 # time between each zombie updatePath call
        self.mainRef.taskMgr.remove('region_dissemination') # removes an old disseminate task if exists one
        if len(self.enemys) > 0:
            self.mainRef.taskMgr.doMethodLater(disseminationStep, self.newRegionDissemination, 'region_dissemination')
    
    def newRegionDissemination(self,task):
        if self.enemys[self.enemyIndex].alive == True:
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
        self.spawnEnemy()
        
        return task.again

    def handleShot(self,rigid_node_target):
        # Handles how player shots affect zombies
        
        # global targettedEnemy
        targetNode = NodePath(rigid_node_target.getNode())
        targetNodeName = targetNode.getName()
        #print targetNodeName
#        print NodePath(hit.getNode())
#        print NodePath(hit.getNode()).getParent()
        if ( targetNodeName.find('enemy') != -1):
            enemyIndex = int(targetNodeName.split("_")[-1])
            attackedLimb = targetNodeName[:targetNodeName.rfind("_",0,targetNodeName.rfind("_"))]
            

            
            damage = 10
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
            elif ( attackedLimb == 'head'):
                damage = 50
            self.enemys[enemyIndex].lifePoints -= damage
                
            print "[Attack] Attacked Enemy_%d at %s with damage %d" % (enemyIndex,attackedLimb,damage)
            if (self.enemys[enemyIndex].lifePoints <= 0):
                print "[Enemy] Destroying Enemy_%d" % (enemyIndex)
                self.enemys[enemyIndex].destroy()
                self.activeEnemys-=1
                self.mainRef.score += 1
            