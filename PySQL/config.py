import sys


#lectura de archivo
def load_config(path="config.txt"):
    cfg = {}
    try:
        with open(path) as f:
            for line in f:
                if ':' in line:
                    k, v = line.strip().split(':', 1)
                    cfg[k] = v
    except FileNotFoundError:
        print(f"Error: Archivo de configuración '{path}' no encontrado")
        sys.exit(1)
    return cfg
