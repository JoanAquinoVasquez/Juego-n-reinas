from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def free(tablero, row, col, n):
    """ Determina si la casilla tablero[row][col] está libre de ataques.

    @param tablero: Tablero actual
    @param row: Fila
    @param col: Columna
    @param n: Tamaño del tablero (n x n)
    @return: True si la casilla está libre de ataques por otras reinas.
    """
    for i in range(n):
        if tablero[row][i] == '|R|' or tablero[i][col] == '|R|':
            return False

    if row <= col:
        c = col - row
        r = 0           
    else:
        r = row - col
        c = 0
    while c < n and r < n:
        if tablero[r][c] == '|R|':
            return False
        r += 1
        c += 1

    if row <= col:
        r = 0
        c = col + row
        if c > (n-1):
            r = c - (n-1)
            c = (n-1)
    else:
        c = n-1
        r = row - (c - col)

    while c >= 0 and r < n:
        if tablero[r][c] == '|R|':
            return False
        r += 1
        c -= 1

    return True

def agregar_reina(tablero, reinas, pasos, n):
    """ Agrega reinas al tablero de manera recursiva y guarda los pasos.

    @param tablero: Tablero actual
    @param reinas: Número de reinas que faltan por colocar
    @param pasos: Lista de tableros en cada paso
    @param n: Tamaño del tablero (n x n)
    @return: True si se pudo agregar las reinas requeridas
    """
    if reinas < 1:
        return True

    for idx_row in range(n):
        for idx_col in range(n):
            if free(tablero, idx_row, idx_col, n):
                tablero[idx_row][idx_col] = '|R|'
                pasos.append([row.copy() for row in tablero])
                if agregar_reina(tablero, reinas-1, pasos, n):
                    return True
                else:
                    tablero[idx_row][idx_col] = '|_|'
                    pasos.append([row.copy() for row in tablero])

    return False

@csrf_exempt
def index(request):
    """ Vista para manejar la página principal y resolver el problema de las N reinas.

    @param request: Request HTTP
    @return: Renderiza la plantilla 'index.html' con los resultados
    """
    if request.method == 'POST':
        n = int(request.POST.get('n'))
        tablero = [['|_|'] * n for _ in range(n)]
        pasos = [[row.copy() for row in tablero]]
        has_solution = agregar_reina(tablero, n, pasos, n)
        return render(request, 'tablero/index.html', {'pasos': pasos, 'has_solution': has_solution, 'n': n})
    
    return render(request, 'tablero/index.html')
