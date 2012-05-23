"""
    @author MinHeap from ZeraldotNet (http://zeraldotnet.codeplex.com/)
    @change Modified by Roy Triesscheijn (http://royalexander.wordpress.com)    
        -Moved method variables to class variables
        -Added English Exceptions and comments (instead of Chinese)
    @change by Guilherme Silva Senges
        - Adapted to Panda3D engine on Python language  
"""

from pathfind import BreadCrumb
from pathfind import Point3D

class MinHeap(object):

    def __init__(self, capacity = 16, isVertexPosOriented = False, desiredAxis = None):
        self.count = 0 # how many on the heap
        self.capacity = capacity
        self.array = [None]*capacity
        self.isVertexPosOriented = isVertexPosOriented
        self.desiredAxis = desiredAxis
    
    def getCount(self):
        return self.count

    def BuildHead(self):
        position = (self.count - 1) >> 1
        while (position >= 0):
            self.MinHeapify(position)
            position -= 1

    def Add(self, item):
        self.count += 1
        if (self.count > self.capacity):
            self.DoubleArray()
        self.array[self.count - 1] = item
        position = self.count - 1

        parentPosition = ((position - 1) >> 1)

        if ( not(self.isVertexPosOriented) ):
            while ( (position > 0) and (self.array[parentPosition].compareTo(self.array[position]) > 0) ):
                self.temp = self.array[position]
                self.array[position] = self.array[parentPosition]
                self.array[parentPosition] = self.temp
                position = parentPosition
                parentPosition = ((position - 1) >> 1)
        else: 
            while ( (position > 0) and (self.array[parentPosition].compareToPos(self.array[position], self.desiredAxis) > 0) ):
                self.temp = self.array[position]
                self.array[position] = self.array[parentPosition]
                self.array[parentPosition] = self.temp
                position = parentPosition
                parentPosition = ((position - 1) >> 1)  

    def DoubleArray(self):
        self.capacity <<= 1
        self.tempArray = [self.capacity]
        self.CopyArray(self.array, self.tempArray)
        self.array = self.tempArray

    def CopyArray(self, source, destination):
        for index in range( len(source) ):
            destination[index] = source[index]

    def Peek(self):
        if (self.count == 0):
            # Heap is empty
            raise Exception()
        return self.array[0]


    def ExtractFirst(self):
        if (self.count == 0):
            # "Heap is empty"
            raise Exception()
        self.temp = self.array[0]            
        self.array[0] = self.array[self.count - 1]
        self.count -= 1
        self.MinHeapify(0)
        return self.temp

    def MinHeapify(self, position):
        while (True):
            left = ((position << 1) + 1)
            right = left + 1
            minPosition = None
            
            if (not(self.isVertexPosOriented)):
                if ( (left < self.count) and (self.array[left].compareTo(self.array[position]) < 0) ):
                    minPosition = left
                else:
                    minPosition = position
    
                if ( (right < self.count) and (self.array[right].compareTo(self.array[minPosition]) < 0) ):
                    minPosition = right
            else:
                if ( (left < self.count) and (self.array[left].compareToPos(self.array[position], self.desiredAxis) < 0) ):
                    minPosition = left
                else:
                    minPosition = position
    
                if ( (right < self.count) and (self.array[right].compareToPos(self.array[minPosition], self.desiredAxis) < 0) ):
                    minPosition = right
            
            if (minPosition != position):
                self.mheap = self.array[position]
                self.array[position] = self.array[minPosition]
                self.array[minPosition] = self.mheap
                position = minPosition
            else:
                return
