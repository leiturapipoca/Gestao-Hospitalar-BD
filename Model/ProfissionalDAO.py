import psycopg2

from exemplos_python.test_queries import connect_to_database 

class ProfissionalDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def autenticar(self, cpf_digitado, senha_digitada):
        
        try:
            cursor = self.connection.cursor()
            
            sql = "SELECT NOME FROM PROFISSIONAL_SAUDE WHERE CPF = %s AND SENHA = %s"
            
            cursor.execute(sql, (cpf_digitado, senha_digitada))
            resultado = cursor.fetchone() # Pega a primeira linha que achar
            cursor.close()
            

            if resultado:
                return resultado[0]
            else:
                return False 
                
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return False
            
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()