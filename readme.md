# PySQL - Herramienta CLI para gestión de bases de datos

## Descripción:

PySQL es una aplicación de línea de comandos (CLI) desarrollada para facilitar la exploración, visualización y modificación de bases de datos MySQL de forma rápida y segura, sin depender de herramientas externas como XAMPP o interfaces gráficas. Incluye confirmaciones antes de operaciones destructivas y un sub-REPL especializado para editar tablas de manera interactiva.

## Características principales:

* Listado y selección de bases de datos.
* Visualización de tablas y contenido de forma inmediata.
* Ejecución de consultas SQL arbitrarias.
* Comandos de limpieza (borrar datos) y eliminación (DROP) a nivel de tabla y base de datos con confirmación.
* Sub-REPL de edición de tablas con operaciones: agregar, renombrar, limpiar, eliminar columnas; reemplazar valores; insertar datos en celdas vacías; agregar filas completas.
* Menú interactivo para elegir tipos de datos al agregar columnas.
* Manejo seguro de errores y protección contra inyecciones SQL.

## Requisitos:

* Python 3.7+
* Conector `mysql-connector-python` (o similar)
* Acceso a una base de datos MySQL
* Archivo `config.txt` con los siguientes datos:

  ```
  user:root
  password:
  host:localhost
  port:3306
  ```


## Uso:

Ejecuta el main principal:

```bash
python main.py
```

### Comandos principales:

```
dbs                         Lista bases de datos
use <nombre>                Seleccionar base de datos
tables                      Listar tablas
table / show data <db?>     Mostrar datos de tablas
show rel <db?>              Mostrar relaciones de esquemas
sql <consulta>              Ejecutar consulta SQL arbitraria
clean <tablas>              Limpiar datos en tablas específicas
clean all <db?>             Limpiar todos los datos de la base
delete <tablas>             Eliminar tablas específicas
delete all <db?>            Eliminar todas las tablas
destroy <db?>               Borrar base de datos completa
help                        Mostrar este mensaje de ayuda
exit / quit                 Salir de la aplicación
```

### Modo edición de tablas (`modify <tabla>`):

```
ADD <columna>                        → Agregar nueva columna
RENAME <columna> TO <nuevo>          → Renombrar columna
CLEAR <columna>                      → Limpiar datos de columna (SET NULL)
DROP <columna>                       → Eliminar columna
REPLACE <columna>,<viejo>,<nuevo>    → Reemplazar valor específico
SET <columna>,<valor>                → Insertar valor en primer NULL
INSERT-ROW <v1>,<v2>,...,<vN>        → Agregar nueva fila completa
LEAVE                                → Salir del modo edición
```

## Contribuciones:

¡Las contribuciones son bienvenidas! Siéntete libre de abrir issues o pull requests para sugerir mejoras, corregir bugs o agregar nuevas funcionalidades.

