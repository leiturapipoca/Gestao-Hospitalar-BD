from tkinter import *
from tkinter import messagebox
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
        view.set_confirm_action(self.remover_func)

    def config_tela_consultar_funcs(self, view: TelaConsultarFunc):
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
        # 1. Pega os dados da View
        if not isinstance(self.view, TelaAdicionarFunc):
            logging.warning("botão de remover func foi pressionado sem que se estivesse na TelaRemoverFunc")
            self.select_gerenciar_func()
        else:
            new_func_name = self.view.get_name_field()
            new_func_cpf = self.view.get_cpf_field()
            new_func_pass = self.view.get_func_pass()
        
            # Pega o valor do Combobox (Ex: "3 Diretor" ou "3 - Diretor")
            cargo_bruto = self.view.get_func_field() 

            # Validação simples
            if not new_func_name or not new_func_cpf or not new_func_pass or not cargo_bruto:
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
                return

            # --- CORREÇÃO DO ERRO DE SINTAXE ---
            try:
                # Pega apenas a primeira parte da string (o número)
                # Ex: "3 Diretor".split() -> ['3', 'Diretor'] -> Pega o '3' -> Converte para int
                cargo_id = int(cargo_bruto.split()[0])
            except (IndexError, ValueError):
                messagebox.showerror("Erro", "Formato de cargo inválido. Selecione uma opção válida.")
                return

        # 2. Chama o DAO passando o ID limpo
        # Note que o DAO retorna DOIS valores agora (sucesso, mensagem)
        sucesso, mensagem = self.funcionario_dao.add_funcionario(new_func_name, new_func_cpf, cargo_id, new_func_pass)

        # 3. Mostra o resultado na tela
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            # Limpar campos se quiser
            
        else:
            messagebox.showerror("Erro de Cadastro", mensagem)


    def select_remover_func(self):
        logging.info("usuário selecionou: remover funcionário")
        self.view.frm.destroy()
        self.view = TelaRemoverFunc(self.root)
        self.config_tela_remover_funcs(self.view)


    def remover_func(self):
        logging.info("usuário apertou botão de remover funcionário")
        if not isinstance(self.view, TelaRemoverFunc):
            logging.warning("botão de remover func foi pressionado sem que se estivesse na TelaRemoverFunc")
            self.select_gerenciar_func()
        else:
            func_cpf = self.view.get_cpf_field()
            logging.info(f"cpf do funcionário a ser removido: {func_cpf}")
            self.funcionario_dao.remove_funcionario(func_cpf)


    def select_consultar_func(self):
        logging.info("usuário selecionou: consultar funcionário")
        self.view.frm.destroy()
        self.view = TelaConsultarFunc(self.root, "nome maluco", "12341234", "função legal", "13412341234", ["hosp1", "hosp2", "hosp3", "hosp4"])
        self.config_tela_consultar_funcs(self.view)


    def voltar(self):
        logging.info("usuário selecionou: voltar")
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.root, {"nome": "batata"}) # TODO: usar valores de verdade
        pass
