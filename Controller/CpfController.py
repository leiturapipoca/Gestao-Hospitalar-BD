
def validate_cpf(cpf: str) -> None:
    '''função que verifica se uma string de cpf é válida'''
    if (len(cpf) != 11): raise ValueError(f"cpf deve ter 11 caracteres. {cpf} possui {len(cpf)}")
    try: int(cpf)
    except: raise ValueError(f"cpf deve ser um valor numérico e não deve conter caracteres ou separadores especiais como '.' e '-'. Cpf fornecido: {cpf}")
