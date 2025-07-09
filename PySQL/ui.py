import db_conn
from messages import MSGS
import re 


def parse_table_list(input_str):
    """
    Parsea una cadena de entrada con nombres de tablas separados por comas
    y devuelve una lista limpia de nombres de tablas
    """
    # Eliminar espacios innecesarios y dividir por comas
    tables = [t.strip() for t in input_str.split(',')]
    
    # Filtrar elementos vacíos
    tables = [t for t in tables if t]
    
    # Validar nombres de tablas (solo caracteres permitidos)
    valid_tables = []
    for table in tables:
        if re.match(r'^[\w$]+$', table):
            valid_tables.append(table)
        else:
            print(f"Advertencia: Nombre de tabla inválido '{table}' ignorado")
    
    return valid_tables





def validate_target_db(db_name):
    """
    Valida y obtiene la base de datos objetivo
    - Si se proporciona db_name, la retorna
    - Si no, usa la base de datos actual
    """
    if db_name and db_name.strip() and db_name.strip().lower() != "none":
        return db_name
    
    if db_conn.current_db:
        return db_conn.current_db
    
    print(MSGS["need_use"])

def confirm_action(action):
    respuesta = input(MSGS["confirm"](action)).strip.lower()
    return respuesta in ('s', 'sí', 'si', 'y', 'yes')


def extract_db_name(args):
    """
    Extrae el nombre de la base de datos de los argumentos
    """
    if not args:
        return None
    
    parts = args.split()
    return parts[0] if parts else None