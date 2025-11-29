from SQL.databaseUtils import connect_to_database

class ProcedimentosDAO:
    def __init__(self):
        self.connection = connect_to_database()


    def select_all_procedures_names(self) -> tuple:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TIPO_PROC;")
        rows = cursor.fetchall()
        return rows
