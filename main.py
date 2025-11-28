from tkinter import *
from tkinter import ttk
from Controller.LoginController import LoginController

if __name__ == "__main__":
    root = Tk()
    
    app = LoginController(root)

    root.mainloop()
