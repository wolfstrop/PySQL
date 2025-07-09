import mysql.connector # type: ignore
from tables import print_table
from messages import MSGS
import db_conn 



#mostrar DBS
def show_dbs(args):
    try:
        db_conn.cursor.execute("SHOW DATABASES")
        dbs = [{"Database": row["Database"]} for row in db_conn.cursor]
        print_table(["Database"], dbs, "BASES DE DATOS")
    except mysql.connector.Error as e:
        print(MSGS["error"](e))



#mostrar Tablas
def show_tables():
    
    try:
        db_conn.cursor.execute("SHOW TABLES")
        tables = [{"Tables": row[f"Tables_in_{db_conn.current_db}"]} for row in db_conn.cursor]
        
        # Mostrar incluso si no hay tablas
        print_table(["Tables"], tables, f"TABLAS EN '{db_conn.current_db.upper()}'")
        
    except mysql.connector.Error as e:
        print(MSGS["error"](e))



#Comando SQL
def sql_command(query):
    try:
        db_conn.cursor.execute(query)
        if db_conn.cursor.with_rows:
            headers = db_conn.cursor.column_names
            rows = db_conn.cursor.fetchall()
            print_table(headers, rows, "RESULTADO SQL")
        else:
            print(MSGS["sql_done"])
    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def use_command():
    db_name = db_conn.current_db
    try:
        db_conn.conn.database = db_name
        db_conn.current_db = db_name
        print(MSGS["using_db"](db_name))
        return db_name
    except mysql.connector.Error as e:
        print(MSGS["db_not_found"](db_name))




