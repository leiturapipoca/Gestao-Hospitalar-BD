import psycopg2
from exemplos_python.test_queries import connect_to_database

class ProcedimentosDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def get_tipos_procedimento(self):
        """
        Busca os nomes dos procedimentos na tabela TIPO_PROC para preencher o Combobox.
        """
        lista = []
        try:
            cursor = self.connection.cursor()
            # Busca todos os tipos ordenados por nome
            cursor.execute("SELECT NOME FROM TIPO_PROC ORDER BY NOME")
            
            # Transforma a lista de tuplas em uma lista simples de strings
            for row in cursor.fetchall():
                lista.append(row[0])
                
            cursor.close()
        except Exception as e:
            print(f"Erro ao buscar tipos de procedimento: {e}")
            
        return tuple(lista) # Retorna uma tupla para o Tkinter usar

    def get_medicos_disponiveis(self, cnes_filtro=None):
        """
        Busca CRMs e Nomes dos médicos.
        Se receber 'cnes_filtro', traz apenas os médicos daquele hospital.
        """
        lista_medicos = []
        try:
            cursor = self.connection.cursor()
            
            sql = """
                SELECT M.CRM, P.NOME 
                FROM MEDICO M
                JOIN PROFISSIONAL_SAUDE P ON M.CRM = P.CRM_MED
            """
            
            # Se tiver filtro, fazemos o JOIN com a tabela de vínculo
            if cnes_filtro:
                sql += """
                    JOIN PROF_SAUDE_HOSP PSH ON P.CPF = PSH.CPF_PROF
                    WHERE PSH.CNES_HOSP = %s
                """
                sql += " ORDER BY P.NOME"
                cursor.execute(sql, (cnes_filtro,))
            else:
                sql += " ORDER BY P.NOME"
                cursor.execute(sql)
            
            for row in cursor.fetchall():
                lista_medicos.append(f"{row[0]} - {row[1]}")
            
            cursor.close()
        except Exception as e:
            print(f"Erro ao buscar médicos: {e}")
        return tuple(lista_medicos)

    def registrar_procedimento_completo(self, cod_entrada, crm_medico, procedimento, nome_doenca, num_sala):
        """
        Chama a procedure com o novo parâmetro de sala.
        """
        try:
            cursor = self.connection.cursor()
            
            # Adicionamos mais um %s::INT para a sala
            sql = "CALL PR_REGISTRAR_PROCEDIMENTO_COMPLETO(%s::INT, %s::CHAR(9), %s::TEXT, %s::TEXT, %s::INT)"
            
            cursor.execute(sql, (cod_entrada, crm_medico, procedimento, nome_doenca, num_sala))
            
            self.connection.commit()
            cursor.close()
            return True, "Procedimento registrado com sucesso!"
            
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            erro_msg = e.pgerror if e.pgerror else str(e)
            return False, f"Erro de Banco: {erro_msg}"
        except Exception as e:
            self.connection.rollback()
            return False, f"Erro inesperado: {e}"

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()