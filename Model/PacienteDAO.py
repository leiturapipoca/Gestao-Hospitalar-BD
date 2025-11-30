# Model/PacienteDAO.py
import psycopg2
from exemplos_python.test_queries import connect_to_database

class PacienteDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def autenticar(self, cpf_digitado, senha_digitada):
        """
        Tenta autenticar paciente. Se ok retorna um dicionário com os dados básicos do paciente:
        { 'cpf':..., 'nome':..., 'dt_nasc':..., 'sexo':..., 'tipo_sang':... }
        Se não autenticou, retorna False.
        """
        try:
            cursor = self.connection.cursor()
            sql = """
                SELECT CPF, NOME, DT_NASC, SEXO, TIPO_SANG
                FROM PACIENTE
                WHERE CPF = %s AND SENHA = %s
            """
            cursor.execute(sql, (cpf_digitado, senha_digitada))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return {
                    'cpf': row[0].strip() if isinstance(row[0], str) else row[0],
                    'nome': row[1],
                    'dt_nasc': row[2],
                    'sexo': row[3],
                    'tipo_sang': row[4]
                }
            else:
                return False
        except Exception as e:
            print(f"[PacienteDAO.autenticar] Erro ao autenticar: {e}")
            return False

    def get_telefones(self, cpf):
        """
        Retorna lista de strings (números) do paciente.
        """
        try:
            cursor = self.connection.cursor()
            sql = "SELECT NUMERO FROM TELEFONE WHERE PROPRIETARIO = %s"
            cursor.execute(sql, (cpf,))
            rows = cursor.fetchall()
            cursor.close()
            return [r[0] for r in rows] if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_telefones] Erro: {e}")
            return []

    def get_doencas(self, cpf):
        """
        Retorna lista de descrições de doenças registradas para o paciente.
        """
        try:
            cursor = self.connection.cursor()
            sql = "SELECT DESCRICAO FROM DOENCA WHERE PORTADOR = %s"
            cursor.execute(sql, (cpf,))
            rows = cursor.fetchall()
            cursor.close()
            return [r[0] for r in rows] if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_doencas] Erro: {e}")
            return []

    def get_entradas(self, cpf):
        """
        Retorna lista de entradas/admissões do paciente.
        Cada item: (codigo, data, cnes_hosp, descricao)
        Ordena por data desc.
        """
        try:
            cursor = self.connection.cursor()
            sql = """
                SELECT CODIGO, DATA, CNES_HOSP, DESCRICAO
                FROM ENTRADA
                WHERE CPF_PAC = %s
                ORDER BY DATA DESC
            """
            cursor.execute(sql, (cpf,))
            rows = cursor.fetchall()
            cursor.close()
            return rows if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_entradas] Erro: {e}")
            return []

    def get_procedimentos_por_cpf(self, cpf):
        """
        Retorna procedimentos/exames associados ao paciente.
        Cada item: (procedimento_codigo, nome_tipo_proc, codigo_entrada, data_entrada, hospital_cnes)
        Faz join PROCEDIMENTO -> TIPO_PROC -> ENTRADA (filtrando por CPF_PAC).
        """
        try:
            cursor = self.connection.cursor()
            sql = """
                SELECT pr.codigo, tp.nome, pr.cod_entr, e.data, e.cnes_hosp
                FROM procedimento pr
                JOIN tipo_proc tp ON pr.id_tipo = tp.id
                JOIN entrada e ON pr.cod_entr = e.codigo
                WHERE e.cpf_pac = %s
                ORDER BY e.data DESC
            """
            cursor.execute(sql, (cpf,))
            rows = cursor.fetchall()
            cursor.close()
            return rows if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_procedimentos_por_cpf] Erro: {e}")
            return []

    def remover(self, cpf):
        """
        Retorna procedimentos/exames associados ao paciente.
        Cada item: (procedimento_codigo, nome_tipo_proc, codigo_entrada, data_entrada, hospital_cnes)
        Faz join PROCEDIMENTO -> TIPO_PROC -> ENTRADA (filtrando por CPF_PAC).
        """
        try:
            cursor = self.connection.cursor()
            sql = f"""
                DELETE FROM PACIENTE WHERE PACIENTE.CPF = '{cpf}';
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows if rows else []
        except Exception as e:
            print(f"[remover] Erro: {e}")
            
    
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
