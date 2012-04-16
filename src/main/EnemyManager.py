from direct.task import Task

from Enemy import *

class EnemyManager(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.enemys = []
        for i in range(30):
            enemy = Enemy(self.mainRef)
            enemy.hide()
            self.enemys.append(enemy)
            enemy.setPos(10*i,5*1,2)
        
        def startInvasion(task):
            for i in range(30):
                enemy = self.enemys.__getitem__(i)
                enemy.show()
            return task.done

        # start
        taskMgr.doMethodLater(10.0, startInvasion, 'Start Invasion')
            
    