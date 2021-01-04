#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "ACO algorithm"
__version__ = "1.0"

from src.Ant import Ant

import numpy as np


class ACO:
    """ Compute Ant Colony Optimization
    """
    def __init__(self, problem, alpha, beta, gamma, Q, rho, nbAnts, epochs):
        self.problem = problem
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._Q = Q
        self._rho = rho

        self._nbAnts = nbAnts
        self._epochs = epochs

        self._pheromons = {}
        self._maximum = 0

    def __str__(self):
        return f'ACO ({self._nbAnts} ants) | alpha={self._alpha}, beta={self._beta}, gamma={self._gamma}, Q={self._Q}, rho={self._rho}'

    @property
    def Maximum(self):
        return self._maximum

    def simulate(self):
        """ Run one step
        """
        self._maximum = 0
        ants = []

        for _ in range(self._nbAnts):
            ant = Ant(self.problem.Start, self._Q)

            for i in range(len(self.problem)):
                # add to the dict if node never seen
                if ant.CurrentCity.Value not in self._pheromons:
                    self._pheromons[ant.CurrentCity.Value] = {}

                # get next stops
                next = self.problem.GetNext(ant.CurrentCity)
                probs = []
                next_not_seen = []
                for nextStop in next:
                    if not ant.Seen(nextStop) and nextStop.Value in self._pheromons[ant.CurrentCity.Value]:
                        tau = self._pheromons[ant.CurrentCity.Value][nextStop.Value]
                    else:
                        tau = 0

                    eta = 1 / nextStop.Distance
                    probs.append(self._gamma + tau**self._alpha * eta**self._beta)
                    next_not_seen.append(nextStop)

                probs = np.array(probs) / sum(probs)

                if len(next_not_seen) > 0:
                    choice = np.random.choice(next_not_seen, p=probs)
                    ant.Go(choice)

                ants.append(ant)

        #
        for c1, val1 in self._pheromons.items():
            for c2, val2 in self._pheromons[c1].items():
                if c1 != c2:
                    self._pheromons[c1][c2] = (1 - self._rho) * self._pheromons[c1][c2]

        # deposit pheromons
        for a in ants:
            for i in range(a.PathLen - 1):
                c1 = a.Path[i].Value
                c2 = a.Path[i+1].Value
                if c1 in self._pheromons:
                    if c2 in self._pheromons[c1]:
                        self._pheromons[c1][c2] += a.Pheromons
                    else:
                        self._pheromons[c1][c2] = a.Pheromons
                else:
                    self._pheromons[c1] = {}
                    self._pheromons[c1][c2] = a.Pheromons

                if self._pheromons[c1][c2] > self._maximum:
                    self._maximum = self._pheromons[c1][c2]
