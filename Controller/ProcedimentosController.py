from tkinter import messagebox
from View.TelaProcedimentos import TelaProcedimentos
from Model.ProcedimentosDAO import ProcedimentosDAO

class ProcedimentosController:
    # O __init__ tem que aceitar o 'numero_sala' opcional
    def __init__(self, root, usuario, id_entrada, numero_sala=None):
        self.usuario = usuario
        self.id_entrada = id_entrada 
        self.numero_sala = numero_sala
        
        self.dao = ProcedimentosDAO()
        
        # Carrega lista do banco
        lista_tipos = self.dao.get_tipos_procedimento()
        
        # Cria a View
        self.view = TelaProcedimentos(root, lista_tipos)
        
        # Se veio uma sala da tela anterior, preenche
        if self.numero_sala:
            # Verifica se a view tem o método antes de chamar
            if hasattr(self.view, 'preencher_sala'):
                self.view.preencher_sala(self.numero_sala)
        
        self.view.set_action_salvar(self.salvar_procedimento)
        self.view.set_action_voltar(self.voltar_menu)

    def salvar_procedimento(self):
        doenca = self.view.get_doenca()
        crm_medico = self.view.get_cpf_medico() 
        tipo_proc = self.view.get_procedimento()
        
        # Pega a sala da tela (o usuário pode ter mudado)
        sala_final = None
        if hasattr(self.view, 'get_sala'):
            sala_str = self.view.get_sala()
            if sala_str and sala_str.isdigit():
                sala_final = int(sala_str)

        if not doenca or not crm_medico or not tipo_proc:
            messagebox.showwarning("Aviso", "Preencha Doença, CRM e Tipo.")
            return

        # Chama o DAO (Passando a Sala junto, se sua procedure pedir)
        # Se sua procedure SQL não pede sala, remova o ultimo argumento
        sucesso, mensagem = self.dao.registrar_procedimento_completo(
            self.id_entrada, 
            crm_medico, 
            tipo_proc, 
            doenca,
            # Se sua procedure pede sala, descomente abaixo:
            sala_final 
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Procedimento registrado!")
            self.voltar_menu()
        else:
            messagebox.showerror("Erro", mensagem)

    def voltar_menu(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.view.janela, self.usuario)