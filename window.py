#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Gabriel Nativel-Fontaine"
__date__ = "21-01-04"
__usage__ = "Class for TKinter window"
__version__ = "1.0"

from tkinter import *

from src.AntColony import ACO


class Window(Tk):
    """ Main Tk window
    """
    def __init__(self, width, height, problem):
        Tk.__init__(self)
        self.title("Ant Colony Optimization")

        self.problem = problem

        # set size
        self.width, self.height = width, height
        self.geometry("{0}x{1}".format(width + 300, height))

        # set window position
        self.positionX = int(self.winfo_screenwidth() / 2 - (self.width + 300) / 2)
        self.positionY = int(self.winfo_screenheight() / 2 - self.height / 2)
        self.geometry("+{}+{}".format(self.positionX, self.positionY))

        # Building main window
        self.canvas = Canvas(self, width=self.width, height=self.height, bg='black', bd=0, highlightthickness=0)

        self.menu = Frame(self, width=300, height=self.height)

        # Building menu
        self._foodTitle = Label(self.menu, text='Paramètres', anchor=W, justify=CENTER, font=("Helvetica", 13, 'bold'))

        self._frame1 = Frame(self.menu)

        self.alpha = IntVar()
        self._scale1 = Scale(self._frame1, orient='horizontal', from_=1, to=20, resolution=1, tickinterval=2,
                             label='Alpha', length=240, variable=self.alpha)
        self._scale1.set(1)

        self.beta = IntVar()
        self._scale2 = Scale(self._frame1, orient='horizontal', from_=1, to=20, resolution=1, tickinterval=2,
                             label='Beta', length=240, variable=self.beta)
        self._scale2.set(1)

        self.gamma = DoubleVar()
        self._scale3 = Scale(self._frame1, orient='horizontal', from_=1, to=1000, resolution=1, tickinterval=200,
                             label='Gamma', length=240, variable=self.gamma)
        self._scale3.set(1)

        self.Q = DoubleVar()
        self._scale5 = Scale(self._frame1, orient='horizontal', from_=0, to=1000, resolution=1, tickinterval=200,
                             label='Q', length=240, variable=self.Q)
        self._scale5.set(1)

        self.rho = DoubleVar()
        self._scale4 = Scale(self._frame1, orient='horizontal', from_=0, to=1, resolution=0.01, tickinterval=1,
                             label='Rho', length=240, variable=self.rho)
        self._scale4.set(0.45)

        self.ants = IntVar()
        self._scale6 = Scale(self._frame1, orient='horizontal', from_=0, to=1000, resolution=1, tickinterval=200,
                             label='Nb Ants', length=240, variable=self.ants)
        self._scale6.set(50)

        self._btnStart = Button(self._frame1, text="Start", command=self._toggleSimulation, width=7, height=2)
        self._btnStop = Button(self._frame1, text="Stop", command=self._stopSimulation, width=7, height=2)

        self.lines = {}
        self.labelEpochs = None

        self.colony = None

        self.pause = False

        self._setupInterface()
        self._drawCities()

        self.tick = 0

        self.mainloop()

    def rgb(self, r, g, b):
        """ Convert RGB to hexadecimal for tkinter
        :return: hexadecimal string
        """
        return f'#{r:02x}{g:02x}{b:02x}'

    def _drawCities(self):
        """ Draw points for each node's position in the problem
        """
        maxX, maxY, minX, minY = self.problem.GetMax()

        self.lines = {}
        cities = []
        labels = []

        self.labelEpochs = self.canvas.create_text(20, 20, fill="white", font="Times 20 italic bold", text='0')

        for c1, position_c1 in self.problem._cities.items():
            x = (position_c1[0] - minX) * (self.width - 15) / maxX + 15
            y = (position_c1[1] - minY) * (self.height - 15) / maxY + 15

            a = self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.rgb(255, 0, 0))
            l = self.canvas.create_text(x + 6, y - 6, fill="white", font="Times 10 italic bold", text=c1)
            cities.append(a)
            labels.append(l)

            self.lines[c1] = {}

        for name_c1, position_c1 in self.problem._cities.items():
            for name_c2, position_c2 in self.problem._cities.items():
                if name_c2 not in self.lines[name_c1] and name_c2 != name_c1:
                    x1 = (position_c1[0] - minX) * (self.width - 15) / maxX + 15
                    y1 = (position_c1[1] - minY) * (self.height - 15) / maxY + 15
                    x2 = (position_c2[0] - minX) * (self.width - 15) / maxX + 15
                    y2 = (position_c2[1] - minY) * (self.height - 15) / maxY + 15
                    line = self.canvas.create_line(x1, y1, x2, y2, fill=self.rgb(0, 0, 0))
                    self.lines[name_c1][name_c2] = line

                    x1 = x1 + 4
                    y1 += 4
                    x2 = x2 + 4
                    y2 += 4
                    line = self.canvas.create_line(x1, y1, x2, y2, fill=self.rgb(0, 0, 0))
                    self.lines[name_c2][name_c1] = line

        for i in range(len(cities)):
            self.canvas.tag_raise(cities[i])
            self.canvas.tag_raise(labels[i])

    def _toggleSimulation(self):
        """ Used to start/pause/stop the simulation when button is clicked
        """
        if self._btnStart['text'] == 'Start':
            if self.pause:
                self._loopSimulation()
            else:
                self._startSimulation()
                self._btnStop.pack()
            self._btnStart['text'] = 'Pause'
        else:
            self._btnStart['text'] = 'Start'
            print('Pause set')
            self.pause = True
            self.canvas.after_cancel(self._loop)

    def _stopSimulation(self):
        """ Used to stop the simulation when stop button is clicked
        """
        self._btnStop.pack_forget()
        if self._btnStart['text'] != 'Start':
            self._btnStart['text'] = 'Start'

        self.pause = False
        self.canvas.after_cancel(self._loop)

    def _startSimulation(self):
        """ Initialize the simulation
        """
        self.colony = ACO(self.problem, alpha=self.alpha.get(), beta=self.beta.get(), gamma=self.gamma.get(),
                          Q=self.Q.get(), rho=self.rho.get(), nbAnts=self.ants.get(), epochs=10)

        print(f'Starting... {self.colony}')

        self._loopSimulation()

    def _loopSimulation(self):
        """ Loop over the simulation
        """
        self._tickSimulation()
        self._loop = self.canvas.after(100, self._loopSimulation)

    def _tickSimulation(self):
        """ Run one tick of the simulation
        """
        self.tick += 1
        self.canvas.itemconfig(self.labelEpochs, text=self.tick)
        self.colony.simulate()
        self._updateDisplay()

    def _updateDisplay(self):
        """ Update display according simulation elements
        """
        for c1 in self.problem._cities.keys():
            for c2 in self.problem._cities.keys():
                if c1 != c2:
                    self.canvas.itemconfig(self.lines[c1][c2], fill=self.rgb(0, 0, 0))

                    if c1 not in self.colony._pheromons or (c1 in self.colony._pheromons and c2 not in self.colony._pheromons[c1]):
                        value = 0
                    else:
                        value = int(self.colony._pheromons[c1][c2] * 255 / self.colony.Maximum)
                        self.canvas.tag_raise(self.lines[c1][c2])
                        self.canvas.itemconfig(self.lines[c1][c2], fill=self.rgb(value, 0, 0))

    def _step(self):
        self._tickSimulation()

    def _setupInterface(self):
        """ Pack all the element in the Tk window
        """
        self.canvas.pack(side=LEFT)
        self.menu.pack(side=TOP)

        self._foodTitle.pack()
        self._frame1.pack()
        self._scale1.pack()
        self._scale2.pack()
        self._scale3.pack()
        self._scale4.pack()
        self._scale5.pack()
        self._scale6.pack()
        self._btnStart.pack()
