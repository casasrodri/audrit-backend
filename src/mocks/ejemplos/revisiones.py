import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

tabla = "revisiones"

cur.execute(
    f"""
    INSERT INTO {tabla} (auditoria_id, sigla, nombre, descripcion, padre_id, estado, informe) VALUES
        (2, 'DEP', 'Depósitos', 'Cuentas a la vista', null, 'iniciada', null),
        (2, 'CA', 'Caja de ahorro', 'No dan interés', 1, 'pendiente', null),
        (2, 'CC', 'Cuenta corriente', 'Podes girar en descubierto', 1, 'iniciada', null),
        (2, 'PRES', 'Préstamos', 'Plata prestada', null, 'pendiente', null),
        (2, 'CONS', 'Consumo y vivienda', 'Para la gente del pueblo', 4, 'iniciada', null),
        (2, 'PLD', 'Prevención de Lavado de Dinero', 'No vamos a permitir el lavado', null, 'finalizada', null)
    """
)

con.commit()

res = cur.execute(f"SELECT * FROM {tabla}")

for row in res.fetchall():
    print(row)
