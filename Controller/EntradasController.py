from tkinter import messagebox, END
from View.TelaEntradas import TelaEntradas
from Model.EntradaDAO import EntradaDAO
import Model.HospitalDAO as HospitalDAO 
from Controller.ProcedimentosController import ProcedimentosController

class EntradasController:
    def __init__(self, root, usuario):
        self.view = TelaEntradas(root)
        self.dao = EntradaDAO()
        self.usuario = usuario # Dicionário {'matricula': X, 'nome': Y}
        self.cnes_vinculado = None 
        
        self.preencher_hospital_automatico()

        self.view.set_action_salvar(self.salvar_registro)
        self.view.set_action_voltar(self.voltar)

    def preencher_hospital_automatico(self):
        matricula = self.usuario.get('matricula')
        
        if not matricula:
            messagebox.showerror("Erro", "Erro nos dados do usuário logado.")
            return

        # Busca o CNES
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.dao.connection)
        
        if cnes:
            self.cnes_vinculado = cnes
            # Busca o Nome do Hospital para mostrar bonito
            nome_hosp = HospitalDAO.get_name_by_cnes(cnes, self.dao.connection)
            texto = nome_hosp if nome_hosp else cnes
            
            self.view.preencher_cnes(texto)
        else:
            messagebox.showwarning("Aviso", "Funcionário sem vínculo hospitalar.")

    def salvar_registro(self):
        cpf = self.view.get_cpf()
        cnes_salvar = self.cnes_vinculado

        if not cpf or not cnes_salvar:
            messagebox.showwarning("Aviso", "Preencha o CPF e verifique o hospital!")
            return
        
        # Chama o DAO (Método INSERT normal)
        sucesso = self.dao.register_entry(cpf, cnes_salvar)

        if sucesso:
            messagebox.showinfo("Sucesso", "Entrada registrada!")
            self.view.campo_cpf.delete(0, END)

            self.view.frm.destroy()
            ProcedimentosController(self.view.janela)
            
        else:
            messagebox.showerror("Erro", "Falha ao registrar. Verifique se o CPF existe.")


    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        # Devolve o dicionário para não perder os dados
        InternosController(self.view.janela, self.usuario)
