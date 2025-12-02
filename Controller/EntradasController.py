from tkinter import messagebox, END
from View.TelaEntradas import TelaEntradas
from Model.EntradaDAO import EntradaDAO
import Model.HospitalDAO as HospitalDAO 
from Controller.ProcedimentosController import ProcedimentosController


class EntradasController:
    def __init__(self, root, usuario):
        # 1. Instancia o DAO
        self.dao = EntradaDAO()
        
        self.usuario = usuario 
        self.cnes_vinculado = None 
        
        # 2. PREPARA OS DADOS ANTES DE CRIAR A TELA
        salas_disponiveis = self.preparar_dados_hospital()

        # 3. CRIA A TELA PASSANDO AS SALAS
        self.view = TelaEntradas(root, salas_disponiveis)
        
        # Preenche o nome do hospital (estética) se já tiver achado
        if self.cnes_vinculado:
            nome_hosp = HospitalDAO.get_name_by_cnes(self.cnes_vinculado, self.dao.connection)
            texto = nome_hosp if nome_hosp else self.cnes_vinculado
            self.view.preencher_cnes(texto)

        self.view.set_action_salvar(self.salvar_e_avancar)
        self.view.set_action_voltar(self.voltar)

    def preparar_dados_hospital(self):
        """
        Busca o CNES do funcionário e, com ele, busca as salas livres.
        """
        if not isinstance(self.usuario, dict): return ()
        matricula = self.usuario.get('matricula')
        if not matricula: return ()

        # Busca CNES
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.dao.connection)
        
        if cnes:
            self.cnes_vinculado = cnes
            # BUSCA AS SALAS LIVRES DESTE HOSPITAL
            return HospitalDAO.get_salas_livres_by_cnes(cnes, self.dao.connection)
        else:
            messagebox.showwarning("Aviso", "Funcionário sem vínculo hospitalar.")
            return ()

    def salvar_e_avancar(self):
        cpf = self.view.get_cpf()
        cnes_salvar = self.cnes_vinculado
        desc = self.view.get_description()
        
        # PEGA A SALA SELECIONADA
        sala_str = self.view.get_sala() # Ex: "Sala 101"

        if not cpf or not cnes_salvar or not sala_str:
            messagebox.showwarning("Aviso", "Preencha CPF e escolha uma Sala!")
            return
        
        # Extrai apenas o número da sala "Sala 101" -> 101
        try:
            numero_sala = int(sala_str.replace("Sala ", ""))
        except:
            messagebox.showerror("Erro", "Formato de sala inválido.")
            return

        # Passa a sala para o DAO (Você precisará atualizar o DAO para receber isso)
        # Como combinamos que a Procedure Complexa de PROCEDIMENTO vai usar a sala,
        # aqui na Entrada você pode ou salvar na ENTRADA (se criou coluna) ou passar para o próximo controller.
        
        # Vou assumir que você quer salvar a entrada normal e passar a sala para o ProcedimentosController
        id_entrada = self.dao.registrar_entrada(cpf, cnes_salvar, desc)

        if id_entrada:
            self.view.frm.destroy()
            # Passa a sala escolhida para o próximo passo!
            ProcedimentosController(self.view.janela, self.usuario, id_entrada, numero_sala)
        else:
            messagebox.showerror("Erro", "Falha ao registrar entrada.")

    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.view.janela, self.usuario)