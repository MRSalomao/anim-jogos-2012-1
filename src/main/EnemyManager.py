from direct.task import Task
from Enemy import *

import random

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # array containing enemy objects
        self.enemys = []
        
        # List of points 3-D space in which enemies can spawn at
        self.spawn_points = [Point3(2, 2, 0.09),Point3(-2, -2, 0.09)]

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
            enemy = Enemy(self.mainRef,'enemy_' + str(i),chosen_spawn_point)
            self.enemys.append(enemy)
            
            # pursue on path find
            enemy.pursue()
        
    def startInvasion(self,task):
        self.startRandomInvasion(1)
        
        return task.done

    def handleShot(self,rigid_node_target):
        # Handles how player shots affect zombies
        
        # global targettedEnemy
        targetNode = NodePath(rigid_node_target.getNode())
        targetNodeName = targetNode.getName(
                                            )
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