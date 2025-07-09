from collections import namedtuple
from handlers import *



Command = namedtuple('Command', ['handler', 'req_args', 'needs_current_db', 'opt_db_arg', 'needs_current_table'])
#'handler', 'requiere argumentos?', 'revisa current db?', 'recibe alguna base de datos en especifico', 'necesita una tabla especifica'

COMMAND_SPECS = {
    #comandos de BDs
    'dbs':          Command(show_dbs,               False,  False,  False,  False),
    'databases':    Command(show_dbs,               False,  False,  False,  False),
    
    #comandos BD
    'use':          Command(handle_use,             True,   False,  False,  False),
    'show rel':     Command(handle_show_rel,        False,  True,   True,   False),
    
    #destroy
    'destroy':      Command(handle_destroy,         False, True,    True,   False),

    #comandos tablas
    'select':       Command(handle_select,          True,   True,   False,  False),
    'show data':    Command(handle_show_data,       False,  True,   True,   False),
    'tables':       Command(handle_tables,          False,  True,   True,   False),
    'table':        Command(handle_tables,          False,  True,   True,   False),
    #comandos tablas limpieza
    'clean table':  Command(handle_clean_table,     True,   True,   False,  False),
    'clean all':    Command(handle_clean_all,       False,  True,   True,   False),
    
    #eliminar tablas
    'delete table': Command(handle_delete_table,    True,  True,   False,  False),
    'delete all':   Command(handle_delete_all,      False,  True,   True,   False),

    #Modify table
    'modify':       Command(handle_modify_table,    True, True, False, False),
    
    'ADD':          Command(handle_add,             True,  True,  False, True),
    'RENAME':       Command(handle_rename,          True,  True,  False, True),
    'CLEAR':        Command(handle_clear_col,       True,  True,  False, True),
    'DROP':         Command(handle_drop_col,        True,  True,  False, True),
    'REPLACE':      Command(handle_replace,         True,  True,  False, True),
    'SET':          Command(handle_set,             True,  True,  False, True),
    'INSERT':       Command(handle_insert,          True,  True,  False, True),
    'LEAVE':        Command(handle_leave,           False, True,  False, True),
    
    #mas funciones
    'sql':          Command(handle_sql,             True,  False, False, False),

    #otros
    'help':         Command(handle_help,            False, False, False, False),
    'HELP':         Command(handle_help_table,      False, False, False, False),
    'more info':    Command(handle_more_info,       False, False, False, False),
    'exit':         Command(handle_exit,            False, False, False, False),
    'quit':         Command(handle_exit,            False, False, False, False),

}


def parse_command_key(line):
    parts = line.split()
    if len(parts) >= 2:
        two = f"{parts[0].lower()} {parts[1].lower()}"
        if two in COMMAND_SPECS:
            return two, ' '.join(parts[2:])
    one = parts[0].lower()
    return one, ' '.join(parts[1:])



def parse_sub_command_key(line: str):
    """
    Devuelve (CMD_KEY, args) donde CMD_KEY está en UPPERCASE
    y args es el resto de la línea tal cual para que cada handler lo procese.
    Maneja comandos de 1 o 2 palabras (p. ej. "RENAME X TO Y").
    """
    parts = line.strip().split()
    if not parts:
        return '', ''
    # intenta dos palabras juntas
    if len(parts) >= 2:
        two = f"{parts[0].upper()} {parts[1].upper()}"
        if two in COMMAND_SPECS:
            # consume longitud de "TWO" + 1 espacio
            rest = line[len(two):].lstrip()
            return two, rest
    # fallback a comando de una palabra
    key = parts[0].upper()
    rest = line[len(parts[0]):].lstrip()
    return key, rest
