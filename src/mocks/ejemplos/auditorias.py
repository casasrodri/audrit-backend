import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

tabla = "auditorias"

cur.execute(
    f"""
    INSERT INTO {tabla} (sigla, nombre, tipo, estado, periodo) VALUES
        ('2023', 'Plan anual 2023', 'anual', 'finalizada', '01/01/2023 - 31/12/2023'),
        ('2024', 'Plan anual 2024', 'anual', 'iniciada', '01/01/2024 - 31/12/2024'),
        ('LIP-202402', 'Revisión especial LIP 2do semestre 2024', 'especial', 'iniciada', '01/07/2024 - 31/12/2024')
    """
)

con.commit()

res = cur.execute(f"SELECT * FROM {tabla}")

for row in res.fetchall():
    print(row)
