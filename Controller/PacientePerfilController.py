# Controller/PacientePerfilController.py
from View.TelaPacientePerfil import TelaPacientePerfil
from Model.PacienteDAO import PacienteDAO
from tkinter import messagebox, simpledialog, filedialog
import csv
from datetime import datetime

class PacientePerfilController:
    def __init__(self, root, paciente_dict, use_toplevel=True):
        self.root = root
        self.paciente = paciente_dict
        self.view = TelaPacientePerfil(root, use_toplevel=use_toplevel)
        self.dao = PacienteDAO()

        # paginação
        self.page = 0
        self.page_size = 10

        # preencher dados iniciais
        self.view.set_dados_pessoais(self.paciente)
        self._carregar_telefones()
        self._carregar_doencas()
        self._carregar_entradas()
        self._carregar_procedimentos()

        # conectar ações da view
        # telefones: os três botões (recuperando pela hierarquia de widgets)
        tel_controls = self.view.frm.nametowidget(self.view.frm.winfo_children()[2].winfo_children()[1].winfo_name())
        # above line is brittle; instead, we will bind by searching the frame (safer below)
        # procurar os botões na árvore de widgets:
        # simplificamos: assumimos os botões estão nessa ordem no tel_controls -> melhor ligar diretamente:
        # para evitar fragilidade, vamos localizar botões pelo texto:
        for child in self.view.frm.winfo_children():
            # localizar o Labelframe de Telefones
            if isinstance(child, type(self.view.lst_telefones.master)) and getattr(child, 'cget', lambda k: None)('text') == 'Telefones':
                tframe = child
                break
        else:
            tframe = None

        if tframe:
            # botões estão no tel_controls (segunda coluna)
            controls = tframe.winfo_children()[1]  # Frame
            # encontrar botões por ordem ou texto
            btns = [w for w in controls.winfo_children() if hasattr(w, 'cget') and w.cget('text') in ('Adicionar','Remover','Editar')]
            if len(btns) >= 3:
                btn_add, btn_remove, btn_edit = btns[0], btns[1], btns[2]
                btn_add.config(command=self.on_add_telefone)
                btn_remove.config(command=self.on_remove_telefone)
                btn_edit.config(command=self.on_edit_telefone)

        # filtros e paginação
        self.view.btn_filtrar.config(command=self.on_filtrar)
        self.view.btn_next.config(command=self.on_next_page)
        self.view.btn_prev.config(command=self.on_prev_page)

        # export
        self.view.btn_export.config(command=self.on_export_csv)

        # duplo clique nas trees para ver detalhes
        self.view.tree_entradas.bind("<Double-1>", self.on_entrada_duplo)
        self.view.tree_procs.bind("<Double-1>", self.on_proc_duplo)

    # --- telefones ---
    def _carregar_telefones(self):
        telefones = self.dao.get_telefones(self.paciente['cpf'])
        self.view.set_telefones(telefones)

    def on_add_telefone(self):
        numero = self.view.entry_tel.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Digite o número para adicionar.")
            return
        ok = self.dao.add_telefone(self.paciente['cpf'], numero)
        if ok:
            messagebox.showinfo("Sucesso", "Telefone adicionado.")
            self._carregar_telefones()
            self.view.entry_tel.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar o telefone.")

    def on_remove_telefone(self):
        selecionado = self.view.get_selected_telefone()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um telefone para remover.")
            return
        if not messagebox.askyesno("Confirmar", f"Remover telefone {selecionado}?"):
            return
        ok = self.dao.remove_telefone(self.paciente['cpf'], selecionado)
        if ok:
            messagebox.showinfo("Sucesso", "Telefone removido.")
            self._carregar_telefones()
        else:
            messagebox.showerror("Erro", "Não foi possível remover.")

    def on_edit_telefone(self):
        selecionado = self.view.get_selected_telefone()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um telefone para editar.")
            return
        novo = simpledialog.askstring("Editar telefone", "Novo número:", initialvalue=selecionado)
        if not novo:
            return
        ok = self.dao.update_telefone(self.paciente['cpf'], selecionado, novo)
        if ok:
            messagebox.showinfo("Sucesso", "Telefone atualizado.")
            self._carregar_telefones()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar telefone.")

    # --- doenças ---
    def _carregar_doencas(self):
        doencas = self.dao.get_doencas(self.paciente['cpf'])
        self.view.set_doencas(doencas)

    # --- entradas / procedimentos (com paginação + filtro) ---
    def _carregar_entradas(self):
        start = self.view.entry_start.get().strip() or None
        end = self.view.entry_end.get().strip() or None
        limit = self.page_size
        offset = self.page * self.page_size
        entradas = self.dao.get_entradas_detalhadas(self.paciente['cpf'], limit=limit, offset=offset, start_date=start, end_date=end)
        self.view.set_entradas(entradas)
        self.view.lbl_page.config(text=f"Página {self.page+1}")

    def _carregar_procedimentos(self):
        start = self.view.entry_start.get().strip() or None
        end = self.view.entry_end.get().strip() or None
        limit = self.page_size
        offset = self.page * self.page_size
        procs = self.dao.get_procedimentos_detalhados(self.paciente['cpf'], limit=limit, offset=offset, start_date=start, end_date=end)
        self.view.set_procedimentos(procs)

    def on_filtrar(self):
        # reset paginação e recarrega
        self.page = 0
        self._carregar_entradas()
        self._carregar_procedimentos()

    def on_next_page(self):
        self.page += 1
        self._carregar_entradas()
        self._carregar_procedimentos()

    def on_prev_page(self):
        if self.page > 0:
            self.page -= 1
            self._carregar_entradas()
            self._carregar_procedimentos()

    # --- export CSV (entradas + procedimentos) ---
    def on_export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], title="Salvar relatório CSV")
        if not path:
            return
        try:
            # pegar TODOS os registros (sem limite) filtrados pelo período atual
            start = self.view.entry_start.get().strip() or None
            end = self.view.entry_end.get().strip() or None
            entradas = self.dao.get_entradas_detalhadas(self.paciente['cpf'], start_date=start, end_date=end)
            procs = self.dao.get_procedimentos_detalhados(self.paciente['cpf'], start_date=start, end_date=end)

            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Tipo", "Código", "Data", "Hospital", "Descrição/Tipo", "Entrada Código"])
                for e in entradas:
                    writer.writerow(["Entrada", e.get('codigo'), e.get('data'), e.get('hospital_nome', e.get('cnes_hosp')), e.get('descricao',''), ""])
                for p in procs:
                    writer.writerow(["Procedimento", p.get('codigo'), p.get('data'), p.get('hospital_nome'), p.get('tipo_nome',''), p.get('cod_entr')])
            messagebox.showinfo("Exportado", f"Relatório salvo em {path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exportar CSV: {e}")

    # --- duplo clique para ver detalhes ---
    def on_entrada_duplo(self, event):
        sel = self.view.get_selected_entrada()
        if not sel:
            return
        # sel é tuple (codigo, data, hospital, descricao)
        codigo, data, hospital, descricao = sel[0], sel[1], sel[2], sel[3]
        messagebox.showinfo("Entrada", f"Código: {codigo}\nData: {data}\nHospital: {hospital}\nDescrição: {descricao}")

    def on_proc_duplo(self, event):
        sel = self.view.get_selected_procedimento()
        if not sel:
            return
        cod_proc, tipo, cod_entr, data, hospital = sel
        messagebox.showinfo("Procedimento", f"Código: {cod_proc}\nTipo: {tipo}\nEntrada: {cod_entr}\nData: {data}\nHospital: {hospital}")
