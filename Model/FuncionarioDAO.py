import psycopg2

from exemplos_python.test_queries import connect_to_database 

class FuncionarioDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def autenticar(self, matr_func, senha_digitada):
        
        try:
            cursor = self.connection.cursor()
            
            sql = "SELECT * FROM FUNCINARIO WHERE MATRICULA = %s AND SENHA = %s"
            
            cursor.execute(sql, (matr_func, senha_digitada))
            resultado = cursor.fetchone() # Pega a primeira linha que achar
            cursor.close()
            

            if resultado:
                return True 
            else:
                return False 
                
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return False
            
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()