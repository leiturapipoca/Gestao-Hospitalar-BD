
from SQL import databaseUtils
from typing import Any
import logging

test_logger = logging.getLogger("FuncaoDAO TEST")

class FuncaoDao:
    def __init__(self):
        self.connection = databaseUtils.connect_to_database()

    def get_all_funcoes(self) -> list[tuple]:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM FUNCAO; """)
        return cursor.fetchall();



def run_funcao_dao_tests():
    """roda testes verificando o correto funcionamento das queries presentes no FuncaoDAO"""
    dao = FuncaoDao()
    test_logger.info(f"get_all_funcoes: {dao.get_all_funcoes()}", )
