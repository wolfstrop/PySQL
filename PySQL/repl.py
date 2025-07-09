import db_conn
from messages import MSGS
from ui import validate_target_db, extract_db_name
import command_specs




def start():
    import handlers
    handlers.handle_welcome()
    repl()



def repl():
    while True:
        try:

            line = input(MSGS['prompt'](db_conn.current_db)).strip()
            
            if not line:
                continue


            cmd_key, args = command_specs.parse_command_key(line)
            spec = command_specs.COMMAND_SPECS.get(cmd_key)
            
            if not spec:
                print(MSGS['unknown'](cmd_key))
                continue
            # Opciones de BD opcional
            
            if spec.opt_db_arg and args:
                db_name = extract_db_name(args)
                db_conn.current_db = validate_target_db(db_name)
                args = ' '.join(args.split()[1:])
            
            elif spec.needs_current_db and not db_conn.current_db:
                print(MSGS['need_use'])
                continue
            
            if spec.req_args and not args:
                print(MSGS['need_args'](cmd_key))
                continue
            
            if spec.needs_current_table and not db_conn.current_table:
                print(MSGS['need_table'])
                continue
            
            spec.handler(args)
        except KeyboardInterrupt:
            print(MSGS['ctrl_c'])
        """except DatabaseNotFoundError as e: # type: ignore
            print(MSGS['db_not_found'](str(e)))
        except TableNotFoundError as e: # type: ignore
            print(MSGS['table_not_found'](str(e)))
        except InvalidSyntaxError: # type: ignore
            print(MSGS['invalid_syntax'])
        except Exception as e:
            print(MSGS['error'](e))"""


