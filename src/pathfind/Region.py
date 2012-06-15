
class Region(object):
    vertices = []
    regionID = 0
    neighbourIDs = []
    portalsList = []
    
    def __init__(self, regionID, neighbourIDs):
        self.regionID = regionID
        self.neighbourIDs = neighbourIDs