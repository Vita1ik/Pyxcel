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
                row_dict = cls.__row_to_dict(row)
                result.append(row_dict)

            return result

    @classmethod
    def where(cls, addresses):
        with cls.db_connection() as connection:
            placeholders = ', '.join('?' for _ in addresses)
            select_query = f"SELECT address, row, column, data, text FROM cells WHERE address IN ({placeholders});"

            cursor = connection.cursor()

            # Pass the addresses as a tuple (this unpacks the list correctly)
            cursor.execute(select_query, tuple(addresses))

            # Fetch the results
            rows = cursor.fetchall()

            result = []
            for row in rows:
                row_dict = cls.__row_to_dict(row)
                result.append(row_dict)

            return result

    @classmethod
    def update(cls, data):
        with cls.db_connection() as connection:
            cursor = connection.cursor()
            update_query = '''
                UPDATE Cells
                SET data = ?, text = ?
                WHERE address = ?;
            '''
            cursor.execute(update_query, data)
            connection.commit()
        print(data[-1])
        cls.__update_callback(data[-1])

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

    @classmethod
    def __update_callback(cls, address):
        from modules.expression_evaluator import ExpressionEvaluator
        with cls.db_connection() as connection:
            cursor = connection.cursor()
            select_query = f"SELECT address, data FROM cells WHERE data LIKE ?;"
            cursor.execute(select_query, (f'%{address}%',))
            data = [(ExpressionEvaluator(row[0]).evaluate(row[1]), row[0]) for row in cursor.fetchall()]

        if len(data) > 0:
            with cls.db_connection() as connection:
                cursor = connection.cursor()
                print('update_query', data)
                update_query = '''
                    UPDATE Cells
                    SET text = ?
                    WHERE address = ?;
                '''
                res = cursor.executemany(update_query, data)
                print(res)
                print(connection.commit())
                print(cls.where(['F2']))


    @classmethod
    def __row_to_dict(cls, row):
        row_dict = {
            'address': row[0],
            'row': row[1],
            'column': row[2],
            'data': row[3],
            'text': row[4]
        }
        return row_dict
