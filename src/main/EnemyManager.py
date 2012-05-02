from direct.task import Task
from panda3d.ai import *
import random
from Enemy import *

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.AIchar = []
        self.AIbehaviors = []
        self.enemys = []
        
        # List of points 3-D space in which enemies can spawn at
        self.spawn_points = [(0,0,0),(30,15,0),(60,0,0)]

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
            enemy = Enemy(self.mainRef,'enemy_'+str(i))
            enemy.setPos(chosen_spawn_point[0],chosen_spawn_point[1],chosen_spawn_point[2])
            self.enemys.append(enemy)
            
            
            # Creating pursue behavior
            self.AIchar.append(AICharacter('seeker_'+str(i),enemy.np, mass, mov_force, max_force))
            self.mainRef.AIworld.addAiChar(self.AIchar[i])
            self.AIbehaviors.append(self.AIchar[i].getAiBehaviors())
            self.AIbehaviors[i].pursue(self.mainRef.player.playerNP)
        
        

    def startInvasion(self,task):
        self.startRandomInvasion(1)
        
        return task.done

    def handleShot(self,rigid_node_target):
        "Handles how player shots affect zombies"
        # Erase zombies that are hit
        
        global targettedEnemy
        targettedEnemy = None
       
        for hit in rigid_node_target.getHits():
            print NodePath(hit.getNode())
            print NodePath(hit.getNode()).getParent()
            if ( (NodePath(hit.getNode()).getName().find('enemy_') != -1) and (targettedEnemy == None) ):
            	print 'entrei A'
                strIndex = NodePath(hit.getNode()).getName().replace('enemy_','')
                index = int(strIndex)
                targettedEnemy = self.enemys[index]
                if (targettedEnemy.lifePoints > 0):
                    targettedEnemy.lifePoints -= 10
                else:
                    targettedEnemy.hide()
                
            elif ( ( NodePath(hit.getNode()).hasParent() ) and (targettedEnemy != None) and ( NodePath(hit.getNode()).getParent().getNode(2).getName() == targettedEnemy.name ) ):
            	print 'entrei B'
                if ( NodePath(hit.getNode()).getName() == 'arm_lr'):
                    if (targettedEnemy.hitPoints['arm_lr'] > 0):
                        targettedEnemy.hitPoints['arm_lr'] -= 1
                    else:
                        NodePath(hit.getNode()).detachNode()
                elif ( NodePath(hit.getNode()).getName() == 'arm_ll'):
                    if (targettedEnemy.hitPoints['arm_ll'] > 0):
                        targettedEnemy.hitPoints['arm_ll'] -= 1
                    else:
                        NodePath(hit.getNode()).detachNode()
                elif ( NodePath(hit.getNode()).getName() == 'leg_lr'):
                    if (targettedEnemy.hitPoints['leg_lr'] > 0):
                        targettedEnemy.hitPoints['leg_lr'] -= 1
                    else:
                        NodePath(hit.getNode()).detachNode()
                elif ( NodePath(hit.getNode()).getName() == 'leg_ll'):
                    if (targettedEnemy.hitPoints['leg_ll'] > 0):
                        targettedEnemy.hitPoints['leg_ll'] -= 1
                    else:
                        NodePath(hit.getNode()).detachNode()
        