#mostrar relaciones
def show_rel_command():

    """Muestra relaciones entre tablas en el formato original"""
    db = db_conn.current_db
    if not db:
        print(MSGS["need_use"])
        return
    
    try:
        # Obtener tablas
        db_conn.cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (db,))
        tablas = [row["TABLE_NAME"] for row in db_conn.cursor]
        
        print(f"\nRelaciones en '{db}':")
        print("=" * 60)
        
        has_relations = False
        
        for tabla in tablas:
            print(f"\nTabla: {tabla}")
            print("-" * 60)
            
            # Obtener relaciones
            db_conn.cursor.execute("""
                SELECT COLUMN_NAME, 
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            """, (db, tabla))
            
            # Crear diccionario de relaciones
            relaciones = {}
            for row in db_conn.cursor:
                if row["REFERENCED_TABLE_NAME"]:
                    relaciones[row["COLUMN_NAME"]] = (
                        row["REFERENCED_TABLE_NAME"],
                        row["REFERENCED_COLUMN_NAME"]
                    )
            
            # Obtener todas las columnas de la tabla
            db_conn.cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            """, (db, tabla))
            
            # Mostrar columnas con relaciones marcadas
            for row in db_conn.cursor:
                col = row["COLUMN_NAME"]
                dtype = row["DATA_TYPE"]
                
                if col in relaciones:
                    ref_table, ref_col = relaciones[col]
                    print(f"  ↳ {col} ({dtype}) → {ref_table}.{ref_col}")
                    has_relations = True
                else:
                    print(f"  - {col} ({dtype})")
        
        if not has_relations:
            print(MSGS["no_relations"])
            
        print()
        
    except mysql.connector.Error as e:
        print(MSGS["error"](e))






#muestra contenido de una tabla
def show_data_command():
    """Muestra el contenido de todas las tablas"""
    target_db = db_conn.current_db
    
    try:
        # Obtener tablas de la base de datos
        db_conn.cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (target_db,))
        tablas = [row["TABLE_NAME"] for row in db_conn.cursor]
        
        if not tablas:
            print(f"No se encontraron tablas en '{target_db}'")
            return
            
        print(f"\nMostrando datos de '{target_db}':")
        print("=" * 60)
        
        # Mostrar contenido para cada tabla
        for tabla in tablas:
            # Usar la base de datos objetivo específicamente
            show_content_command(tabla)
        
    except mysql.connector.Error as e:
        print(MSGS["error"](e))



def clean_table_command(table_name):
    target_db = db_conn.current_db

    try:
        db_conn.cursor.execute(f"DELETE FROM `{target_db}`.`{table_name}`")
        show_content_command(table_name)
    except mysql.connector.Error as e:
        print(f"Tabla '{table_name}' no encontrada en '{target_db}': {e}")



def clean_all_command():
    """Muestra el contenido de todas las tablas"""
    target_db = db_conn.current_db
    
    try:
        # Obtener tablas de la base de datos
        db_conn.cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (target_db,))
        tablas = [row["TABLE_NAME"] for row in db_conn.cursor]
        
        if not tablas:
            print(f"No se encontraron tablas en '{target_db}'")
            return
            
        print(f"\nlimpiando datos de '{target_db}':")
        print("=" * 60)
        
        # Mostrar contenido para cada tabla
        for tabla in tablas:
            # Usar la base de datos objetivo específicamente
            clean_table_command(tabla)
        
    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def delete_table_command(table_name):
    target_db = db_conn.current_db

    try:
        db_conn.cursor.execute(f"DROP TABLE `{target_db}`.`{table_name}`")
        print(f"Tabla '{table_name}' eliminada correctamente de '{target_db}'")
    except mysql.connector.Error as e:
        print(f"Error al eliminar la tabla '{table_name}' en '{target_db}': {e}")




def delete_all_command():
    """Muestra el contenido de todas las tablas"""
    target_db = db_conn.current_db
    
    try:
        # Obtener tablas de la base de datos
        db_conn.cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (target_db,))
        tablas = [row["TABLE_NAME"] for row in db_conn.cursor]
        
        if not tablas:
            print(f"No se encontraron tablas en '{target_db}'")
            return
            
        print(f"\neliminando tablas en '{target_db}':")
        print("=" * 60)
        
        # Mostrar contenido para cada tabla
        for tabla in tablas:
            # Usar la base de datos objetivo específicamente
            delete_table_command(tabla)
        
    except mysql.connector.Error as e:
        print(MSGS["error"](e))



def destroy_command():
    target_db = db_conn.current_db
    
    try:
    
        db_conn.execute(f"DROP DATABASE `{target_db}`")
        print(f"Base de datos '{target_db}' eliminada exitosamente.")

        if db_conn.current_db == target_db:
            db_conn.current_db = None
    
    except mysql.connector.Error as e:
        print(f"Error al eliminar la base de datos '{target_db}': {e}")



def show_content_command(table_name):
    """Muestra el contenido de una o varias tablas"""
    target_db = db_conn.current_db

    try:
        # Especificar explícitamente la base de datos
        db_conn.cursor.execute(f"SELECT * FROM `{target_db}`.`{table_name}`")
        headers = db_conn.cursor.column_names
        rows = db_conn.cursor.fetchall()
        
        # Siempre mostrar estructura aunque esté vacía
        db_prefix = f"{target_db}." 
        print_table(headers, rows, f"CONTENIDO: {db_prefix}{table_name.upper()}")
        
    except mysql.connector.Error as e:
        print(f"Tabla '{table_name}' no encontrada en '{target_db}': {e}")



#===============================================================
#comandos table

def find_old_type(old):
    try:
        db_conn.cursor.execute(
            f"SELECT COLUMN_TYPE FROM information_schema.COLUMNS "
            f"WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
            (db_conn.current_db, db_conn.current_table, old)
        )
        result = db_conn.cursor.fetchone()

        if not result:
            print(f"La columna '{old}' no existe.")
            return
        

        return result
    

    except mysql.connector.Error as e:
        print(MSGS["error"](e))



def column_exist(col_name):
    db_conn.cursor.execute(
            "SELECT COUNT(*) FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s",
            (db_conn.current_db, db_conn.current_table, col_name)
    )
    exists = db_conn.cursor.fetchone()[0]
    return exists == 1


def get_table_columns():
    """
    Devuelve la lista de columnas (en orden) de la tabla actual.
    """
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    db_conn.cursor.execute(
        """
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME   = %s
        ORDER BY ORDINAL_POSITION
        """,
        (target_db, target_table)
    )
    rows = db_conn.cursor.fetchall()
    return [row[0] for row in rows]


def get_primary_key():
    """
    Devuelve el nombre de la columna PK de la tabla actual,
    o None si no tiene PK.
    """
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    db_conn.cursor.execute(
        "SELECT COLUMN_NAME "
        "FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s "
          "AND TABLE_NAME = %s "
          "AND COLUMN_KEY = 'PRI' "
        "LIMIT 1",
        (target_db, target_table)
    )
    res = db_conn.cursor.fetchone()
    return res[0] if res else None

def prompt_column_type():
    """
    Muestra un submenú para seleccionar el tipo de dato y devuelve
    la definición SQL correspondiente (p. ej. "VARCHAR(50)").
    """
    tipos = {
        '1': 'INT',
        '2': 'VARCHAR',
        '3': 'TEXT',
        '4': 'DATE',
        '5': 'FLOAT',
    }

    print("\nSelecciona el tipo de dato para la nueva columna:")
    for key, nombre in tipos.items():
        print(f"  {key}. {nombre}")
    choice = input("Opción [1-5]: ").strip()

    if choice not in tipos:
        print("Opción inválida. Cancelando operación.")
        return None

    tipo = tipos[choice]
    if tipo == 'VARCHAR':
        # Pedir longitud
        length = input("Especifica la longitud de VARCHAR (ej. 50): ").strip()
        if not length.isdigit():
            print("Longitud inválida. Cancelando.")
            return None
        return f"VARCHAR({length})"
    else:
        return tipo

def add_column_command(col_name):
    """
    ALTER TABLE ... ADD COLUMN `col_name` <tipo>.
    Antes muestra un menú para escoger tipo de dato.
    """
    target_db    = db_conn.current_db
    target_table = db_conn.current_table

    # 1) Validar no exista
    if column_exist(col_name):
        print(f"La columna '{col_name}' ya existe.")
        return

    # 2) Pedir tipo de dato
    data_type = prompt_column_type()
    if not data_type:
        return

    # 3) Ejecutar ALTER TABLE
    try:
        sql = (
            f"ALTER TABLE `{target_db}`.`{target_table}` "
            f"ADD COLUMN `{col_name}` {data_type}"
        )
        db_conn.cursor.execute(sql)
        db_conn.conn.commit()
        print(f"Columna '{col_name}' agregada con tipo {data_type}.")
    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def edit_column_command(old, new):
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    try:
        col_type = find_old_type(old)

        if not col_type:
            return 
        
        db_conn.cursor.execute(
            f"ALTER TABLE `{target_db}`.`{target_table}` CHANGE `{old}` `{new}` {col_type}"
        )
        
        db_conn.conn.commit()

        print(f"Columna '{old}' renombrada a '{new}' con tipo '{col_type}'.")
        show_content_command(target_table)
        
    except mysql.connector.Error as e:
        print(f"Error al renombrar columna: {e}")



def clean_column_command(col_name):
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    try:
        # Validamos que la columna exista
        
        if not column_exist(col_name):
            print(f"La columna '{col_name}' no existe en la tabla actual.")
            return

        # Intentamos poner todos los valores en NULL
        db_conn.cursor.execute(
            f"UPDATE `{target_db}`.`{target_table}` SET `{col_name}` = NULL"
        )
        db_conn.conn.commit()
        print(f"Todos los valores de la columna '{col_name}' fueron limpiados (ahora son NULL).")

    except mysql.connector.Error as e:
        print(MSGS["error"](e))



def delete_column_command(col_name):
    
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    try:
        if not column_exist(col_name):
            print(f"La columna '{col_name}' no existe en la tabla actual.")
            return

        db_conn.cursor.execute(
            f"ALTER TABLE `{target_db}`.`{target_table}` DROP COLUMN `{col_name}`"
        )
        db_conn.conn.commit()
        print(f"Columna '{col_name}' eliminada exitosamente.")

    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def modify_value_command(col, old, new):
    target_db = db_conn.current_db
    target_table = db_conn.current_table

    try:
        if not column_exist(col):
            print(f"La columna '{col}' no existe en la tabla actual.")
            return

        query = (
            f"UPDATE `{target_db}`.`{target_table}` "
            f"SET `{col}` = %s WHERE `{col}` = %s"
        )
        db_conn.cursor.execute(query, (new, old))
        db_conn.conn.commit()

        print(f"Se reemplazaron los valores '{old}' por '{new}' en la columna '{col}'.")

    except mysql.connector.Error as e:
        print(MSGS["error"](e))





def insert_value_command(col, val):
    """
    Inserta `val` en la primera fila donde `col` es NULL.
    Si no encuentra celdas vacías, sugiere usar INSERT-ROW.
    """
    target_db    = db_conn.current_db
    target_table = db_conn.current_table

    # 1) Validar que la columna exista
    if not column_exist(col):
        print(f"La columna '{col}' no existe en la tabla actual.")
        return

    # 2) Detectar PK para ordenar
    pk = get_primary_key()

    # 3) Ejecutar UPDATE sobre la primera celda NULL
    #    Usamos ORDER BY pk LIMIT 1 si hay PK; si no, simplemente LIMIT 1
    order_clause = f"ORDER BY `{pk}`" if pk else ""
    query = (
        f"UPDATE `{target_db}`.`{target_table}` "
        f"SET `{col}` = %s "
        f"WHERE `{col}` IS NULL "
        f"{order_clause} "
        f"LIMIT 1"
    )

    try:
        db_conn.cursor.execute(query, (val,))
        db_conn.conn.commit()

        if db_conn.cursor.rowcount > 0:
            print(f"Valor '{val}' insertado en la primera celda NULL de '{col}'.")
        else:
            print(
                f"No hay celdas NULL en la columna '{col}'.\n"
                "Usa el comando INSERT AT para agregar una nueva fila."
            )
    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def insert_at_command(arg_string):
    """
    INSERT-ROW <val1, val2, ..., valN>:
    Inserta una nueva fila con los valores en el orden de las columnas.
    """
    target_db    = db_conn.current_db
    target_table = db_conn.current_table

    # 1) Parsear valores
    values = [v.strip() for v in arg_string.split(',')]

    # 2) Obtener columnas
    columns = get_table_columns()
    n_cols = len(columns)
    n_vals = len(values)

    if n_vals != n_cols:
        print(
            f"INSERT-ROW necesita {n_cols} valores (una por columna); "
            f"recibiste {n_vals}."
        )
        return

    # 3) Construir la consulta
    col_list     = ', '.join(f"`{col}`" for col in columns)
    placeholders = ', '.join(['%s'] * n_cols)
    query = (
        f"INSERT INTO `{target_db}`.`{target_table}` "
        f"({col_list}) VALUES ({placeholders})"
    )

    # 4) Ejecutar
    try:
        db_conn.cursor.execute(query, tuple(values))
        db_conn.conn.commit()
        print(f"Fila insertada en '{target_table}' con valores: {values}")
    except mysql.connector.Error as e:
        print(MSGS["error"](e))




def clean_tables(table_list):     
    
    print("\nADVERTENCIA: Esta operación eliminará TODOS los datos de las tablas seleccionadas")
    print("Tablas a limpiar:", ", ".join(table_list))
    
    # Confirmación general
    resp = input("\n¿Continuar? (s/n): ").strip().lower()
    if resp != 's':
        print(MSGS["clean_canceled"])
        return False
    
    cleaned_count = 0
    for table in table_list:
        try:
            # Obtener conteo actual de filas
            db_conn.cursor.execute(f"SELECT COUNT(*) AS total FROM `{table}`")
            count_result = db_conn.cursor.fetchone()
            row_count = count_result["total"]
            
            if row_count == 0:
                print(f"Tabla '{table}' ya está vacía. Saltando.")
                continue
            
            # Confirmación específica por tabla
            resp = input(MSGS["clean_confirm"](table, row_count)).strip().lower()
            if resp != 's':
                print(f"Saltando limpieza de '{table}'")
                continue
            
            # Ejecutar DELETE (no TRUNCATE por problemas con FK)
            db_conn.cursor.execute(f"DELETE FROM `{table}`")
            db_conn.conn.commit()
            
            print(MSGS["clean_done"](table, row_count))
            cleaned_count += 1
            
        except mysql.connector.Error as e:
            print(MSGS["clean_error"](table, e))
            db_conn.conn.rollback()
    
    return cleaned_count > 0