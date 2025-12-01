# View/TelaPacientePerfil.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog

class TelaPacientePerfil:
    def __init__(self, master, use_toplevel=True):
        if use_toplevel:
            self.janela = Toplevel(master) if master else Tk()
        else:
            self.janela = master if master else Tk()

        self.janela.title("Meu Perfil - Paciente")
        self.frm = ttk.Frame(self.janela, padding=12)
        self.frm.grid(sticky="nsew")
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        # --- Topo: informações pessoais + ações rápidas ---
        top = ttk.Frame(self.frm)
        top.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0,8))
        lbl_title = ttk.Label(top, text="Meu Perfil", font=("Arial", 14, "bold"))
        lbl_title.pack(side=LEFT)

        # ação export
        self.btn_export = ttk.Button(top, text="Exportar CSV")
        self.btn_export.pack(side=RIGHT)

        # info
        info = ttk.Frame(self.frm)
        info.grid(row=1, column=0, columnspan=2, sticky="we")
        self.lbl_nome = ttk.Label(info, text="Nome: ")
        self.lbl_nome.grid(row=0, column=0, sticky="w")
        self.lbl_cpf = ttk.Label(info, text="CPF: ")
        self.lbl_cpf.grid(row=0, column=1, sticky="w", padx=10)
        self.lbl_dt = ttk.Label(info, text="Nascimento: ")
        self.lbl_dt.grid(row=1, column=0, sticky="w")
        self.lbl_sexo = ttk.Label(info, text="Sexo: ")
        self.lbl_sexo.grid(row=1, column=1, sticky="w", padx=10)
        self.lbl_sangue = ttk.Label(info, text="Tipo Sanguíneo: ")
        self.lbl_sangue.grid(row=2, column=0, sticky="w")

        # --- Telefones (com CRUD simples) ---
        tel_frame = ttk.Labelframe(self.frm, text="Telefones", padding=8)
        tel_frame.grid(row=2, column=0, sticky="nsew", padx=(0,8), pady=(10,0))
        self.lst_telefones = Listbox(tel_frame, height=6)
        self.lst_telefones.grid(row=0, column=0, rowspan=4, sticky="nswe")
        tel_controls = ttk.Frame(tel_frame)
        tel_controls.grid(row=0, column=1, sticky="n")
        ttk.Label(tel_controls, text="Número:").grid(row=0, column=0, sticky="w")
        self.entry_tel = ttk.Entry(tel_controls)
        self.entry_tel.grid(row=1, column=0, pady=(4,8))
        ttk.Button(tel_controls, text="Adicionar").grid(row=2, column=0, pady=4)
        ttk.Button(tel_controls, text="Remover").grid(row=3, column=0, pady=4)
        ttk.Button(tel_controls, text="Editar").grid(row=4, column=0, pady=4)

        # --- Doenças (apenas exibir por enquanto) ---
        doenças_frame = ttk.Labelframe(self.frm, text="Doenças", padding=8)
        doenças_frame.grid(row=2, column=1, sticky="nsew", pady=(10,0))
        self.lst_doencas = Listbox(doenças_frame, height=6)
        self.lst_doencas.grid(row=0, column=0, sticky="nswe")

        # --- Filtros e paginação para entradas/procedimentos ---
        filter_frame = ttk.Frame(self.frm)
        filter_frame.grid(row=3, column=0, columnspan=2, sticky="we", pady=(10,0))
        ttk.Label(filter_frame, text="Data início (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.entry_start = ttk.Entry(filter_frame, width=12)
        self.entry_start.grid(row=0, column=1, sticky="w", padx=(4,12))
        ttk.Label(filter_frame, text="Data fim (YYYY-MM-DD):").grid(row=0, column=2, sticky="w")
        self.entry_end = ttk.Entry(filter_frame, width=12)
        self.entry_end.grid(row=0, column=3, sticky="w", padx=(4,12))
        self.btn_filtrar = ttk.Button(filter_frame, text="Filtrar")
        self.btn_filtrar.grid(row=0, column=4, padx=(8,0))

        # paginação
        pag_frame = ttk.Frame(self.frm)
        pag_frame.grid(row=4, column=0, columnspan=2, sticky="we", pady=(8,0))
        self.btn_prev = ttk.Button(pag_frame, text="Anterior")
        self.btn_prev.pack(side=LEFT)
        self.lbl_page = ttk.Label(pag_frame, text="Página 1")
        self.lbl_page.pack(side=LEFT, padx=8)
        self.btn_next = ttk.Button(pag_frame, text="Próximo")
        self.btn_next.pack(side=LEFT)

        # --- Entradas (admissões) ---
        entradas_label = ttk.Label(self.frm, text="Entradas (admissões):", font=("Arial", 10, "bold"))
        entradas_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10,0))
        self.tree_entradas = ttk.Treeview(self.frm, columns=("codigo", "data", "hospital", "descricao"), show="headings", height=6)
        self.tree_entradas.heading("codigo", text="Código")
        self.tree_entradas.heading("data", text="Data")
        self.tree_entradas.heading("hospital", text="Hospital")
        self.tree_entradas.heading("descricao", text="Descrição")
        self.tree_entradas.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # --- Procedimentos/Exames ---
        proc_label = ttk.Label(self.frm, text="Procedimentos / Exames:", font=("Arial", 10, "bold"))
        proc_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(10,0))
        self.tree_procs = ttk.Treeview(self.frm, columns=("cod_proc", "tipo", "cod_entr", "data", "hospital"), show="headings", height=6)
        self.tree_procs.heading("cod_proc", text="Proc. Código")
        self.tree_procs.heading("tipo", text="Tipo")
        self.tree_procs.heading("cod_entr", text="Entrada")
        self.tree_procs.heading("data", text="Data")
        self.tree_procs.heading("hospital", text="Hospital")
        self.tree_procs.grid(row=8, column=0, columnspan=2, sticky="nsew")

        # botão sair
        self.btn_fechar = ttk.Button(self.frm, text="Sair", command=self.janela.destroy)
        self.btn_fechar.grid(row=9, column=0, columnspan=2, pady=(10,0))

        # responsividade
        self.frm.columnconfigure(0, weight=1)
        self.frm.columnconfigure(1, weight=1)
        self.frm.rowconfigure(6, weight=1)
        self.frm.rowconfigure(8, weight=1)

        # -------------------------
        # Expor referências dos widgets que o controller usará/ligará:
        # - telefone controls: entry_tel, lst_telefones, e os 3 botões (na ordem)
        # - filtros: entry_start, entry_end, btn_filtrar
        # - paginação: btn_prev, btn_next, lbl_page
        # - export: btn_export
        # - árvores: tree_entradas, tree_procs (duplo clique)
        # -------------------------
    # métodos públicos simples
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

    def set_entradas(self, lista_dicts):
        for i in self.tree_entradas.get_children():
            self.tree_entradas.delete(i)
        for d in lista_dicts:
            self.tree_entradas.insert('', 'end', values=(d.get('codigo'), d.get('data'), d.get('hospital_nome', d.get('cnes_hosp')), d.get('descricao')))

    def set_procedimentos(self, lista_dicts):
        for i in self.tree_procs.get_children():
            self.tree_procs.delete(i)
        for d in lista_dicts:
            self.tree_procs.insert('', 'end', values=(d.get('codigo'), d.get('tipo_nome', d.get('tipo')), d.get('cod_entr'), d.get('data'), d.get('hospital_nome')))

    # helper para recuperar telefone selecionado
    def get_selected_telefone(self):
        sel = self.lst_telefones.curselection()
        if not sel: 
            return None
        return self.lst_telefones.get(sel[0])

    # helper para recuperar seleção nas tables
    def get_selected_entrada(self):
        sel = self.tree_entradas.selection()
        if not sel: return None
        return self.tree_entradas.item(sel[0])['values']

    def get_selected_procedimento(self):
        sel = self.tree_procs.selection()
        if not sel: return None
        return self.tree_procs.item(sel[0])['values']
