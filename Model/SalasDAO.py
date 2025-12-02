import psycopg2
from exemplos_python.test_queries import connect_to_database

class SalasDAO:
    def __init__(self):
        self.connection = connect_to_database()

    def get_salas_ocupadas_by_cnes(self, cnes):
        """
        Busca salas ocupadas (LIVRE = FALSE) de um hospital específico.
        Retorna lista de tuplas: [(ID, NUMERO), ...]
        """
        lista_salas = []
        try:
            cursor = self.connection.cursor()
            # Busca ID e Numero das salas ocupadas
            sql = "SELECT ID, NUMERO FROM SALA WHERE HOSPITAL = %s AND LIVRE = FALSE ORDER BY NUMERO"
            cursor.execute(sql, (cnes,))
            rows = cursor.fetchall()
            
            for row in rows:
                # Formata como "Sala 101 (ID: 5)" para facilitar o update depois
                lista_salas.append(f"Sala {row[1]} (ID: {row[0]})")
                
            cursor.close()
        except Exception as e:
            print(f"Erro ao buscar salas ocupadas: {e}")
            
        return tuple(lista_salas)

    def liberar_sala(self, id_sala):
        """
        Atualiza o status da sala para LIVRE = TRUE.
        """
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE SALA SET LIVRE = TRUE WHERE ID = %s"
            cursor.execute(sql, (id_sala,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Erro ao liberar sala: {e}")
            return False

    def fechar_conexao(self):
        if self.connection:
            self.connection.close()