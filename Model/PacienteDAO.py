# Model/PacienteDAO.py
import calendar
from datetime import datetime
import psycopg2
from exemplos_python.test_queries import connect_to_database

# Helper (module-level) para normalizar datas flexíveis
def _normalize_date_input(s: str, is_start: bool):
    if not s:
        return None
    s = s.strip()
    # YYYY
    if len(s) == 4 and s.isdigit():
        year = int(s)
        return f"{year:04d}-01-01" if is_start else f"{year:04d}-12-31"
    # YYYY-MM
    if len(s) == 7 and s[:4].isdigit() and s[4] == '-' and s[5:7].isdigit():
        year = int(s[:4]); month = int(s[5:7])
        if 1 <= month <= 12:
            if is_start:
                return f"{year:04d}-{month:02d}-01"
            last = calendar.monthrange(year, month)[1]
            return f"{year:04d}-{month:02d}-{last:02d}"
        return None
    # YYYY-MM-DD
    try:
        dt = datetime.strptime(s, "%Y-%m-%d").date()
        return dt.isoformat()
    except Exception:
        return None

class PacienteDAO:
    def __init__(self):
        # cria conexão (connect_to_database deve estar implementado no teu projeto)
        self.connection = connect_to_database()

    # ============ Autenticação / busca básica ============
    def autenticar(self, cpf_digitado, senha_digitada):
        """
        Retorna dicionário com dados do paciente (sem senha) se ok, senão False.
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT CPF, NOME, DT_NASC, SEXO, TIPO_SANG, SENHA FROM PACIENTE WHERE CPF = %s",
                    (cpf_digitado,)
                )
                row = cur.fetchone()
            if not row:
                return False
            # Se estiver usando senhas em texto, compara diretamente. Se usar hash (bcrypt),
            # substitua por bcrypt.checkpw(...)
            stored_hash = row[5]
            # Aqui assume senha em texto plano (como seu DB atual). Ajuste se usar hash.
            if senha_digitada == stored_hash:
                return {
                    'cpf': row[0].strip() if isinstance(row[0], str) else row[0],
                    'nome': row[1],
                    'dt_nasc': row[2],
                    'sexo': row[3],
                    'tipo_sang': row[4]
                }
            return False
        except Exception as e:
            print(f"[PacienteDAO.autenticar] Erro: {e}")
            return False

    def buscar_por_cpf(self, cpf):
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT CPF, NOME, DT_NASC, SEXO, TIPO_SANG FROM PACIENTE WHERE CPF = %s", (cpf,))
                row = cur.fetchone()
            if not row:
                return None
            return {
                'cpf': row[0].strip() if isinstance(row[0], str) else row[0],
                'nome': row[1],
                'dt_nasc': row[2],
                'sexo': row[3],
                'tipo_sang': row[4]
            }
        except Exception as e:
            print(f"[PacienteDAO.buscar_por_cpf] Erro: {e}")
            return None

    # ============ Telefones CRUD ============
    def get_telefones(self, cpf):
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT NUMERO FROM TELEFONE WHERE PROPRIETARIO = %s", (cpf,))
                rows = cur.fetchall()
            return [r[0] for r in rows] if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_telefones] Erro: {e}")
            return []

    def add_telefone(self, cpf, numero):
        try:
            with self.connection.cursor() as cur:
                cur.execute("INSERT INTO TELEFONE (PROPRIETARIO, NUMERO) VALUES (%s, %s)", (cpf, numero))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[PacienteDAO.add_telefone] Erro: {e}")
            self.connection.rollback()
            return False

    def remove_telefone(self, cpf, numero):
        try:
            with self.connection.cursor() as cur:
                cur.execute("DELETE FROM TELEFONE WHERE PROPRIETARIO = %s AND NUMERO = %s", (cpf, numero))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[PacienteDAO.remove_telefone] Erro: {e}")
            self.connection.rollback()
            return False

    def update_telefone(self, cpf, old_num, new_num):
        try:
            with self.connection.cursor() as cur:
                cur.execute("UPDATE TELEFONE SET NUMERO = %s WHERE PROPRIETARIO = %s AND NUMERO = %s", (new_num, cpf, old_num))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[PacienteDAO.update_telefone] Erro: {e}")
            self.connection.rollback()
            return False

    # ============ Doenças ============
    def get_doencas(self, cpf):
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT DESCRICAO FROM DOENCA WHERE PORTADOR = %s", (cpf,))
                rows = cur.fetchall()
            return [r[0] for r in rows] if rows else []
        except Exception as e:
            print(f"[PacienteDAO.get_doencas] Erro: {e}")
            return []

    # ============ Entradas / Procedimentos com filtros flexíveis ============
    def get_entradas_detalhadas(self, cpf, limit=None, offset=None, start_date=None, end_date=None):
        try:
            start = _normalize_date_input(start_date, is_start=True)
            end = _normalize_date_input(end_date, is_start=False)

            sql = """
                SELECT e.codigo, e.data, e.cnes_hosp, COALESCE(h.nome, '') as hospital_nome, e.descricao
                FROM entrada e
                LEFT JOIN hospital h ON e.cnes_hosp = h.cnes
                WHERE e.cpf_pac = %s
            """
            params = [cpf]
            if start:
                sql += " AND e.data >= %s"
                params.append(start)
            if end:
                sql += " AND e.data <= %s"
                params.append(end)
            sql += " ORDER BY e.data DESC"
            if limit is not None:
                sql += " LIMIT %s"
                params.append(int(limit))
            if offset is not None:
                sql += " OFFSET %s"
                params.append(int(offset))

            with self.connection.cursor() as cur:
                cur.execute(sql, tuple(params))
                rows = cur.fetchall()
                cols = [c[0].lower() for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        except Exception as e:
            print(f"[PacienteDAO.get_entradas_detalhadas] Erro: {e}")
            return []

    def get_procedimentos_detalhados(self, cpf, limit=None, offset=None, start_date=None, end_date=None):
        try:
            start = _normalize_date_input(start_date, is_start=True)
            end = _normalize_date_input(end_date, is_start=False)

            sql = """
                SELECT pr.codigo, tp.nome as tipo_nome, pr.cod_entr, e.data, COALESCE(h.nome, '') as hospital_nome
                FROM procedimento pr
                JOIN tipo_proc tp ON pr.id_tipo = tp.id
                JOIN entrada e ON pr.cod_entr = e.codigo
                LEFT JOIN hospital h ON e.cnes_hosp = h.cnes
                WHERE e.cpf_pac = %s
            """
            params = [cpf]
            if start:
                sql += " AND e.data >= %s"
                params.append(start)
            if end:
                sql += " AND e.data <= %s"
                params.append(end)
            sql += " ORDER BY e.data DESC"
            if limit is not None:
                sql += " LIMIT %s"
                params.append(int(limit))
            if offset is not None:
                sql += " OFFSET %s"
                params.append(int(offset))

            with self.connection.cursor() as cur:
                cur.execute(sql, tuple(params))
                rows = cur.fetchall()
                cols = [c[0].lower() for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        except Exception as e:
            print(f"[PacienteDAO.get_procedimentos_detalhados] Erro: {e}")
            return []
    def cadastrar(self, nome: str,data_nasc: str, sexo: str, cpf: str,tipo_sang: str, senha: str ):
        data_nasc = data_nasc.replace("/","-")
        cursor = self.connection.cursor()
        
        cursor.execute(f"""INSERT INTO PACIENTE (CPF, NOME, SEXO, DT_NASC, TIPO_SANG, SENHA) VALUES
                       ('{cpf}','{nome}','{sexo}','{data_nasc}','{tipo_sang}','{senha}');
                       
                       """)
        self.connection.commit()


    def remover(self, cpf: str):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM PACIENTE WHERE CPF = '{cpf}'")
        self.connection.commit()
        

    # ============ fechar conexão ============
    def fechar_conexao(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"[PacienteDAO.fechar_conexao] Erro: {e}")
