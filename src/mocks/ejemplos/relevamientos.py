import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

tabla = "relevamientos"

cur.execute(
    f"""
    INSERT INTO {tabla} (tipo, revision_id, sigla, nombre, padre_id) VALUES
        ('proceso', 3, 'MP1', 'Alta de cuentas corrientes', null),
        ('proceso', 3, 'PR1', 'Alta por red de sucursales', 1),
        ('documento', 3, null, 'Operatoria habitual', 2),
        ('documento', 3, null, 'Operatoria por contingencia', 2),
        ('proceso', 3, 'PR2', 'Alta por canales digitales', 1),
        ('documento', 3, null, 'Alta por BANCON', 5),
        ('proceso', 3, 'MP2', 'Contabilización de operaciones', null)
    """
)

con.commit()

res = cur.execute(f"SELECT * FROM {tabla}")

for row in res.fetchall():
    print(row)
