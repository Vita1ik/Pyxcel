import sqlite3

db_name = 'db/database.db'
connection = sqlite3.connect(db_name)
cursor = connection.cursor()
for row_index, row in enumerate(range(1, 101)):
    for col_index, col in enumerate(range(ord('A'), ord('Z') + 1)):
        cursor.execute("""
            INSERT INTO cells (address, row, column, data, text) VALUES (?, ?, ?, ?, ?)
        """, (f'{chr(col)}{row}', row_index, col_index, None, ''))
connection.commit()
connection.close()