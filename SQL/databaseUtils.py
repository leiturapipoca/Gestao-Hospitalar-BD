import psycopg2
import logging
import json
from typing import Any

logger = logging.getLogger(__name__)
logging.basicConfig(filename='program.log', level=logging.INFO)

def load_env_file() -> dict:
    """retorna as variáveis de ambiente do arquivo .env.json"""
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


def connect_to_database() -> Any:
    """cria e retorna uma connecção com o banco de dados"""

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



