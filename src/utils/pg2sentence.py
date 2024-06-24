import psycopg2
from psycopg2 import sql


def get_postgres_schema_and_data(connection_params):
    # Conectarse a la base de datos PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Obtener la estructura de la base de datos
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()

    schema_info = []
    data = {}

    for table in tables:
        table_name = table[0]
        print(
            f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), (SELECT MAX(id) FROM {table_name}));"
        )
        # Obtener la definición de la tabla
        cursor.execute(
            sql.SQL(
                f"SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = '{table_name}'"
            )  # .format(table=sql.Identifier(table_name))
        )
        columns = cursor.fetchall()

        # Crear el SQL de creación de la tabla
        create_table_sql = f"CREATE TABLE {table_name} ("
        col_defs = []
        for col in columns:
            col_def = f"{col[0]} {col[1]}"
            if col[2] is not None:
                col_def += f"({col[2]})"
            col_defs.append(col_def)
        create_table_sql += ", ".join(col_defs) + ");"
        schema_info.append((table_name, "table", create_table_sql))

        # Obtener los datos de la tabla
        cursor.execute(
            sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name))
        )
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data[table_name] = {"columns": column_names, "rows": rows}

    # Obtener los índices
    cursor.execute("""
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
    """)
    indexes = cursor.fetchall()
    for index in indexes:
        schema_info.append((index[0], "index", index[1]))

    conn.close()
    return schema_info, data


def generate_sql(schema_info, data):
    sql_statements = []

    for name, type_, _sql in schema_info:
        if type_ == "table":
            sql_statements.append(_sql)
            if name in data:
                for row in data[name]["rows"]:
                    values = ", ".join(
                        [f"'{str(v)}'" if v is not None else "NULL" for v in row]
                    )
                    insert_statement = f"INSERT INTO {name} ({', '.join(data[name]['columns'])}) VALUES ({values});"
                    sql_statements.append(insert_statement)
        elif type_ == "index":
            sql_statements.append(_sql)

    return sql_statements


# Parámetros de conexión a la base de datos PostgreSQL
connection_params = {
    "dbname": "audrit",
    "user": "rodri",
    "password": "rodri",
    "host": "localhost",
    "port": 5432,
}

schema_info, data = get_postgres_schema_and_data(connection_params)
sql_statements = generate_sql(schema_info, data)

# Guardar las sentencias SQL en un archivo con codificación utf-8
with open("output_postgres.sql", "w", encoding="utf-8") as f:
    for statement in sql_statements:
        if statement.startswith("INSERT INTO"):
            f.write(statement + "\n")

print("Las sentencias SQL se han generado correctamente en 'output_postgres.sql'")
