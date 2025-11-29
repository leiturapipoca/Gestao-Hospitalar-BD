from Controller import CpfController

class ProfCreateDto:
    def __init__(self, cpf: str, nome: str, tipo: str, crm_med: str, cod_enf: str):
        ProfCreateDto.validate_tipo(tipo)
        CpfController.validate_cpf(cpf)
        self.cpf = cpf
        self.nome = nome
        self.tipo = tipo
        self.crm_med = crm_med
        self.cod_enf = cod_enf

    @staticmethod
    def validate_tipo(tipo: str):
        if tipo != 'M' and tipo != 'E':
            raise ValueError(f"Erro de validação do tipo de profissional de saude: tipo '{tipo}' não é um tipo válido ('E', 'M').")
    
