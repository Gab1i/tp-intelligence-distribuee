#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "Class for ACO"
__version__ = "1.0"


class Ant:
    """ Class used to old Ants path in ACO algorithm
    """
    def __init__(self, start, Q):
        self._path = [start]
        self._current = start
        self._deltaPhero = 0
        self._q = Q

    @property
    def Path(self):
        return self._path

    @property
    def CurrentCity(self):
        return self._current

    @property
    def PathLen(self):
        return len(self._path)

    @property
    def Pheromons(self):
        return self._q / len(self._path)

    def Go(self, city):
        self._path.append(city)
        self._current = city

    def Seen(self, city):
        return city in self._path
