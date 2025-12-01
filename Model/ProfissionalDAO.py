import psycopg2
import logging

from exemplos_python.test_queries import connect_to_database 

logger = logging.getLogger("ProfissionalDAO")

class ProfissionalDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def autenticar(self, cpf_digitado, senha_digitada):
        
        try:
            cursor = self.connection.cursor()
            
            sql = "SELECT NOME FROM PROFISSIONAL_SAUDE WHERE CPF = %s AND SENHA = %s"
            
            cursor.execute(sql, (cpf_digitado, senha_digitada))
            resultado = cursor.fetchone() # Pega a primeira linha que achar
            cursor.close()
            

            if resultado:
                return resultado[0]
            else:
                return False 
                
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return False

    def add_profissional(self, cpf: str, nome: str, tipo: str, crm: str | None = None, codigo: int | None = None) -> tuple[bool, str]:
        """
        Adiciona um novo profissional de saúde ao sistema.
        
        Args:
            cpf: CPF do profissional (11 caracteres)
            nome: Nome completo do profissional
            tipo: Tipo do profissional ('M' para Médico, 'E' para Enfermeiro)
            crm: CRM do médico (obrigatório se tipo='M')
            codigo: Código do enfermeiro (opcional, será auto-gerado se tipo='E')
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            cursor = self.connection.cursor()
            
            # Variáveis para armazenar as chaves estrangeiras
            crm_med = None
            cod_enf = None
            
            if tipo == 'M':
                # Inserir registro na tabela MEDICO
                if not crm:
                    return False, "Erro: CRM é obrigatório para médicos."
                
                sql_medico = "INSERT INTO MEDICO (CRM) VALUES (%s)"
                cursor.execute(sql_medico, (crm,))
                crm_med = crm
                logger.info(f"Médico com CRM {crm} inserido na tabela MEDICO")
                
            elif tipo == 'E':
                # Inserir registro na tabela ENFERMEIRO (CODIGO é SERIAL, auto-gerado)
                sql_enfermeiro = "INSERT INTO ENFERMEIRO (CODIGO) VALUES (DEFAULT) RETURNING CODIGO"
                cursor.execute(sql_enfermeiro)
                cod_enf = cursor.fetchone()[0]
                logger.info(f"Enfermeiro com CODIGO {cod_enf} inserido na tabela ENFERMEIRO")
                
            else:
                return False, f"Erro: Tipo '{tipo}' inválido. Use 'M' para Médico ou 'E' para Enfermeiro."
            
            # Inserir registro na tabela PROFISSIONAL_SAUDE
            sql_profissional = """
                INSERT INTO PROFISSIONAL_SAUDE (CPF, NOME, TIPO, CRM_MED, COD_ENF)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_profissional, (cpf, nome, tipo, crm_med, cod_enf))
            
            # Commit da transação
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Profissional {nome} (CPF: {cpf}) cadastrado com sucesso")
            return True, "Profissional de saúde cadastrado com sucesso!"
            
        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            logger.warning(f"Tentativa de cadastrar CPF duplicado: {cpf}")
            return False, f"Erro: O CPF {cpf} já está cadastrado no sistema."
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Erro ao adicionar profissional: {e}")
            return False, f"Erro ao cadastrar profissional: {str(e)}"
            
    def remove_profissional(self, cpf: str) -> tuple[bool, str]:
        """
        Remove um profissional de saúde do sistema.
        
        Args:
            cpf: CPF do profissional a ser removido (11 caracteres)
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            cursor = self.connection.cursor()
            
            # Verificar se o profissional existe
            sql_check = "SELECT NOME, TIPO FROM PROFISSIONAL_SAUDE WHERE CPF = %s"
            cursor.execute(sql_check, (cpf,))
            resultado = cursor.fetchone()
            
            if not resultado:
                cursor.close()
                logger.warning(f"Tentativa de remover profissional inexistente: CPF {cpf}")
                return False, f"Erro: Profissional com CPF {cpf} não encontrado no sistema."
            
            nome_profissional = resultado[0]
            tipo_profissional = resultado[1]
            
            logger.info(f"Iniciando remoção do profissional {nome_profissional} (CPF: {cpf}, Tipo: {tipo_profissional})")
            
            # Deletar registros da tabela PROF_PROC (relacionamento com procedimentos)
            sql_delete_prof_proc = "DELETE FROM PROF_PROC WHERE COD_PROF = %s"
            cursor.execute(sql_delete_prof_proc, (cpf,))
            logger.info(f"Registros de PROF_PROC removidos para CPF {cpf}")
            
            # Deletar registros da tabela PROF_SAUDE_HOSP (relacionamento com hospitais)
            sql_delete_prof_hosp = "DELETE FROM PROF_SAUDE_HOSP WHERE CPF_PROF = %s"
            cursor.execute(sql_delete_prof_hosp, (cpf,))
            logger.info(f"Registros de PROF_SAUDE_HOSP removidos para CPF {cpf}")
            
            # Deletar o profissional da tabela PROFISSIONAL_SAUDE
            # O ON DELETE SET NULL nas referências MEDICO/ENFERMEIRO será tratado automaticamente
            sql_delete_profissional = "DELETE FROM PROFISSIONAL_SAUDE WHERE CPF = %s"
            cursor.execute(sql_delete_profissional, (cpf,))
            logger.info(f"Profissional removido da tabela PROFISSIONAL_SAUDE: CPF {cpf}")
            
            # Commit da transação
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Profissional {nome_profissional} (CPF: {cpf}) removido com sucesso")
            return True, f"Profissional {nome_profissional} removido com sucesso!"
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Erro ao remover profissional com CPF {cpf}: {e}")
            return False, f"Erro ao remover profissional: {str(e)}"
            
    def consultar_profissional(self, cpf: str) -> dict | None:
        """
        Consulta informações de um profissional de saúde pelo CPF.
        
        Args:
            cpf: CPF do profissional a ser consultado (11 caracteres)
            
        Returns:
            dict | None: Dicionário com dados do profissional ou None se não encontrado
                        Chaves: 'cpf', 'nome', 'tipo', 'crm' (se tipo='M'), 'codigo' (se tipo='E')
        """
        try:
            cursor = self.connection.cursor()
            
            # Query para buscar o profissional
            sql = """
                SELECT CPF, NOME, TIPO, CRM_MED, COD_ENF
                FROM PROFISSIONAL_SAUDE
                WHERE CPF = %s
            """
            cursor.execute(sql, (cpf,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if not resultado:
                logger.info(f"Profissional com CPF {cpf} não encontrado")
                return None
            
            # Extrair dados do resultado
            cpf_prof, nome, tipo, crm_med, cod_enf = resultado
            
            # Montar dicionário de retorno
            dados_profissional = {
                'cpf': cpf_prof,
                'nome': nome,
                'tipo': tipo
            }
            
            # Adicionar CRM ou CODIGO dependendo do tipo
            if tipo == 'M' and crm_med:
                dados_profissional['crm'] = crm_med
            elif tipo == 'E' and cod_enf:
                dados_profissional['codigo'] = cod_enf
            
            logger.info(f"Profissional {nome} (CPF: {cpf}) consultado com sucesso")
            return dados_profissional
            
        except Exception as e:
            logger.error(f"Erro ao consultar profissional com CPF {cpf}: {e}")
            return None
    
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
