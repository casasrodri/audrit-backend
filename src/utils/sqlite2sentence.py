import sqlite3


def get_schema_and_data(database_path):
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Obtener la estructura de la base de datos
    cursor.execute(
        "SELECT name, type, sql FROM sqlite_master WHERE type IN ('table', 'index')"
    )
    schema_info = cursor.fetchall()

    # Obtener los datos de cada tabla
    data = {}
    for name, type_, sql in schema_info:
        if type_ == "table":
            cursor.execute(f"SELECT * FROM {name}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            data[name] = {"columns": column_names, "rows": rows}

    conn.close()
    return schema_info, data


def generate_sql(schema_info, data, target_dialect="sqlite"):
    # Esta función generará las sentencias SQL para crear la base de datos en el motor objetivo.
    # target_dialect puede ser 'sqlite', 'postgresql', 'mysql', etc. (dependiendo del motor de destino)
    sql_statements = []

    for name, type_, sql in schema_info:
        if type_ == "table":
            sql_statements.append(sql)
            if name in data:
                for row in data[name]["rows"]:
                    values = ", ".join(
                        [f"'{str(v)}'" if v is not None else "NULL" for v in row]
                    )
                    insert_statement = f"INSERT INTO {name} ({', '.join(data[name]['columns'])}) VALUES ({values});"
                    sql_statements.append(insert_statement)
        elif type_ == "index":
            sql_statements.append(sql)

    return sql_statements


database_path = "audrit.sqlite"
schema_info, data = get_schema_and_data(database_path)
sql_statements = generate_sql(schema_info, data)

# Guardar las sentencias SQL en un archivo con codificación utf-8
with open("output.sql", "w", encoding="utf-8") as f:
    for statement in sql_statements:
        if not statement:
            continue

        if not statement.endswith(";"):
            statement += ";"

        if statement.startswith("INSERT INTO"):
            f.write(statement + "\n")


print("Las sentencias SQL se han generado correctamente en 'output.sql'")
