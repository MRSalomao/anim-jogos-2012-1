from direct.task import Task
from panda3d.ai import *

from Enemy import *

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.AIchar = []
        self.AIbehaviors = []
        self.enemys = []
        for i in range(5):
            enemy = Enemy(self.mainRef,'enemy'+str(i))
#            enemy.hide()
            self.enemys.append(enemy)
            enemy.setPos(-50*i,5,0)
            
            # creating pursue behavior
            self.AIchar.append(AICharacter('seeker'+str(i),enemy.np, 50, 1, 6))
            self.mainRef.AIworld.addAiChar(self.AIchar[i])
            self.AIbehaviors.append(self.AIchar[i].getAiBehaviors())
            self.AIbehaviors[i].pursue(self.mainRef.player.playerNP)
            
        def startInvasion(task):
            for i in range(5):
                enemy = self.enemys[i]
                enemy.show()
            return task.done

        # start
#        taskMgr.doMethodLater(2.0, startInvasion, 'Start Invasion')