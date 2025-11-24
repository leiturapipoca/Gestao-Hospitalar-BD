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
        logger.error(f"erro na função 'select_everything_from'")
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


if __name__ == '__main__':
    print("\x1b[31mCONSULTE OS LOGS EM CASO DE ERRO\x1b[0m")
    connection = connect_to_database()
    rows = select_everything_from("hospital", connection)
    for row in rows:
        print(row)

