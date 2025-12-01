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
            

    def add_funcionario(self, nome: str, cpf: str, cargo_id: int, senha: str, cnes_hospital: str):
        """
        Cadastra o funcionário e cria o vínculo com o hospital.
        """
        try:
            cursor = self.connection.cursor()
            
            # 1. Inserir Funcionário e recuperar a Matrícula gerada
            sql_func = """
                INSERT INTO FUNCINARIO (NOME, CPF, FUNC, SENHA)
                VALUES (%s, %s, %s, %s)
                RETURNING MATRICULA
            """
            cursor.execute(sql_func, (nome, cpf, cargo_id, senha))
            
            # Pega o ID gerado (ex: 5)
            nova_matricula = cursor.fetchone()[0]
            
            # 2. Criar o vínculo na tabela FUNC_HOSP
            if cnes_hospital:
                sql_vinculo = """
                    INSERT INTO FUNC_HOSP (CNES_HOSP, MATR_FUNC)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_vinculo, (cnes_hospital, nova_matricula))
            
            self.connection.commit()
            cursor.close()
            return True, "Funcionário cadastrado e vinculado com sucesso!"

        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            return False, f"Erro: O CPF {cpf} já está cadastrado."
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao cadastrar: {e}")
            return False, f"Erro inesperado: {e}"
        

    def get_func_by_cpf(self, cpf: str):
        logger.info("entrou na função get_func_by_cpf")
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT * FROM FUNC_COMPLETO WHERE CPF = '{cpf}';
        """)
        rows: list[tuple] = cursor.fetchall()
        if len(rows) < 1:
            raise ValueError("não encontrou nenhum cpf correspondente")
        rows = [{'cpf': row[0], 'nome': row[1], 'matricula': row[2], 'funcao_nome': row[3]} for row in rows][0]
        logger.info(f"rows geradas pelo select: {rows}")
        logger.info(f"tipo da variável rows: {rows}")
        return rows
        

    def get_func_by_nome(self, nome: str):
        logger.info("entrou na função get_func_by_nome")
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT * FROM FUNC_COMPLETO WHERE NOME LIKE '{nome}%';
        """)
        rows: list[tuple] = cursor.fetchall()
        if len(rows) > 1:
            raise NameError("existe mais de uma correspondência para esse nome")
        if len(rows) < 1:
            raise ValueError("não encontrou nenhum nome correspondente")
        rows = [{'cpf': row[0], 'nome': row[1], 'matricula': row[2], 'funcao_nome': row[3]} for row in rows][0]
        logger.info(f"rows geradas pelo select: {rows}")
        logger.info(f"tipo da variável rows: {rows}")
        return rows
        

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

  
    def get_foto_by_cpf(self, cpf):
        """
        Busca os dados binários da foto de um funcionário pelo CPF.
        Retorna: bytes ou None
        """
        try:
            cursor = self.connection.cursor()
            # Busca a FOTO onde o CPF bate
            sql = "SELECT FOTO FROM FUNCINARIO WHERE CPF = %s"
            cursor.execute(sql, (cpf,))
            row = cursor.fetchone()
            cursor.close()
            
            if row and row[0]:
                return row[0] # Retorna os bytes da imagem
            return None
        except Exception as e:
            print(f"Erro ao buscar foto: {e}")
            return None


    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
