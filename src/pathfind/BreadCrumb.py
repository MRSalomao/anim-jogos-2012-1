"""
    @author: Roy Triesscheijn (http://www.royalexander.wordpress.com)
    @change by Guilherme Silva Senges
        - Adapted to Panda3D engine on Python language
    Class defining BreadCrumbs used in path finding to mark our routes
"""
from PathPoint import *

import sys

class BreadCrumb(object):

    def __init__(self, point, parent = None):
        if (type(point) == PathPoint):
            self.point = point
            self.next = parent
            self.cost = sys.float_info.max
            self.onClosedList = False
            self.onOpenList = False
        else:
            raise Exception()
        
    # overrides default Equals so we check on position instead of object memory location
    def __eq__(self, obj):
        return (type(obj) == BreadCrumb) and obj.point == self.point

    def __hash__(self):
        return self.point.__hash__()

    def compareTo(self, other):
        rValue = None
        if (self.cost < other.cost): rValue = -1
        elif (self.cost == other.cost): rValue = 0
        elif (self.cost > other.cost): rValue = 1
        return rValue
    
    
        