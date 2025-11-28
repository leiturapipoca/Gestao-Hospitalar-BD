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
