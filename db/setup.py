import sqlite3

# Name of the SQLite database
db_name = 'db/database.db'

# Connect to the SQLite database (it will create the file if it doesn't exist)
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS cells (
    address TEXT NOT NULL PRIMARY KEY,
    row INTEGER NOT NULL,
    column INTEGER NOT NULL,
    data TEXT,
    text TEXT
);
'''
cursor.execute(create_table_query)

for row_index, row in enumerate(range(1, 101)):
    for col_index, col in enumerate(range(ord('A'), ord('Z') + 1)):
        cursor.execute("""
            INSERT INTO cells (address, row, column, data, text) VALUES (?, ?, ?, ?, ?)
        """, (f'{chr(col)}{row}', row_index, col_index, None, ''))
connection.commit()
connection.close()
