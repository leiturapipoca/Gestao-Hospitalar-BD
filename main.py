from tkinter import *
from tkinter import ttk
from Controller.LoginController import LoginController
from Model import HospitalDAO
from SQL import databaseUtils

test_hosp_model = True

if __name__ == "__main__":
    if test_hosp_model: HospitalDAO.run_hosp_model_tests()

    root = Tk()
    
    app = LoginController(root)

    root.mainloop()
