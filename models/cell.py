import sqlite3
from contextlib import contextmanager

class Cell:
    DB_NAME = 'db/database.db'
    
    @classmethod
    def all(cls):
        with cls.db_connection() as connection:
            select_query = "SELECT address, row, column, data, text FROM cells;"
            cursor = connection.cursor()
            cursor.execute(select_query)

            rows = cursor.fetchall()

            result = []
            for row in rows:
                row_dict = {
                    'address': row[0],
                    'row': row[1],
                    'column': row[2],
                    'data': row[3],
                    'text': row[4]
                }
                result.append(row_dict)

            return result

    @classmethod
    def update_all(cls, data):
        with cls.db_connection() as connection:
            cursor = connection.cursor()
            update_query = '''
                UPDATE Cells
                SET data = ?, text = ?
                WHERE address = ?;
            '''
            cursor.executemany(update_query, data)
            connection.commit()

    @classmethod
    @contextmanager
    def db_connection(cls):
        connection = sqlite3.connect(cls.DB_NAME)
        try:
            yield connection
        finally:
            connection.close()
