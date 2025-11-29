from tkinter import *
from View.TelaGerenciarFuncs import TelaGerenciarFuncs
from View.TelaAdicionarFunc import TelaAdicionarFunc
from View.TelaConsultarFunc import TelaConsultarFunc
from View.TelaRemoverFunc import TelaRemoverFunc
import logging

test_logger = logging.getLogger("GerenciarFuncsController")

class GerenciarFuncsController:
    def __init__(self, root: Tk):
        self.root = root
        self.view: TelaGerenciarFuncs | TelaConsultarFunc | TelaAdicionarFunc | TelaRemoverFunc = TelaGerenciarFuncs(root)
        self.config_tela_gerenciar_funcs_callbacks(self.view)

    def config_tela_gerenciar_funcs_callbacks(self, view: TelaGerenciarFuncs):
        view.set_action_adicionar_func(self.select_adicionar_func)
        view.set_action_remover_func(self.select_remover_func)
        view.set_action_consultar_func(self.select_consultar_func)
        view.set_action_voltar(self.voltar)


    def select_adicionar_func(self):
        logging.info("usuário selecionou: adicionar funcionário")
        self.view.frm.destroy()
        self.view = TelaAdicionarFunc(self.root)

    def select_remover_func(self):
        logging.info("usuário selecionou: remover funcionário")
        self.view.frm.destroy()
        self.view = TelaRemoverFunc(self.root)

    def select_consultar_func(self):
        logging.info("usuário selecionou: consultar funcionário")
        self.view.frm.destroy()
        self.view = TelaConsultarFunc(self.root)


    def voltar(self):
        logging.info("usuário selecionou: voltar")
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.root, {"nome": "batata"}) # TODO: usar valores de verdade
        pass
