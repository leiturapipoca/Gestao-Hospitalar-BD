import psycopg2
from exemplos_python.test_queries import connect_to_database

class EntradaDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def registrar_entrada(self, cpf_paciente, cnes_hospital, entry_desc):
        """
        Insere a entrada e RETORNA O ID GERADO.
        Retorna o ID (int) se sucesso, ou None se falha.
        """
        try:
            cursor = self.connection.cursor()
            
            # 1. Validação simples: Paciente existe?
            cursor.execute("SELECT 1 FROM PACIENTE WHERE CPF = %s", (cpf_paciente,))
            if not cursor.fetchone():
                print(f"Paciente {cpf_paciente} não encontrado.")
                return None 

            # 2. INSERT com RETURNING para pegar o ID automático (Serial)
            sql = """
                INSERT INTO ENTRADA (DATA, CPF_PAC, CNES_HOSP, DESCRICAO)
                VALUES (NOW(), %s, %s, %s)
                RETURNING CODIGO
            """
            
            cursor.execute(sql, (cpf_paciente, cnes_hospital, entry_desc))
            
            # Pega o ID gerado (O Pulo do Gato)
            id_gerado = cursor.fetchone()[0]
            
            self.connection.commit() 
            cursor.close()
            
            return id_gerado # Retorna o número (Ex: 5)
            
        except Exception as e:
            print(f"Erro ao registrar entrada: {e}")
            self.connection.rollback()
            return None

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()