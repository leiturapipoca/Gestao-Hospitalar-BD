import psycopg2
import logging

from exemplos_python.test_queries import connect_to_database 

logger = logging.getLogger("FuncionarioDAO")

class FuncionarioDAO:
    def __init__(self):
        self.connection = connect_to_database()
    
    # Pega o nome baseado no login e na senha
    def autenticar(self, matr_func, senha_digitada):        
        try:
            cursor = self.connection.cursor()
            sql = "SELECT NOME FROM FUNCINARIO WHERE MATRICULA = %s AND SENHA = %s"
            cursor.execute(sql, (matr_func, senha_digitada))
            resultado = cursor.fetchone() # Pega a primeira linha que achar
            cursor.close()
            if resultado:
                return {
                    "matricula": matr_func,  # O número inteiro (1, 2, 3...)
                    "nome": resultado[0]     # O nome (Carlos Func)
                }
            else:
                return False 
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return False
            

    def add_funcionario(self, nome: str, cpf: str, cargo_id: int, senha: str):
        cursor = self.connection.cursor()
        cursor.execute(f"""
                           INSERT INTO FUNCINARIO (NOME,CPF, FUNC, SENHA)
                           VALUES ('{nome}','{cpf}', {cargo_id}, '{senha}');
                       """)
        self.connection.commit()
    

    def remove_funcionario(self, cpf: str):
        logger.info("entrou-se na query de remove funcionario")
        cursor = self.connection.cursor()
        cursor.execute(f"""
                       SELECT MATRICULA FROM FUNCINARIO WHERE CPF = '{cpf}';""")
        func_id = cursor.fetchall()[0][0]
        logger.info(f"matricula do funcionário a ser removido: {func_id}")
        logger.info(f"tipo da variável matrícula: {type(func_id)}")
        cursor.execute(f"""
             DELETE FROM FUNC_HOSP WHERE MATR_FUNC = {func_id};
        """)
        cursor.execute(f"""DELETE FROM FUNCINARIO WHERE CPF = '{cpf}';""")
        self.connection.commit()
        logger.info(f"concluiu-se a query de remover funcionario: {type(func_id)}")


    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
