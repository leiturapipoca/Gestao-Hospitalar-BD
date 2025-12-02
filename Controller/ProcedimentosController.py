from tkinter import messagebox
from View.TelaProcedimentos import TelaProcedimentos
from Model.ProcedimentosDAO import ProcedimentosDAO

class ProcedimentosController:
    # --- ADICIONADO 'cnes_hospital=None' no final ---
    def __init__(self, root, usuario, id_entrada, numero_sala=None, cnes_hospital=None):
        self.usuario = usuario
        self.id_entrada = id_entrada 
        self.numero_sala = numero_sala
        self.cnes_hospital = cnes_hospital # Guarda o hospital
        
        self.dao = ProcedimentosDAO()
        
        # Busca tipos
        lista_tipos = self.dao.get_tipos_procedimento()
        
        # --- FILTRA OS MÉDICOS PELO HOSPITAL ---
        # Passamos o CNES que veio da tela anterior
        lista_medicos = self.dao.get_medicos_disponiveis(self.cnes_hospital)
        
        # Cria a View
        self.view = TelaProcedimentos(root, lista_tipos, lista_medicos)
        
        if self.numero_sala and hasattr(self.view, 'preencher_sala'):
            self.view.preencher_sala(self.numero_sala)

        self.view.set_action_salvar(self.salvar_procedimento)
        self.view.set_action_voltar(self.voltar_menu)

    def salvar_procedimento(self):
        # pega as coisas das telas
        doenca = self.view.get_doenca()
        
        medico_str = self.view.get_cpf_medico() 
        tipo_proc = self.view.get_procedimento()
        
        # Pega a sala 
        sala_final = self.numero_sala
        if hasattr(self.view, 'get_sala') and self.view.get_sala():
             try:
                 s = self.view.get_sala()
                 if s.isdigit(): sala_final = int(s)
             except: pass

        if not doenca or not medico_str or not tipo_proc:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            #Extrai só o CRM da string do combobox
            crm_puro = medico_str.split(' - ')[0].strip()
        except:
            messagebox.showerror("Erro", "Médico inválido.")
            return

        # Chama DAO
        sucesso, mensagem = self.dao.registrar_procedimento_completo(
            self.id_entrada, 
            crm_puro, 
            tipo_proc, 
            doenca,
            int(sala_final) if sala_final else 0
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