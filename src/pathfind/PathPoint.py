from Point3D import *

class PathPoint(Point3D):        

    def __init__(self, X, Y, Z, arrayID = None, gridPosX = None, gridPosY = None, gridPosZ = None):
        super(PathPoint, self).__init__(X, Y, Z)
        
        self.gridPosX = gridPosX
        self.gridPosY = gridPosY
        self.gridPosZ = gridPosZ
        
        self.arrayID = arrayID
        
    def __add__(self,obj):
        return PathPoint(self.X + obj.X, self.Y + obj.Y, self.Z + obj.Z, self.arrayID, self.gridPosX + obj.gridPosX, self.gridPosY + obj.gridPosY, self.gridPosZ + obj.gridPosZ)

    def __radd__(self,obj):
        return PathPoint(self.X + obj.X, self.Y + obj.Y, self.Z + obj.Z, self.arrayID, self.gridPosX + obj.gridPosX, self.gridPosY + obj.gridPosY, self.gridPosZ + obj.gridPosZ)

    def __sub__(self,obj):
        return PathPoint(self.X - obj.X, self.Y - obj.Y, self.Z - obj.Z, self.arrayID, self.gridPosX, self.gridPosY, self.gridPosZ)
    
    def __rsub__(self,obj):
        return PathPoint(obj.X - self.X, obj.Y - self.Y, obj.Z - self.Z, self.arrayID, self.gridPosX, self.gridPosY, self.gridPosZ)