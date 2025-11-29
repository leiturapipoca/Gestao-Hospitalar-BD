import psycopg2
from exemplos_python.test_queries import connect_to_database

class EntradaDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def register_entry(self, cpf_paciente, cnes_hospital):
        try:
            cursor = self.connection.cursor()
            
            #verifica se o paciente existe
            cursor.execute("SELECT 1 FROM PACIENTE WHERE CPF = %s", (cpf_paciente,))
            if not cursor.fetchone():
                print(f"Validação Falhou: Paciente {cpf_paciente} não encontrado.")
                return False # Retorna falso para o Controller avisar o usuário

            
            sql = """
                INSERT INTO ENTRADA (DATA, CPF_PAC, CNES_HOSP)
                VALUES (NOW(), %s, %s)
            """
            
            cursor.execute(sql, (cpf_paciente, cnes_hospital))
            
            self.connection.commit() 
            cursor.close()
            return True 
            
        except Exception as e:
            print(f"Erro ao registrar entrada: {e}")
            self.connection.rollback()
            return False

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()