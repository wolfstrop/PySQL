from commands import *
from ui import *
import sub_repl
import repl
import sys




# Handlers básicos
def handle_use(args):
    db_name = extract_db_name(args)
    try:
        db_conn.current_db = validate_target_db(db_name)
    except DatabaseNotFoundError: # type: ignore
        print(MSGS['db_not_found'](db_name))
        return
    use_command()
    show_tables()


def handle_show_rel(args):
    show_rel_command()


def handle_show_data(args):
    show_data_command()


def handle_tables(args):
    show_tables()


def handle_select(args):
    table_list = parse_table_list(args)
    if table_list:
        for table in table_list:
            show_content_command(table)

    else:
        print(MSGS["invalid_table_list"])


def handle_clean_table(args):
    tables = parse_table_list(args)
    for table in tables:
        if confirm_action(f"limpipar la tabla '{table}'"):
            clean_table_command(table)


def handle_clean_all(args):
    if confirm_action(f"limpiar todas las tablas de la base '{db_conn.current_db}'"):
        clean_all_command()


def handle_delete_table(args):
    tables = parse_table_list(args)
    for table in tables:
        if confirm_action(f"eliminar la tabla '{table}'"):
            delete_table_command(table)


def handle_delete_all(args):
    if confirm_action(f"eliminar todas las tablas de la base '{db_conn.current_db}'"):
        delete_all_command()


def handle_destroy(args):
    if confirm_action(f"eliminar la base '{db_conn.current_db}'"):
        destroy_command()





#===================================
#COMANDOS DE MODIFICACION DE TABLAS
#===================================

def handle_modify_menu():
    table = db_conn.current_table
    show_content_command(table)
    print(MSGS["selected_menu_fast"])



def handle_modify_table(args):
    """select table y entrar al modo edición."""
    tables = parse_table_list(args)
    if len(tables) != 1:
        print(MSGS['select_one_table'])
        return
    tbl = tables[0]
    db_conn.current_table = tbl
    # Aquí podrías validar existencia con ui.table_exists
    handle_modify_menu()
    sub_repl.sub_repl()


def handle_add(args):
    add_column_command(args)
    handle_modify_menu()



def handle_rename(args):
    parts = args.split()
    if len(parts) != 3 or parts[1].lower() != 'to':
        print(MSGS['need_args']('RENAME <col> TO <nuevo>'))
        return
    old, _, new = parts
    edit_column_command(old, new)
    handle_modify_menu()



def handle_clear_col(args):
    if confirm_action(f"limpiar la columna `{args}`"):
        clean_column_command(args)
    handle_modify_menu()



def handle_drop_col(args):
    if confirm_action(f"eliminar la columna `{args}`"):
        delete_column_command(args)
    handle_modify_menu()


#en este va a estar complicado, se necesita arreglar
def handle_replace(args):
    parts = [p.strip() for p in args.split(',')]
    if len(parts) != 3:
        print(MSGS['need_args']('REPLACE <col>, <viejo>, <nuevo>'))
        return
    col, old, new = parts
    modify_value_command(col, old, new)
    handle_modify_menu()


def handle_set(args):
    parts = args.split(maxsplit=1)
    if len(parts) != 2:
        print(MSGS['need_args']('SET <col> <valor>'))
        return
    col, val = parts
    insert_value_command(col, val)
    handle_modify_menu()

def handle_insert(args):
    insert_at_command(args)
    handle_modify_menu()

def handle_leave(args):
    db_conn.current_table = None
    # romper sub_repl
    show_tables()
    repl.repl()



#===========================
#OTROS COMANDOS
#=======================
def handle_sql(args):
    sql_command(args)


def handle_help(args):
    print("\n" * 50)
    print(MSGS["help"])


def handle_help_table(args):
    print("\n" * 50)
    print(MSGS["help_selected"])


def handle_exit(args):
    print("\n" * 50)
    print(MSGS["bye"])
    sys.exit(0)


def handle_more_info(args):
    print(MSGS['more_info'])
    print(MSGS['art1'])
    input("\nPresiona Enter para continuar...")
    print("\n" * 50)


def handle_welcome():
    #Manejo menu
    print(MSGS["art_welcome"])
    print(MSGS["bienvenida"])
    input("\nPresiona Enter para continuar...")
    print("\n" * 50)  # Limpiar pantalla
    show_dbs("")
