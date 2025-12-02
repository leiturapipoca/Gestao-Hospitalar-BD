from tkinter import messagebox, END
from View.TelaEntradas import TelaEntradas
from Model.EntradaDAO import EntradaDAO
import Model.HospitalDAO as HospitalDAO 
from Controller.ProcedimentosController import ProcedimentosController

class EntradasController:
    def __init__(self, root, usuario):
        self.dao = EntradaDAO()
        self.usuario = usuario 
        self.cnes_vinculado = None 
        
        salas_disponiveis = self.preparar_dados_hospital()
        self.view = TelaEntradas(root, salas_disponiveis)
        
        if self.cnes_vinculado:
            nome_hosp = HospitalDAO.get_name_by_cnes(self.cnes_vinculado, self.dao.connection)
            texto = nome_hosp if nome_hosp else self.cnes_vinculado
            self.view.preencher_cnes(texto)

        self.view.set_action_salvar(self.salvar_e_avancar)
        self.view.set_action_voltar(self.voltar)

    def preparar_dados_hospital(self):
        if not isinstance(self.usuario, dict): return ()
        matricula = self.usuario.get('matricula')
        if not matricula: return ()
        
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.dao.connection)
        
        if cnes:
            self.cnes_vinculado = cnes
            return HospitalDAO.get_salas_livres_by_cnes(cnes, self.dao.connection)
        return ()

    def salvar_e_avancar(self):
        cpf = self.view.get_cpf()
        cnes_salvar = self.cnes_vinculado
        desc = self.view.get_description()
        sala_str = self.view.get_sala()

        if not cpf or not cnes_salvar or not sala_str:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            numero_sala = int(sala_str.replace("Sala ", "").strip())
        except:
            messagebox.showerror("Erro", "Sala inválida.")
            return

        id_entrada = self.dao.registrar_entrada(cpf, cnes_salvar, desc)

        if id_entrada:
            self.view.frm.destroy()
            
            # Cria novo procedimento
            ProcedimentosController(
                self.view.janela, 
                self.usuario, 
                id_entrada, 
                numero_sala, 
                cnes_salvar 
            )
        else:
            messagebox.showerror("Erro", "Falha ao registrar entrada.")

    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.view.janela, self.usuario)