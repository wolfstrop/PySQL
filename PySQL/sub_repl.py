from messages import MSGS
import db_conn
import command_specs

def sub_repl():
    while True:
        try:
            prompt = MSGS['prompt_table'](db_conn.current_db, db_conn.current_table)
            line = input(prompt).strip()
            
            if not line:
                continue

            cmd_key, args = command_specs.parse_sub_command_key(line)
            
            spec = command_specs.COMMAND_SPECS.get(cmd_key)
            
            if not spec:
                print(MSGS['unknown'](cmd_key))
                continue

            
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
        except Exception as e:
            print(MSGS['error s'](e))