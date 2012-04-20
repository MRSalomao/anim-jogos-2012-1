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
        self.spawn_points = [(0,0,0)]

        # start
        taskMgr.doMethodLater(2.0, self.startInvasion, 'Start Invasion')
        
    def startRandomInvasion(self,n_enemies,mass=50,mov_force=5,max_force=15):
        "Spawns 'n_enemies' random enemies with mass 'mass', movement force 'mov_force' and max force 'max_force' in the stage, aiming for the player"
        
        # For each enemy required, spawn at different spawn point
        for i in range(n_enemies):
            # Choose spawn point
            random.seed()
            chosen_spawn_point = random.choice(self.spawn_points)

            # Creating enemy
            enemy = Enemy(self.mainRef,'enemy_'+str(i))
            self.enemys.append(enemy)
            enemy.setPos(chosen_spawn_point[0],chosen_spawn_point[1],chosen_spawn_point[2])
            
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
        print rigid_node_target.getNode()
        NodePath(rigid_node_target.getNode()).remove_node()
        