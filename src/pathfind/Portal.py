from pandac.PandaModules import *

class Portal(object):
    
    def __init__(self, connectedRegionsIDs, frontiers):
        
        self.frontiers = frontiers
        self.connectedRegionsIDs = connectedRegionsIDs
        
        self.frontiersVec = self.frontiers[1] - self.frontiers[0]
        
        self.middleCrossPoint = self.frontiers[0] + self.frontiersVec / 2.0
        
        self.frontiersVec.normalize()
        
        enemyRadius = 0.4
        self.crossPoints = [self.frontiers[0] + self.frontiersVec * enemyRadius,  # Points where the zombies can go through
                            self.frontiers[1] - self.frontiersVec * enemyRadius]
           
            
            
            
            
class PortalEntrance(object):
    
    def __init__(self, portal, connectedRegionID):
        self.portal = portal
        self.connectedRegionID = connectedRegionID