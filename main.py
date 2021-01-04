import sys
from tkinter import messagebox, Tk

from src.CityProblem import CityProblem
from src.XYProblem import XYProblem
from window import Window

if __name__ == "__main__":
    ListenN = False
    N = 10
    problem = XYProblem(N, 0)

    for arg in sys.argv:
        if ListenN:
            try:
                N = int(arg)
            except ValueError:
                N = 10
            ListenN = False
        if arg == '-n':
            ListenN = True
        if arg == '-cities':
            problem = CityProblem('Bordeaux')

    try:
        splash = Window(700, 600, problem)
    except:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Erreur inconnue",
                             "Ooops il semble qu'un problème soit survenu ! Le programme va être fermé.")
