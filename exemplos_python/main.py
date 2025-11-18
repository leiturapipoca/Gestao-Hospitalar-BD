from tkinter import *
from tkinter import ttk

if __name__ == "__main__":
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Login:").grid(column=1, row=0)
    ttk.Label(frm, text="Nome: ").grid(column=0, row=1)
    ttk.Entry(frm).grid(column=1, row=1)
    ttk.Label(frm, text="Senha: ").grid(column=0, row=2)
    ttk.Entry(frm, show="*").grid(column=1, row=2)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=4)
    root.mainloop()
