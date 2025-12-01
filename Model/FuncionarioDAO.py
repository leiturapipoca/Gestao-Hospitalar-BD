import psycopg2

from exemplos_python.test_queries import connect_to_database 

class FuncionarioDAO:
    def __init__(self):
        self.connection = connect_to_database()
    
    # Pega o nome baseado no login e na senha
    def autenticar(self, matr_func, senha_digitada):        
        try:
            cursor = self.connection.cursor()
            sql = "SELECT NOME FROM FUNCINARIO WHERE CPF = %s AND SENHA = %s"
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
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                           INSERT INTO FUNCINARIO (NOME,CPF, FUNC, SENHA)
                           VALUES ('{nome}','{cpf}', {cargo_id}, '{senha}');
                       """)
            self.connection.commit()
            return True, "Funcionário cadastrado com sucesso!"

        except psycopg2.errors.UniqueViolation:
            self.connection.rollback() # Cancela a tentativa
            return False, f"Erro: O CPF {cpf} já está cadastrado no sistema."


    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
