from tkinter import *
from tkinter import ttk

class TelaPerfilFuncionario:
    def __init__(self, master, dados_atuais):
        self.janela = master
        self.janela.title("Gerenciar Meu Perfil")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Editar Meus Dados", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Matrícula
        ttk.Label(self.frm, text="Matrícula:").grid(row=1, column=0, sticky=W)
        self.ent_matr = ttk.Entry(self.frm)
        self.ent_matr.grid(row=1, column=1, sticky=EW)
        self.ent_matr.insert(0, dados_atuais.get('matricula', ''))
        self.ent_matr.config(state='readonly')

        # Nome
        ttk.Label(self.frm, text="Nome Completo:").grid(row=2, column=0, sticky=W)
        self.ent_nome = ttk.Entry(self.frm, width=30)
        self.ent_nome.grid(row=2, column=1, sticky=EW, pady=5)
        self.ent_nome.insert(0, dados_atuais.get('nome', ''))

        # Senha
        ttk.Label(self.frm, text="Nova Senha:").grid(row=3, column=0, sticky=W)
        self.ent_senha = ttk.Entry(self.frm, show="*", width=30)
        self.ent_senha.grid(row=3, column=1, sticky=EW, pady=5)
        
        # --- ÁREA DA FOTO ---
        ttk.Separator(self.frm, orient=HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=EW, pady=15)
        ttk.Label(self.frm, text="Foto de Perfil", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=W)
        
        self.lbl_status_foto = ttk.Label(self.frm, text="Nenhuma foto selecionada", foreground="gray")
        self.lbl_status_foto.grid(row=5, column=1, sticky=W)

        self.btn_foto = ttk.Button(self.frm, text="Selecionar Nova Foto...")
        self.btn_foto.grid(row=6, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Separator(self.frm, orient=HORIZONTAL).grid(row=7, column=0, columnspan=2, sticky=EW, pady=15)

        # Botões Principais
        self.btn_salvar = ttk.Button(self.frm, text="SALVAR TUDO")
        self.btn_salvar.grid(row=8, column=0, columnspan=2, pady=10, sticky=EW)
        
        self.btn_voltar = ttk.Button(self.frm, text="Cancelar")
        self.btn_voltar.grid(row=9, column=0, columnspan=2, sticky=EW)

    # Getters
    def get_nome(self): return self.ent_nome.get()
    def get_senha(self): return self.ent_senha.get()

    # Configuração
    def configurar_botoes(self, cmd_salvar, cmd_voltar, cmd_foto):
        self.btn_salvar.config(command=cmd_salvar)
        self.btn_voltar.config(command=cmd_voltar)
        self.btn_foto.config(command=cmd_foto)