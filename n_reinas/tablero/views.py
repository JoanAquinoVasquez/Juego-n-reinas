from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def free(tablero, row, col, n):
    """Determina si la casilla rowxcol está libre de ataques."""
    for i in range(n):
        if tablero[row][i] == '|R|' or tablero[i][col] == '|R|':
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == '|R|':
            return False

    for i, j in zip(range(row, -1, -1), range(col, n)):
        if tablero[i][j] == '|R|':
            return False

    return True

def agregar_reina(tablero, row, n, soluciones, pasos):
    """Agrega n reinas al tablero."""
    if row == n:
        soluciones.append([r.copy() for r in tablero])
        if not pasos or pasos[-1]['tablero'] != tablero:
            pasos.append({'tablero': [r.copy() for r in tablero], 'is_solution': True})
        return

    for col in range(n):
        if free(tablero, row, col, n):
            tablero[row][col] = '|R|'
            if not pasos or pasos[-1]['tablero'] != tablero:
                pasos.append({'tablero': [r.copy() for r in tablero], 'is_solution': False})
            agregar_reina(tablero, row + 1, n, soluciones, pasos)
            tablero[row][col] = '|_|'
            if not pasos or pasos[-1]['tablero'] != tablero:
                pasos.append({'tablero': [r.copy() for r in tablero], 'is_solution': False})

@csrf_exempt
def index(request):
    """Vista para manejar la página principal y resolver el problema de las N reinas."""
    if request.method == 'POST':
        n = int(request.POST.get('n'))
        tablero = [['|_|'] * n for _ in range(n)]
        pasos = [{'tablero': [row.copy() for row in tablero], 'is_solution': False}]
        soluciones = []
        agregar_reina(tablero, 0, n, soluciones, pasos)
        has_solution = len(soluciones) > 0
        return render(request, 'tablero/index.html', {'pasos': pasos, 'soluciones': soluciones, 'has_solution': has_solution, 'n': n})
    
    return render(request, 'tablero/index.html')
