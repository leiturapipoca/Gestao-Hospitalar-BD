from tkinter import *
from View.TelaGerenciarFuncs import TelaGerenciarFuncs
from View.TelaAdicionarFunc import TelaAdicionarFunc
from View.TelaConsultarFunc import TelaConsultarFunc
from View.TelaRemoverFunc import TelaRemoverFunc
from Model.FuncaoDAO import FuncaoDao
from Model.FuncionarioDAO import FuncionarioDAO
import logging

test_logger = logging.getLogger("GerenciarFuncsController")

class GerenciarFuncsController:
    def __init__(self, root: Tk):
        self.root = root
        self.funcao_dao: FuncaoDao = FuncaoDao()
        self.funcionario_dao: FuncionarioDAO = FuncionarioDAO()
        self.view: TelaGerenciarFuncs | TelaConsultarFunc | TelaAdicionarFunc | TelaRemoverFunc = TelaGerenciarFuncs(root)
        self.config_tela_gerenciar_funcs_callbacks(self.view)

    def config_tela_gerenciar_funcs_callbacks(self, view: TelaGerenciarFuncs):
        view.set_action_adicionar_func(self.select_adicionar_func)
        view.set_action_remover_func(self.select_remover_func)
        view.set_action_consultar_func(self.select_consultar_func)
        view.set_action_voltar(self.voltar)

    def config_tela_adicionar_funcs(self, view: TelaAdicionarFunc):
        view.set_confirm_action(self.adicionar_func)
        view.set_return_action(self.voltar)


    def config_tela_remover_funcs(self, view: TelaRemoverFunc):
        view.set_return_action(self.voltar)


    def select_adicionar_func(self):
        logging.info("usuário selecionou: adicionar funcionário")
        self.view.frm.destroy()
        funcoes = tuple(self.funcao_dao.get_all_funcoes())
        self.view = TelaAdicionarFunc(self.root, funcoes)
        self.config_tela_adicionar_funcs(self.view)


    def select_gerenciar_func(self):
        logging.info("entrou-se na tela gerenciar func")
        self.view.frm.destroy()
        self.view = TelaGerenciarFuncs(self.root)
        self.config_tela_gerenciar_funcs_callbacks(self.view)


    def adicionar_func(self):
        if not isinstance(self.view, TelaAdicionarFunc):
            logging.warning("botão de adicionar func foi pressionado sem que se estivesse na TelaAdicionarFunc")
            self.select_gerenciar_func()
        else:
            new_func_name = self.view.get_name_field()
            new_func_cargo = self.view.get_func_field()
            cargo_id = int(new_func_cargo.split(' ')[0])
            logging.info(f"novo funcionário Nome: {new_func_name} Cargo: {new_func_cargo} Cargo ID: {cargo_id}")
            try:
                self.funcionario_dao.add_funcionario(new_func_name, cargo_id)
                self.voltar()
            except Exception as e:
                logging.error("erro na query de adicionar funcionário")
                raise e

        pass

    def select_remover_func(self):
        logging.info("usuário selecionou: remover funcionário")
        self.view.frm.destroy()
        self.view = TelaRemoverFunc(self.root)
        self.config_tela_remover_funcs(self.view)

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
