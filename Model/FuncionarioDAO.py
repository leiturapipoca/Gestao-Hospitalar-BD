import psycopg2
import logging

from exemplos_python.test_queries import connect_to_database 

logger = logging.getLogger("FuncionarioDAO")

class FuncionarioDAO:
    def __init__(self):
        self.connection = connect_to_database()
    
    # Pega o nome baseado no login e na senha
    def autenticar(self, login_digitado, senha_digitada):        
        """
        Busca o funcionário pelo CPF ou MATRICULA.
        Retorna o dicionário com a MATRICULA correta para uso interno.
        """
        try:
            cursor = self.connection.cursor()
            
            # Vamos tentar achar por CPF primeiro (é o mais comum)
            # Selecionamos a MATRICULA (ID) e o NOME
            sql = "SELECT MATRICULA, NOME FROM FUNCINARIO WHERE CPF = %s AND SENHA = %s"
            
            cursor.execute(sql, (login_digitado, senha_digitada))
            resultado = cursor.fetchone() 
            cursor.close()
            
            if resultado:
                # O PULO DO GATO:
                # O usuário digitou o CPF (login_digitado), 
                # mas nós retornamos a MATRICULA (resultado[0]) vinda do banco.
                return {
                    "matricula": resultado[0], # O ID Real (ex: 1)
                    "nome": resultado[1]       # O Nome (ex: Carlos)
                }
            else:
                return None 
                
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return None
            

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

    def update_funcionario(self, matricula, novo_nome, nova_senha):
        """Atualiza dados textuais"""
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE FUNCINARIO SET NOME = %s, SENHA = %s WHERE MATRICULA = %s"
            cursor.execute(sql, (novo_nome, nova_senha, matricula))
            self.connection.commit()
            cursor.close()
            return True, "Perfil atualizado com sucesso!"
        except Exception as e:
            self.connection.rollback()
            return False, f"Erro ao atualizar: {e}"

    def salvar_foto(self, matricula, caminho_arquivo):
        """
        Lê o arquivo do disco (RB = Read Binary) e salva no banco (BYTEA).
        """
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                dados_binarios = arquivo.read()

            cursor = self.connection.cursor()
            sql = "UPDATE FUNCINARIO SET FOTO = %s WHERE MATRICULA = %s"
            cursor.execute(sql, (dados_binarios, matricula))
            self.connection.commit()
            cursor.close()
            return True, "Foto enviada com sucesso!"
        except Exception as e:
            self.connection.rollback()
            return False, f"Erro ao salvar foto: {e}"

  
        
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
