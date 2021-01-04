#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "Class for ACO algorithm"
__version__ = "1.0"


class SearchNode:
    def __init__(self, v, d):
        self._value = v
        self._distance = d

    @property
    def Value(self):
        return self._value

    @property
    def Distance(self):
        return self._distance

    def __hash__(self):
        return hash(self._value)

    def __eq__(self, n2):
        if n2 is None:
            return False

        return n2.Value == self._value

    def __ne__(self, n2):
        return not n2 == self

    def __str__(self):
        return f"{self._value}"

    def __repr__(self):
        return f"{self._value}"
