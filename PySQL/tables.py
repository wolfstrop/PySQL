from datetime import datetime




#formatea las fechas para que seal mas legibles
def format_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, (bytes, bytearray)):
        return "0x" + value.hex()
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)


def print_table(headers, rows, title=None):
    # Primero, transforma rows en data_rows (strings ya formateados)
    if rows:
        if isinstance(rows[0], dict):
            data_rows = [[format_value(row.get(h)) for h in headers] for row in rows]
        else:
            data_rows = [[format_value(cell) for cell in row] for row in rows]
    else:
        data_rows = []

    # Ahora calculamos col_widths de forma segura
    col_widths = []
    for i, header in enumerate(headers):
        # ancho mínimo = largo del encabezado
        width = len(header)

        # si hay datos para esta columna, ajusta al máximo de las celdas
        if data_rows:
            # extraemos todos los valores de la columna i
            col_cells = [row[i] for row in data_rows]
            # calculamos el ancho máximo de las celdas (ya hay al menos uno)
            max_cells = max(len(cell) for cell in col_cells)
            width = max(width, max_cells)

        col_widths.append(width)

    # ...el resto queda igual (bordes, impresión)...
    top_border      = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    header_separator= "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    row_separator   = "│" + "│".join("─" * (w + 2) for w in col_widths) + "│"
    bottom_border   = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"

    if title:
        print(f"\n{title.center(len(top_border))}")
    print(top_border)

    # Encabezados
    header_row = "│ " + " │ ".join(
        headers[i].ljust(col_widths[i])
        for i in range(len(headers))
    ) + " │"
    print(header_row)
    print(header_separator)

    # Filas de datos o mensaje de vacía
    if data_rows:
        for row in data_rows:
            data_row = "│ " + " │ ".join(
                cell.ljust(col_widths[i])
                for i, cell in enumerate(row)
            ) + " │"
            print(data_row)
    else:
        # Mensaje centrado que ocupa todas las columnas
        total_width = sum(col_widths) + 3*(len(headers)-1)
        empty_msg = " TABLA VACÍA "
        empty_cell = empty_msg.center(total_width, ' ')
        print(f"│ {empty_cell} │")

    print(bottom_border)

    # Conteo de filas
    if rows:
        print(f"Total: {len(rows)} fila(s)\n")
    else:
        print()  # solo espacio para formato


