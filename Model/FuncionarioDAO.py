import psycopg2

from exemplos_python.test_queries import connect_to_database 

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
            
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()