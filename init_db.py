import duckdb

conn = duckdb.connect("my_database.db")

with open("init_db.sql", "r") as file:
    sql_script = file.read()

conn.execute(sql_script)

conn.close()
