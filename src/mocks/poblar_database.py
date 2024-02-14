import sqlite3

con = sqlite3.connect(r"audrit.sqlite")
cur = con.cursor()

cur.execute(
    """
    INSERT INTO ciclos (sigla, sigla_extendida, nombre, descripcion, padre_id) VALUES
        ('DEP', 'DEP', 'Depósitos', 'Cuentas a la vista', null),
        ('CA', 'DEP-CA', 'Caja de ahorro', 'No dan interés', 1),
        ('CC', 'DEP-CC', 'Cuenta corriente', 'Podes girar en descubierto', 1),
        ('PRES', 'PRES', 'Préstamos', 'Plata prestada', null),
        ('CONS', 'PRES-CONS', 'Consumo y vivienda', 'Para la gente del pueblo', 4),
        ('PLD', 'PLD', 'Prevención de Lavado de Dinero', 'No vamos a permitir el lavado', null)
    """
)

con.commit()

res = cur.execute("SELECT * FROM ciclos")

for row in res.fetchall():
    print(row)
