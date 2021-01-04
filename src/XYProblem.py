#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "Class for problem modelisation"
__version__ = "1.0"

from math import sqrt
import numpy as np

from src.SearchNode import SearchNode


class XYProblem:
    """ Used to create problem modelisation
    Create N random point in a 2D space
    """

    def __init__(self, nbPoints, start, end=None):
        self._start = SearchNode(start, 0)
        self._end = end

        self._cities = {}
        for i in range(nbPoints):
            x = np.random.randint(0, 50)
            y = np.random.randint(0, 50)
            self._cities[i] = (x, y)

    def __len__(self):
        return len(self._cities)

    @property
    def Start(self):
        return self._start

    @property
    def End(self):
        return self._end.Value

    def GetMax(self):
        """ Get min and max value of position (for display)
        """
        start = True
        minX = 0
        minY = 0
        for val in self._cities.values():
            if start:
                maxX, maxY = val
                minX, minY = val
                start = False
            else:
                x, y = val
                if maxX < x: maxX = x
                if maxY < y: maxY = y

                if minX > x: minX = x
                if minY > y: minY = y

        return maxX, maxY, minX, minY

    def GetNext(self, prev):
        next = []
        prev_pos = self._cities[prev.Value]
        for name, position in self._cities.items():
            if name != prev.Value:
                next.append(SearchNode(name, self._distance(prev_pos, position)))

        return next

    def _distance(self, pos1, pos2):
        """
        Euclidian distance
        :param pos1: tuple of (x, y) position
        :param pos2: tuple of (x, y) position
        :return: distance
        """
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def isEnd(self, node):
        return node == self._end
