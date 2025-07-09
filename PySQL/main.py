#!/usr/bin/env python3
import sys 
from db_conn import connect_db, close_conn




if __name__ == "__main__":
    
    try:
        connect_db()
        import repl
        repl.start()
    except Exception as e:
        print(f"Error crítico: {e}")
        sys.exit(1)
    finally:
        close_conn()


