import psycopg2
from exemplos_python.test_queries import connect_to_database

class ProcedimentosDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def get_tipos_procedimento(self):
        """Busca nomes para o combobox"""
        lista = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT NOME FROM TIPO_PROC ORDER BY NOME")
            for row in cursor.fetchall():
                lista.append(row[0])
            cursor.close()
        except Exception as e:
            print(f"Erro ao buscar tipos: {e}")
        return tuple(lista)

    def registrar_procedimento_completo(self, cod_entrada, crm, procedimento, doenca):
        """
        Chama a procedure que salva Procedimento, Médico e Doença de uma vez.
        """
        try:
            cursor = self.connection.cursor()
            
            sql = "CALL PR_REGISTRAR_PROCEDIMENTO_COMPLETO(%s, %s, %s, %s)"
            cursor.execute(sql, (cod_entrada, crm, procedimento, doenca))
            
            self.connection.commit()
            cursor.close()
            return True, "Sucesso"
            
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            # Retorna o erro específico do banco (ex: Médico não encontrado)
            return False, f"Erro de Banco: {e.pgerror}"
            
        except Exception as e:
            self.connection.rollback()
            return False, f"Erro inesperado: {e}"

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()