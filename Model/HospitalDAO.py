from SQL import databaseUtils
from typing import Any
import logging

test_logger = logging.getLogger("HospitalDAO TEST")

def validate_cnes(cnes: str) -> None:
    """confere a conformidade do cnes ao formato esperado"""

    if len(cnes) != 7:
        raise ValueError(f"cnes deve conter 7 caracteres. cnes informad ({cnes}) possui {len(cnes)}.")

    try: int(cnes)
    except: ValueError(f"cnes deve ser exclusivamente numérico. cnes informado, {cnes}, não é.")


def num_of_docs_in_hosp(cnes: str, connection: Any) -> int:
    """conta o número de medicos vinculados a um dado hospital"""

    validate_cnes(cnes)
    cursor = connection.cursor()
    cursor.execute(f"""
                   SELECT COUNT(*) FROM prof_saude_hosp
                   JOIN profissional_saude
                   ON profissional_saude.cpf = prof_saude_hosp.cpf_prof
                   WHERE
                       prof_saude_hosp.cnes_hosp = '{cnes}'
                       AND 
                       profissional_saude.tipo = 'M';
                   """)
    rows = cursor.fetchall()
    return rows[0][0]


def num_of_enf_in_hosp(cnes: str, connection: Any) -> int:
    """conta o número de enfermeiros vinculados a um dado hospital"""

    validate_cnes(cnes)
    cursor = connection.cursor()
    cursor.execute(f"""
                   SELECT COUNT(*) FROM prof_saude_hosp
                   JOIN profissional_saude
                   ON profissional_saude.cpf = prof_saude_hosp.cpf_prof
                   WHERE
                       prof_saude_hosp.cnes_hosp = '{cnes}'
                       AND 
                       profissional_saude.tipo = 'E';
                   """)
    rows = cursor.fetchall()
    return rows[0][0]


def num_of_fun_in_hosp(cnes: str, connection: Any) -> int:
    """conta o número de empregados (excluindo médicos e enfermeiros) vinculados a um dado hospital"""

    validate_cnes(cnes)
    cursor = connection.cursor()
    cursor.execute(f"""
                   SELECT COUNT(*) FROM func_hosp
                   JOIN funcionario
                   ON funcionario.matricula = func_hosp.matr_func
                   WHERE func_hosp.cnes_hosp = '{cnes}';
                   """)
    rows = cursor.fetchall()
    return rows[0][0]

def get_cnes_by_matricula(matricula: int, connection: Any) -> str:
    """
    busca qual o CNES do hospital onde o funcionário trabalha.
    retorna o CNES (string) ou None se não achar.
    """
    try:
        cursor = connection.cursor()
        
        sql = "SELECT CNES_HOSP FROM FUNC_HOSP WHERE MATR_FUNC = %s"
        
        cursor.execute(sql, (matricula,))
        row = cursor.fetchone()
        
        if row:
            return row[0] # Retorna o CNES (Ex: "0000001")
        else:
            return None
        
    except Exception as e:
        print(f"Erro ao buscar hospital do funcionário: {e}")
        return None
    
def get_name_by_cnes(cnes: str, connection: Any) -> str:
    
    try:
        cursor = connection.cursor()
        sql = "SELECT NOME FROM HOSPITAL WHERE CNES = %s"
        cursor.execute(sql, (cnes,))
        row = cursor.fetchone()
        
        if row:
            return row[0] # Retorna o Nome (Ex: "Hospital Central")
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar nome do hospital: {e}")
        return None
    

def run_hosp_model_tests():
    """roda testes verificando o correto funcionamento das queries presentes no HospitalDAO"""
    connection = databaseUtils.connect_to_database() 
    cnes1 = "0000001"
    cnes2 = "0000002"
    test_logger.info(f"número de médicos no hospital {cnes1}: {num_of_docs_in_hosp(cnes1, connection)}")
    test_logger.info(f"número de enfermeiros no hospital {cnes1}: {num_of_enf_in_hosp(cnes1, connection)}")
    test_logger.info(f"número de funcionários no hospital {cnes1}: {num_of_fun_in_hosp(cnes1, connection)}")
    test_logger.info(f"número de médicos no hospital {cnes2}: {num_of_docs_in_hosp(cnes2, connection)}")
    test_logger.info(f"número de enfermeiros no hospital {cnes2}: {num_of_enf_in_hosp(cnes2, connection)}")
    test_logger.info(f"numero de funcionários no hospital {cnes2}: {num_of_fun_in_hosp(cnes2, connection)}")
