from tkinter import messagebox, END
from View.TelaEntradas import TelaEntradas
from Model.EntradaDAO import EntradaDAO
import Model.HospitalDAO as HospitalDAO 
import logging
from Controller.ProcedimentosController import ProcedimentosController

class EntradasController:
    def __init__(self, root, usuario):
        self.dao = EntradaDAO()
        self.usuario = usuario 
        self.cnes_vinculado = None 
        
        # 1. BUSCA AS SALAS ANTES DE CRIAR A TELA
        salas_disponiveis = self.preparar_dados_hospital()

        # 2. PASSA A LISTA DE SALAS PARA A TELA
        self.view = TelaEntradas(root, salas_disponiveis)
        
        # 3. PREENCHE O NOME DO HOSPITAL
        if self.cnes_vinculado:
            nome_hosp = HospitalDAO.get_name_by_cnes(self.cnes_vinculado, self.dao.connection)
            texto = nome_hosp if nome_hosp else self.cnes_vinculado
            self.view.preencher_cnes(texto)

        self.view.set_action_salvar(self.salvar_e_avancar)
        self.view.set_action_voltar(self.voltar)

    def preparar_dados_hospital(self):
        if not isinstance(self.usuario, dict): return ()
        matricula = self.usuario.get('matricula')
        
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.dao.connection)
        
        if cnes:
            self.cnes_vinculado = cnes
            # Busca salas livres
            return HospitalDAO.get_salas_livres_by_cnes(cnes, self.dao.connection)
        else:
            messagebox.showwarning("Aviso", "Funcionário sem vínculo hospitalar.")
            return ()

    def salvar_e_avancar(self):
        logging.info("De fato entrou em salva_e_avancar")
        cpf = self.view.get_cpf()
        cnes_salvar = self.cnes_vinculado
        desc = self.view.get_description()
        sala_str = self.view.get_sala() # "Sala 101"

        if not cpf or not cnes_salvar or not sala_str:
            messagebox.showwarning("Aviso", "Preencha CPF e Sala!")
            return
        
        try:
            # Extrai número da sala: "Sala 101" -> 101
            numero_sala = int(sala_str.replace("Sala ", ""))
        except:
            messagebox.showerror("Erro", "Sala inválida.")
            return

        

        try:
            logging.info("Entrou no try")
            id_entrada = self.dao.registrar_entrada(cpf, cnes_salvar, desc)
            logging.info(f"{id_entrada} eh o id de entrada")
            self.view.frm.destroy()
            # Passa o numero_sala para o próximo controller
            ProcedimentosController(self.view.janela, self.usuario, id_entrada, numero_sala)
        except:
            messagebox.showerror("Erro", "Falha ao registrar.")

    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.view.janela, self.usuario)