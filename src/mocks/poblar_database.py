import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

cur.execute(
    """
    INSERT INTO ciclos (sigla, nombre, descripcion, padre_id) VALUES
        ('DEP', 'Depósitos', 'Cuentas a la vista', null),
        ('CA', 'Caja de ahorro', 'No dan interés', 1),
        ('CC', 'Cuenta corriente', 'Podes girar en descubierto', 1),
        ('PRES', 'Préstamos', 'Plata prestada', null),
        ('CONS', 'Consumo y vivienda', 'Para la gente del pueblo', 4),
        ('PLD', 'Prevención de Lavado de Dinero', 'No vamos a permitir el lavado', null)
    """
)

con.commit()

res = cur.execute("SELECT * FROM ciclos")

for row in res.fetchall():
    print(row)
