import mysql.connector # type: ignore
from config import load_config


conn = None
cursor = None 
current_db = None 
current_table = None
cfg = None 


#coneccion
def connect_db():

    global conn, cursor, cfg, current_db, current_table


    cfg = load_config()

    conn = mysql.connector.connect(
        user=cfg.get("user"),
        password=cfg.get("password"),
        host=cfg.get("host","localhost"),
        port=int(cfg.get("port", 3306))
    )

    cursor = conn.cursor(dictionary = True)

def close_conn():
    global conn, cursor
    if cursor:
        cursor.close()
    if conn:
        conn.close()
