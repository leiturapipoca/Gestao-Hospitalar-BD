import psycopg2
import logging
import json
from typing import Any

logger = logging.getLogger(__name__)
logging.basicConfig(filename='program.log', level=logging.INFO)


def load_env_file():
    try:
        f = open('.env.json', 'r')
        data = json.load(f);
        f.close
        return data
    except json.JSONDecodeError as e:
        logger.error(f"erro ao decodificar variáveis de ambiente em '.env.json'. mensagem: '{e.msg}' linha: {e.lineno} coluna: {e.colno}")
        f.close()
        raise e
    except FileNotFoundError as e:
        logger.error(f"O arquivo contendo as variáveis de ambiente não foi encontrado. Consultar o 'README.md', seção 'FAQ', item 1 para mais informações.")
        raise e
    except Exception  as e:
        logger.error("um erro ocorreu na função load_env_file")
        raise e


def select_everything_from(table: str, connection: Any) -> list[tuple]:
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()    
        return rows
    except Exception as e:
        logger.error("erro na função 'select_everything_from'")
        raise e
##retorna os pacientes e suas doenças
def select_pacient_illness(doenca: str, paciente: str, connection: Any) -> list[tuple]:
    try:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT 
                       p.NOME,
                       d.DESCRICAO FROM {doenca} AS d 
                       JOIN {paciente} AS p ON p.CPF = d.PORTADOR""")
        rows = cursor.fetchall()    
        return rows
    except Exception as e:
        logger.error(f"erro na função 'select_pacient_illness'")
        raise e
## retorna os medicos e suas att
def select_medic_specialization(medico: str, especializacao: str, medicoespecializacao: str, profissionalsaude: str,  connection: Any) -> list[tuple]:
    try:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT 
                        ps.NOME,
                        e.NOME
                        FROM {medico} AS m JOIN {profissionalsaude} AS ps ON m.CRM = ps.CRM_MED
                        JOIN {medicoespecializacao} AS me ON m.CRM = me.CRM_MED
                        JOIN {especializacao} AS e ON e.ID = me.ID_SPEC""")
        rows = cursor.fetchall()    
        return rows
    except Exception as e:
        logger.error(f"erro na função 'select_medic_specialization'")
        raise e
    
##procura por um medico especifico, setar o db pra ser sempre maiusculo
def search_medic(name: str, medico: str, especializacao: str, medicoespecializacao: str, profissionalsaude: str,  connection: Any) -> list[tuple]:
    try:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT 
                        ps.NOME,
                        e.NOME,
                        ps.CPF
                        FROM {medico} AS m JOIN {profissionalsaude} AS ps ON m.CRM = ps.CRM_MED
                        JOIN {medicoespecializacao} AS me ON m.CRM = me.CRM_MED
                        JOIN {especializacao} AS e ON e.ID = me.ID_SPEC WHERE ps.NOME = '{name}' """)
        rows = cursor.fetchall()    
        return rows
    except Exception as e:
        logger.error(f"erro na função 'search_medic'")
        raise e
    
# retorna todos os profissionais da saude
def get_prof_saude( connection: Any):

    try:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM PROFISSIONAL_SAUDE ;""")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error("erro na função ' get_prof_saude'")
        raise e

def connect_to_database() -> Any:
    env = load_env_file()
    try:
        conn = psycopg2.connect(
            host=env['host'],
            database=env['database'],
            user=env['user'],
            password=env['password']
        )
        logger.info('connection successs')
        return conn
    except psycopg2.Error as e:
        logger.error(f'erro ao gerar conecção: {e}')


# retorna todos as salas de um dado hospital
def get_hospital_rooms(cnes: str, connection: Any):
    if len(cnes) != 7:
        raise ValueError(f"cnes deve conter 7 caracteres. cnes informad ({cnes}) possui {len(cnes)}.")

    try: int(cnes)
    except: ValueError(f"cnes deve ser exclusivamente numérico. cnes informado, {cnes}, não é.")

    try:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM SALA WHERE hospital = '{cnes}';""")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error("erro na função 'get_hospital_rooms'")
        raise e


    

if __name__ == '__main__':
    print("\x1b[31mCONSULTE OS LOGS EM CASO DE ERRO\x1b[0m")
    connection = connect_to_database()
    rows = get_hospital_rooms("0000001", connection)
    for row in rows:
        print(row)
    rows2 = select_pacient_illness("DOENCA","PACIENTE", connection)
    for row in rows2:
        print(row)
    rows3 = select_medic_specialization("MEDICO","ESPECIALIDADE","MEDICO_ESPEC", "PROFISSIONAL_SAUDE", connection)
    for row in rows3:
        print(row)
