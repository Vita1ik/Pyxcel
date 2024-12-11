import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("table_data.db")
cursor = conn.cursor()



# Insert data

conn.commit()

# Fetch and display data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
