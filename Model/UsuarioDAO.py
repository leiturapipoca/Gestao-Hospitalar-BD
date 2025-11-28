import psycopg2
#
from exemplos_python.test_queries import connect_to_database 

class UsuarioDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def autenticar(self, id_usuario, senha_digitada):
        
        try:
            cursor = self.connection.cursor()
            
            sql = "SELECT * FROM USUARIO WHERE ID = %s AND SENHA = %s"
            
            cursor.execute(sql, (id_usuario, senha_digitada))
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