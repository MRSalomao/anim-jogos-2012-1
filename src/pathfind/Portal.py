from pandac.PandaModules import *

class Portal(object):
    
    def __init__(self, connectedRegionsIDs, frontiers):
        self.frontiers = frontiers
        self.connectedRegionsIDs = connectedRegionsIDs
        
        self.crossPoints = []       # Points where the zombies can go through
        
        numberOfCrossPoints = 3     # 3 seems a good value, but we can change this
        deltaV = []
        deltaV.append((self.frontiers[1][0] - self.frontiers[0][0]) / (numberOfCrossPoints + 2) )    # ex:     | * * * |      (  '|'=frontier ;  '*'=crossPoint  )
        deltaV.append((self.frontiers[1][1] - self.frontiers[0][1]) / (numberOfCrossPoints + 2) )
        deltaV.append((self.frontiers[1][2] - self.frontiers[0][2]) / (numberOfCrossPoints + 2) )
        
        for i in range(numberOfCrossPoints):
            crossPoint = [self.frontiers[0][0] + deltaV[0] * i, 
                          self.frontiers[0][1] + deltaV[1] * i, 
                          self.frontiers[0][1] + deltaV[2] * i]
            self.crossPoints.append(crossPoint)