from tkinter import *
from tkinter import ttk

class TelaPacientes:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Gestão de Pacientes")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        # --- TÍTULO ---
        ttk.Label(self.frm, text="Gerenciar Pacientes", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # --- CAMPOS DE CADASTRO ---
        # CPF
        ttk.Label(self.frm, text="CPF (11 dígitos):").grid(row=1, column=0, sticky=W)
        self.ent_cpf = ttk.Entry(self.frm, width=30)
        self.ent_cpf.grid(row=1, column=1, sticky=EW, pady=2)

        # Nome
        ttk.Label(self.frm, text="Nome Completo:").grid(row=2, column=0, sticky=W)
        self.ent_nome = ttk.Entry(self.frm, width=30)
        self.ent_nome.grid(row=2, column=1, sticky=EW, pady=2)

        # Data de Nascimento
        ttk.Label(self.frm, text="Data Nasc (AAAA-MM-DD):").grid(row=3, column=0, sticky=W)
        self.ent_data = ttk.Entry(self.frm, width=30)
        self.ent_data.grid(row=3, column=1, sticky=EW, pady=2)

        # Sexo
        ttk.Label(self.frm, text="Sexo (M/F):").grid(row=4, column=0, sticky=W)
        self.ent_sexo = ttk.Entry(self.frm, width=30)
        self.ent_sexo.grid(row=4, column=1, sticky=EW, pady=2)

        # Senha (para o paciente logar depois)
        ttk.Label(self.frm, text="Senha Provisória:").grid(row=5, column=0, sticky=W)
        self.ent_senha = ttk.Entry(self.frm, show="*", width=30)
        self.ent_senha.grid(row=5, column=1, sticky=EW, pady=2)

         #Sangue
        ttk.Label(self.frm, text="Tipo Sanguíneo").grid(row=6, column=0, sticky=W)
        self.ent_sangue = ttk.Entry(self.frm, width=30)
        self.ent_sangue.grid(row=6, column=1, sticky=EW, pady=2)

        # --- BOTÕES DE AÇÃO ---
        self.btn_cadastrar = ttk.Button(self.frm, text="Cadastrar Novo Paciente")
        self.btn_cadastrar.grid(row=7, column=0, pady=15, sticky=EW)

        self.btn_remover = ttk.Button(self.frm, text="Remover (Buscar pelo CPF)")
        self.btn_remover.grid(row=8, column=1, pady=15, sticky=EW)

        # --- LINHA DIVISÓRIA ---
        ttk.Separator(self.frm, orient=HORIZONTAL).grid(row=9, column=0, columnspan=2, sticky=EW, pady=10)
        
        # --- ÁREA DE HISTÓRICO ---
        ttk.Label(self.frm, text="Consultas e Entradas", font=("Arial", 12)).grid(row=10, column=0, columnspan=2)
        
        self.btn_buscar_hist = ttk.Button(self.frm, text="Buscar Histórico (Pelo CPF)")
        self.btn_buscar_hist.grid(row=11, column=0, columnspan=2, sticky=EW, pady=5)

        # Tabela (Treeview) para mostrar resultados
        columns = ('id', 'data', 'hospital')
        self.tree = ttk.Treeview(self.frm, columns=columns, show='headings', height=5)
        
        # Cabeçalhos da tabela
        self.tree.heading('id', text='ID Entrada')
        self.tree.heading('data', text='Data/Hora')
        self.tree.heading('hospital', text='Hospital')
        
        # Largura das colunas
        self.tree.column('id', width=80, anchor=CENTER)
        self.tree.column('data', width=150, anchor=CENTER)
        self.tree.column('hospital', width=200, anchor=W)
        
        self.tree.grid(row=10, column=0, columnspan=2, pady=10)

        # Botão Voltar
        self.btn_voltar = ttk.Button(self.frm, text="Voltar ao Menu Principal")
        self.btn_voltar.grid(row=11, column=0, columnspan=2, pady=10, sticky=EW)

    # --- GETTERS (Para o Controller pegar os dados) ---
    def get_cpf(self): return self.ent_cpf.get()
    def get_nome(self): return self.ent_nome.get()
    def get_data(self): return self.ent_data.get()
    def get_sexo(self): return self.ent_sexo.get()
    def get_senha(self): return self.ent_senha.get()
    def get_sangue(self): return self.ent_sangue.get()

    # --- LISTENER CONFIG (Para o Controller ligar os botões) ---
    def configurar_botoes(self, cmd_cadastrar, cmd_remover, cmd_historico, cmd_voltar):
        self.btn_cadastrar.config(command=cmd_cadastrar)
        self.btn_remover.config(command=cmd_remover)
        self.btn_buscar_hist.config(command=cmd_historico)
        self.btn_voltar.config(command=cmd_voltar)

    # --- MÉTODO PARA PREENCHER A TABELA ---
    def atualizar_tabela(self, lista_dados):
        # 1. Limpa a tabela atual
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # 2. Preenche com os dados novos vindos do banco
        # lista_dados deve ser uma lista de tuplas: [(1, '2023-01-01', 'Hosp A'), ...]
        for item in lista_dados:
            self.tree.insert('', END, values=item)