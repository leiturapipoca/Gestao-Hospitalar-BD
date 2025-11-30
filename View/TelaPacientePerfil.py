# View/TelaPacientePerfil.py
from tkinter import *
from tkinter import ttk

class TelaPacientePerfil:
    def __init__(self, master):
        self.janela = Toplevel(master) if master else Tk()
        self.janela.title("Meu Perfil - Paciente")
        self.frm = ttk.Frame(self.janela, padding=12)
        self.frm.grid(sticky="nsew")
        # Layout básico
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        # --- INFORMAÇÕES PESSOAIS ---
        lbl_title = ttk.Label(self.frm, text="Meu Perfil", font=("Arial", 14, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(0,8), sticky="w")

        # Personal info labels
        self.lbl_nome = ttk.Label(self.frm, text="Nome: ")
        self.lbl_nome.grid(row=1, column=0, sticky="w")
        self.lbl_cpf = ttk.Label(self.frm, text="CPF: ")
        self.lbl_cpf.grid(row=1, column=1, sticky="w")
        self.lbl_dt = ttk.Label(self.frm, text="Nascimento: ")
        self.lbl_dt.grid(row=2, column=0, sticky="w")
        self.lbl_sexo = ttk.Label(self.frm, text="Sexo: ")
        self.lbl_sexo.grid(row=2, column=1, sticky="w")
        self.lbl_sangue = ttk.Label(self.frm, text="Tipo Sanguíneo: ")
        self.lbl_sangue.grid(row=3, column=0, sticky="w")

        # --- TELEFONES e DOENÇAS ---
        ttk.Label(self.frm, text="Telefones:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10,0))
        self.lst_telefones = Listbox(self.frm, height=4)
        self.lst_telefones.grid(row=5, column=0, sticky="we", padx=(0,8))

        ttk.Label(self.frm, text="Doenças:", font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w", pady=(10,0))
        self.lst_doencas = Listbox(self.frm, height=4)
        self.lst_doencas.grid(row=5, column=1, sticky="we")

        # --- ENTRADAS (admissões) ---
        ttk.Label(self.frm, text="Entradas (admissões):", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, sticky="w", pady=(10,0))
        self.tree_entradas = ttk.Treeview(self.frm, columns=("codigo", "data", "hospital", "descricao"), show="headings", height=6)
        self.tree_entradas.heading("codigo", text="Código")
        self.tree_entradas.heading("data", text="Data")
        self.tree_entradas.heading("hospital", text="CNES Hospital")
        self.tree_entradas.heading("descricao", text="Descrição")
        self.tree_entradas.grid(row=7, column=0, columnspan=2, sticky="nsew")

        # --- PROCEDIMENTOS/EXAMES ---
        ttk.Label(self.frm, text="Procedimentos / Exames:", font=("Arial", 10, "bold")).grid(row=8, column=0, columnspan=2, sticky="w", pady=(10,0))
        self.tree_procs = ttk.Treeview(self.frm, columns=("cod_proc", "nome_tipo", "cod_entr", "data", "hospital"), show="headings", height=6)
        self.tree_procs.heading("cod_proc", text="Proc. Código")
        self.tree_procs.heading("nome_tipo", text="Tipo")
        self.tree_procs.heading("cod_entr", text="Entr. Código")
        self.tree_procs.heading("data", text="Data Entrada")
        self.tree_procs.heading("hospital", text="Hospital")
        self.tree_procs.grid(row=9, column=0, columnspan=2, sticky="nsew")

        # Botão fechar
        self.btn_fechar = ttk.Button(self.frm, text="Fechar", command=self.janela.destroy)
        self.btn_fechar.grid(row=10, column=0, columnspan=2, pady=(10,0))

        # Ajuste responsivo
        self.frm.columnconfigure(0, weight=1)
        self.frm.columnconfigure(1, weight=1)
        self.frm.rowconfigure(7, weight=1)
        self.frm.rowconfigure(9, weight=1)

    # Métodos auxiliares para popular dados
    def set_dados_pessoais(self, paciente_dict):
        self.lbl_nome.config(text=f"Nome: {paciente_dict.get('nome','')}")
        self.lbl_cpf.config(text=f"CPF: {paciente_dict.get('cpf','')}")
        self.lbl_dt.config(text=f"Nascimento: {paciente_dict.get('dt_nasc','')}")
        self.lbl_sexo.config(text=f"Sexo: {paciente_dict.get('sexo','')}")
        self.lbl_sangue.config(text=f"Tipo Sanguíneo: {paciente_dict.get('tipo_sang','')}")

    def set_telefones(self, lista):
        self.lst_telefones.delete(0, 'end')
        for t in lista:
            self.lst_telefones.insert('end', t)

    def set_doencas(self, lista):
        self.lst_doencas.delete(0, 'end')
        for d in lista:
            self.lst_doencas.insert('end', d)

    def set_entradas(self, lista_tuplas):
        for i in self.tree_entradas.get_children():
            self.tree_entradas.delete(i)
        for tup in lista_tuplas:
            # tup: (codigo, data, cnes_hosp, descricao)
            self.tree_entradas.insert('', 'end', values=tup)

    def set_procedimentos(self, lista_tuplas):
        for i in self.tree_procs.get_children():
            self.tree_procs.delete(i)
        for tup in lista_tuplas:
            # tup: (proc_codigo, tipo_nome, cod_entr, data, hospital)
            self.tree_procs.insert('', 'end', values=tup)
