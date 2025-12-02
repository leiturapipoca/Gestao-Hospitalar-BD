from tkinter import *
from tkinter import ttk

from View.TelaHospital import TelaHospital
from View.TelaHospHosp import TelaHospHosp
from View.TelaLiberarSala import TelaLiberarSala
from Controller.InternosController import InternosController
import logging
from Model.HospitalDAO import hosps_and_gerentes

class HospitaisController:
    def __init__(self, root: Tk, dados_usuario):
        self.view = TelaHospital(root)
        self.root = root
        self.dados_usuario = dados_usuario
        self.config_tela_gerenciar_hosp(self.view)

    def config_tela_gerenciar_hosp(self, view: TelaHospital):
        view.set_action_return(self.voltar)
        view.set_action_hosps(self.selecionar_hosps)
        view.set_action_salas(self.selecionar_salas)

    def config_tela_hosp_hosp(self, view: TelaHospHosp):
        view.set_action_return(self.voltar)

    def config_tela_liberar_salas(self, view: TelaLiberarSala):
        view.set_action_return(self.voltar)
    
    def voltar(self):
        self.view.frm.destroy()
        InternosController(self.root, self.dados_usuario)

    def selecionar_hosps(self):
        logging.info("selecionar_hosps")
        self.view.frm.destroy()
        hospitais = hosps_and_gerentes()
        self.view = TelaHospHosp(self.root, hospitais)
        self.config_tela_hosp_hosp(self.view)
        
    def selecionar_salas(self):
        logging.info("selecionar_salas")
        self.view.frm.destroy()
        self.view = TelaLiberarSala(self.root, [("sala1", "2"), ("sala2", "3")])
        self.config_tela_liberar_salas(self.view)

