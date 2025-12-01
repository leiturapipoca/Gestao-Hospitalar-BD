from tkinter import *
from View.TelaGerenciarProfs import TelaGerenciarProfs
from View.TelaAdicionarProf import TelaAdicionarProf
from View.TelaConsultarProf import TelaConsultarProf
from View.TelaRemoverProf import TelaRemoverProf
from Model.ProfissionalDAO import ProfissionalDAO
import logging

test_logger = logging.getLogger("GerenciarProfsController")

class GerenciarProfsController:
    def __init__(self, root: Tk, dados_usuario: dict):
        self.root = root
        self.dados_usuario = dados_usuario
        self.dao = ProfissionalDAO()
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
        """Handler for adding a professional - validates form data and calls DAO"""
        try:
            form_data = self.view.get_form_data()
            
            cpf = form_data.get('cpf', '').strip()
            nome = form_data.get('nome', '').strip()
            tipo = form_data.get('tipo', '').strip()
            crm = form_data.get('crm', '').strip() if 'crm' in form_data else None
            codigo = form_data.get('codigo', '').strip() if 'codigo' in form_data else None
            
            logging.info(f"Ação: adicionar profissional de saúde - CPF: {cpf}, "
                        f"Nome: {nome}, Tipo: {tipo}, "
                        f"CRM: {crm if crm else 'N/A'}, CODIGO: {codigo if codigo else 'N/A'}")
            
            # Validate form data
            if not cpf or len(cpf) != 11:
                self.view.show_error_message("Erro: CPF deve ter exatamente 11 caracteres.")
                return
            
            if not nome:
                self.view.show_error_message("Erro: Nome não pode estar vazio.")
                return
            
            if tipo not in ['M', 'E']:
                self.view.show_error_message("Erro: Tipo deve ser 'M' (Médico) ou 'E' (Enfermeiro).")
                return
            
            if tipo == 'M':
                if not crm or len(crm) != 9:
                    self.view.show_error_message("Erro: CRM deve ter exatamente 9 caracteres para médicos.")
                    return
            elif tipo == 'E':
                # CODIGO is optional for nurses (auto-generated), but if provided, validate it
                if codigo and not codigo.isdigit():
                    self.view.show_error_message("Erro: CODIGO deve ser um número válido.")
                    return
                # Convert to int if provided, otherwise None
                codigo = int(codigo) if codigo else None
            
            # Call DAO to add professional
            success, message = self.dao.add_profissional(cpf, nome, tipo, crm, codigo)
            
            if success:
                self.view.show_success_message(message)
                self.view.clear_form()
            else:
                self.view.show_error_message(message)
                
        except Exception as e:
            logging.error(f"Erro ao adicionar profissional: {e}")
            self.view.show_error_message(f"Erro inesperado: {str(e)}")

    def handle_remover_prof(self):
        """Handler for removing a professional - validates CPF and calls DAO"""
        try:
            cpf = self.view.get_cpf().strip()
            
            logging.info(f"Ação: remover profissional de saúde - CPF: {cpf}")
            
            # Validate CPF
            if not cpf or len(cpf) != 11:
                self.view.show_error_message("Erro: CPF deve ter exatamente 11 caracteres.")
                return
            
            # Call DAO to remove professional
            success, message = self.dao.remove_profissional(cpf)
            
            if success:
                self.view.show_success_message(message)
                self.view.clear_form()
            else:
                self.view.show_error_message(message)
                
        except Exception as e:
            logging.error(f"Erro ao remover profissional: {e}")
            self.view.show_error_message(f"Erro inesperado: {str(e)}")

    def handle_consultar_prof(self):
        """Handler for querying a professional - validates CPF and calls DAO"""
        try:
            cpf = self.view.get_cpf().strip()
            
            logging.info(f"Ação: consultar profissional de saúde - CPF: {cpf}")
            
            # Validate CPF
            if not cpf or len(cpf) != 11:
                self.view.show_error_message("Erro: CPF deve ter exatamente 11 caracteres.")
                return
            
            # Call DAO to query professional
            professional_data = self.dao.consultar_profissional(cpf)
            
            if professional_data:
                self.view.display_results(professional_data)
            else:
                self.view.show_error_message(f"Profissional com CPF {cpf} não encontrado.")
                
        except Exception as e:
            logging.error(f"Erro ao consultar profissional: {e}")
            self.view.show_error_message(f"Erro inesperado: {str(e)}")
