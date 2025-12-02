from tkinter import messagebox
from View.TelaLiberarSala import TelaLiberarSala
from Model.SalasDAO import SalasDAO
import Model.HospitalDAO as HospitalDAO
import logging

class SalasController:
    def __init__(self, root, dados_usuario):
        self.root = root
        self.dados_usuario = dados_usuario # {'matricula': 1, 'nome': 'Carlos'}
        self.view = None
        self.salas_dao = SalasDAO()
        
        # Já inicia abrindo a tela
        self.abrir_tela_liberar_salas()

    def abrir_tela_liberar_salas(self):
        logging.info("Iniciando fluxo de liberar salas (SalasController)")
        
        # 1. Descobrir o Hospital do Usuário
        if not isinstance(self.dados_usuario, dict): 
            messagebox.showerror("Erro", "Dados de usuário inválidos.")
            self.voltar_para_hospitais()
            return

        matricula = self.dados_usuario.get('matricula')
        
        # Usa a conexão do SalasDAO para buscar o CNES
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.salas_dao.connection)
        
        if not cnes:
            messagebox.showwarning("Aviso", "Você não está vinculado a nenhum hospital para gerenciar salas.")
            self.voltar_para_hospitais()
            return

        # 2. Buscar Salas OCUPADAS desse hospital
        salas_ocupadas = self.salas_dao.get_salas_ocupadas_by_cnes(cnes)
        
        if not salas_ocupadas:
            messagebox.showinfo("Info", "Não há salas ocupadas neste hospital no momento.")
            # Pode optar por voltar ou abrir vazia. Vamos abrir vazia para o usuário ver.
        
        # 3. Abrir a tela
        self.view = TelaLiberarSala(self.root, salas_ocupadas)
        
        # Configura os botões
        self.view.set_action_return(self.voltar_para_hospitais)
        self.view.set_action_liberar(self.liberar_sala_selecionada)

    def liberar_sala_selecionada(self):
        selecao = self.view.get_sala_selecionada() # Ex: "Sala 101 (ID: 5)"
        
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma sala.")
            return
        
        try:
            # Extrai o ID: "Sala 101 (ID: 5)" -> "5)" -> "5"
            id_sala_str = selecao.split("ID: ")[1].replace(")", "")
            id_sala = int(id_sala_str)
            
            if self.salas_dao.liberar_sala(id_sala):
                messagebox.showinfo("Sucesso", "Sala liberada com sucesso!")
                # Recarrega a tela (destrói e cria de novo para atualizar a lista)
                self.view.frm.destroy()
                self.abrir_tela_liberar_salas()
            else:
                messagebox.showerror("Erro", "Falha ao liberar sala.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar sala: {e}")

    def voltar_para_hospitais(self):
        # Importa aqui para evitar ciclo de importação
        from Controller.HospitaisController import HospitaisController
        
        if self.view:
            self.view.frm.destroy()
            
        # Volta para o menu de hospitais passando os dados do usuário
        HospitaisController(self.root, self.dados_usuario)