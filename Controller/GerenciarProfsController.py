from tkinter import *
from View.TelaGerenciarProfs import TelaGerenciarProfs
from View.TelaAdicionarProf import TelaAdicionarProf
from View.TelaConsultarProf import TelaConsultarProf
from View.TelaRemoverProf import TelaRemoverProf
import logging

test_logger = logging.getLogger("GerenciarProfsController")

class GerenciarProfsController:
    def __init__(self, root: Tk, dados_usuario: dict):
        self.root = root
        self.dados_usuario = dados_usuario
        self.view: TelaGerenciarProfs | TelaConsultarProf | TelaAdicionarProf | TelaRemoverProf = TelaGerenciarProfs(root)
        self.config_tela_gerenciar_profs_callbacks(self.view)

    def config_tela_gerenciar_profs_callbacks(self, view: TelaGerenciarProfs):
        view.set_action_adicionar_prof(self.select_adicionar_prof)
        view.set_action_remover_prof(self.select_remover_prof)
        view.set_action_consultar_prof(self.select_consultar_prof)
        view.set_action_voltar(self.voltar)

    def select_adicionar_prof(self):
        logging.info("usuário selecionou: adicionar profissional de saúde")
        self.view.frm.destroy()
        self.view = TelaAdicionarProf(self.root)
        self.view.set_action_adicionar(self.handle_adicionar_prof)
        self.view.set_action_voltar(self.voltar_to_menu)

    def select_remover_prof(self):
        logging.info("usuário selecionou: remover profissional de saúde")
        self.view.frm.destroy()
        self.view = TelaRemoverProf(self.root)
        self.view.set_action_remover(self.handle_remover_prof)
        self.view.set_action_voltar(self.voltar_to_menu)

    def select_consultar_prof(self):
        logging.info("usuário selecionou: consultar profissional de saúde")
        self.view.frm.destroy()
        self.view = TelaConsultarProf(self.root)
        self.view.set_action_consultar(self.handle_consultar_prof)
        self.view.set_action_voltar(self.voltar_to_menu)

    def voltar(self):
        logging.info("usuário selecionou: voltar")
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.root, self.dados_usuario)

    def voltar_to_menu(self):
        """Navigate back to the main professional management menu"""
        logging.info("usuário selecionou: voltar ao menu de gerenciamento")
        self.view.frm.destroy()
        self.view = TelaGerenciarProfs(self.root)
        self.config_tela_gerenciar_profs_callbacks(self.view)

    def handle_adicionar_prof(self):
        """Placeholder handler for adding a professional - logs action and displays success message"""
        form_data = self.view.get_form_data()
        
        logging.info(f"Ação: adicionar profissional de saúde - CPF: {form_data.get('cpf')}, "
                    f"Nome: {form_data.get('nome')}, Tipo: {form_data.get('tipo')}, "
                    f"CRM: {form_data.get('crm', 'N/A')}, CODIGO: {form_data.get('codigo', 'N/A')}")
        
        # Display placeholder success message
        self.view.show_success_message("Profissional adicionado com sucesso! (placeholder)")
        self.view.clear_form()

    def handle_remover_prof(self):
        """Placeholder handler for removing a professional - logs action and displays success message"""
        cpf = self.view.get_cpf()
        
        logging.info(f"Ação: remover profissional de saúde - CPF: {cpf}")
        
        # Display placeholder success message
        self.view.show_success_message(f"Profissional com CPF {cpf} removido com sucesso! (placeholder)")
        self.view.clear_form()

    def handle_consultar_prof(self):
        """Placeholder handler for querying a professional - logs action and displays placeholder results"""
        cpf = self.view.get_cpf()
        
        logging.info(f"Ação: consultar profissional de saúde - CPF: {cpf}")
        
        # Display placeholder results
        placeholder_data = {
            'nome': 'João da Silva (placeholder)',
            'tipo': 'M',
            'crm': '123456789'
        }
        
        self.view.display_results(placeholder_data)
