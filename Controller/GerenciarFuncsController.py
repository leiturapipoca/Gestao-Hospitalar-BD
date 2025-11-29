from tkinter import *
from View.TelaGerenciarFuncs import TelaGerenciarFuncs

class GerenciarFuncsController:
    def __init__(self, root: Tk):
        self.view = TelaGerenciarFuncs(root)
