
class Region(object):

    def __init__(self, regionID):
        self.regionID = regionID
        self.neighbourIDs = []
        self.vertices = []
        self.portalsList = []
        
    def chagedRegion(self, currentRegion):
        
        return 0