from tkinter import *
from tkinter import ttk
from Controller.LoginController import LoginController
from Controller.InternosController import InternosController
from Controller.ExternosController import ExternosController
from Model import HospitalDAO
from SQL import databaseUtils

test_hosp_model = False
specific_view_test = 'acesso_interno'

if __name__ == "__main__":
    if test_hosp_model: HospitalDAO.run_hosp_model_tests()

    root = Tk()

    if specific_view_test == 'login': app = LoginController(root)
    elif specific_view_test == 'acesso_interno': app = InternosController(root, {'nome': 'batata'})
    elif specific_view_test == 'acesso_externo': app = ExternosController(root)
    

    root.mainloop()
