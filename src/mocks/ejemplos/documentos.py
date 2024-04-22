import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

tabla = "documentos"

cur.execute(
    f"""
    INSERT INTO {tabla} (relevamiento_id, contenido) VALUES
        (3, '{{\"mensaje":"Hola mundo!\"}}')
    """
)

con.commit()

res = cur.execute(f"SELECT * FROM {tabla}")

for row in res.fetchall():
    print(row)
