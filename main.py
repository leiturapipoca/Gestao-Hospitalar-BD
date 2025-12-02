from tkinter import *
from tkinter import ttk
from Controller.LoginController import LoginController
from Controller.InternosController import InternosController
from Controller.ExternosController import ExternosController
from Controller.GerenciarFuncsController import GerenciarFuncsController
from Controller.PacientesController import PacientesController
from Model import HospitalDAO
from Model import FuncaoDAO
from SQL import databaseUtils

test_hosp_model = False
test_funcao_model = True
specific_view_test = 'login'

if __name__ == "__main__":
    if test_hosp_model: HospitalDAO.run_hosp_model_tests()
    if test_funcao_model: FuncaoDAO.run_funcao_dao_tests()

    root = Tk()

    if specific_view_test == 'login': app = LoginController(root)
    elif specific_view_test == 'acesso_interno': app = InternosController(root, {'nome': 'batata'})
    elif specific_view_test == 'acesso_externo': app = ExternosController(root)
    elif specific_view_test == 'gerenciar_funcs': app = GerenciarFuncsController(root)
    elif specific_view_test == 'paciente': app = PacientesController(root, [])
    

    root.mainloop()
