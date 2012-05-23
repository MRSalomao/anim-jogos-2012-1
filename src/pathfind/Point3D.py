"""    
    @author: Roy Triesscheijn (http://www.royalexander.wordpress.com)
    @change by Guilherme Silva Senges
        - Adapted to Panda3D engine on Python language
    Point3D class mimics some of the Microsoft.Xna.Framework.Vector3
    but uses Int32's instead of floats.
"""

class Point3D(object):        

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def getDistanceSquared(self, point):
        dx = self.X - point.X
        dy = self.Y - point.Y
        dz = self.Z - point.Z
        return (dx * dx) + (dy * dy) + (dz * dz)         

    def __eq__(self, obj):
        p3d = obj
        return (p3d.X == self.X) and (p3d.Z == self.Z) and (p3d.Y == self.Y)
        

    def __hash__(self):
        return (self.X + " " + self.Y + " " + self.Z).__hash__()

    def __str__(self):
        return str(self.X) + ", " + str(self.Y) + ", " + str(self.Z)

    def __ne__(self, obj):
        p3d = obj
        return (p3d.X != self.X) and (p3d.Z != self.Z) and (p3d.Y != self.Y)

    def __add__(self,obj):
        return Point3D(self.X + obj.X, self.Y + obj.Y, self.Z + obj.Z)

    def __radd__(self,obj):
        return Point3D(self.X + obj.X, self.Y + obj.Y, self.Z + obj.Z)

    def __sub__(self,obj):
        return Point3D(self.X - obj.X, self.Y - obj.Y, self.Z - obj.Z)
    
    def __rsub__(self,obj):
        return Point3D(obj.X - self.X, obj.Y - self.Y, obj.Z - self.Z )
    
    def compareToPos(self, other, desiredAxis):
        rValue = None
        if (desiredAxis == "X" or desiredAxis == "x"):
            if (self.X < other.X):    rValue = -1
            elif (self.X == other.X): rValue = 0
            elif (self.X > other.X):  rValue = 1
        elif (desiredAxis == "Y" or desiredAxis == "y"):
            if (self.Y < other.Y):    rValue = -1
            elif (self.Y == other.Y): rValue = 0
            elif (self.Y > other.Y):  rValue = 1
        elif (desiredAxis == "Z" or desiredAxis == "z"):
            if (self.Z < other.Z):    rValue = -1
            elif (self.Z == other.Z): rValue = 0
            elif (self.Z > other.Z):  rValue = 1
        else:
            # invalid argument
            raise Exception()
        return rValue