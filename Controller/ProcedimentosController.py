from View.TelaProcedimentos import TelaProcedimentos
from tkinter import *
from tkinter import ttk

class ProcedimentosController:
    def __init__(self,root: Tk):
        self.view = TelaProcedimentos(root)
        
