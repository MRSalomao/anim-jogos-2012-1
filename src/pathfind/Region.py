
class Region(object):

    def __init__(self, regionID):
        self.regionID = regionID
        self.vertices = []
        
        self.neighbourIDs = [] # OBS: self.neighbourIDs[i] corresponds to self.portalsList[i]
        self.portalsList = []
        
    def chagedRegion(self, currentRegion):
        
        return 0