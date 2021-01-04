#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "Class for problem modelisation"
__version__ = "1.0"

from math import pi, cos, asin, sqrt

from src.SearchNode import SearchNode


class CityProblem:
    """ Used to create problem modelisation
    """
    def __init__(self, start, end=None):
        self._start = SearchNode(start, 0)
        self._end = end

        self._cities = {
            "Bordeaux": (44.833333, -0.566667), "Paris": (48.8566969, 2.3514616), "Nice": (43.7009358, 7.2683912),
            "Lyon": (45.7578137, 4.8320114), "Nantes": (47.2186371, -1.5541362), "Brest": (48.4, -4.483333),
            "Lille": (50.633333, 3.066667), "Clermont-Ferrand": (45.783333, 3.083333), "Strasbourg": (48.583333, 7.75),
            "Poitiers": (46.583333, 0.333333), "Angers": (47.466667, -0.55), "Montpellier": (43.6, 3.883333),
            "Caen": (49.183333, -0.35), "Rennes": (48.083333, -1.683333), "Pau": (43.3, -0.366667)
        }

    def GetMax(self):
        """ Get min and max value of position (for display)
        """
        start = True
        maxX = 0
        maxY = 0
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

    def __len__(self):
        return len(self._cities)

    @property
    def Start(self):
        return self._start

    @property
    def End(self):
        return self._end.Value

    def GetNext(self, prev):
        """ Return children nodes
        :param prev: previous node
        :return: Children
        """
        next = []
        prev_pos = self._cities[prev.Value]
        for name, position in self._cities.items():
            if name != prev.Value:
                next.append(SearchNode(name, self._distance(prev_pos, position)))

        return next

    def _distance(self, pos1, pos2):
        """
        Haversine distance
        :param pos1: tuple of (x, y) position
        :param pos2: tuple of (x, y) position
        :return: distance
        """
        p = pi / 180
        a = 0.5 - cos((pos2[0] - pos1[0]) * p) / 2 + cos(pos1[0] * p) * cos(pos2[0] * p) * (
                    1 - cos((pos2[1] - pos1[1]) * p)) / 2
        R = 6371
        return 2 * R * asin(sqrt(a))

    def isEnd(self, node):
        return node == self._end
