import math
import heapq
import time

# Definir clase de nodos en el grid
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Costo del inicio a este nodo
        self.h = 0  # Estimación heurística hasta el destino
        self.f = 0  # Costo total (g + h)
    
    # Comparadores para usarse en la priority queue
    def __lt__(self, other):
        return self.f < other.f

# Definir el algoritmo A*
def a_star(start, end, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    closed_set = set()
    start.g = start.h = start.f = 0
    end_node = None
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        # Si llegamos al nodo destino, reconstruimos la ruta
        if current.x == end.x and current.y == end.y:
            end_node = current
            break
        
        closed_set.add((current.x, current.y))
        
        # Explorar vecinos (movimientos rectos sin diagonales)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = current.x + dx, current.y + dy
            
            # Verificar si está dentro del grid y es transitable
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:
                if (x, y) in closed_set:
                    continue
                
                neighbor = Node(x, y, current)
                neighbor.g = current.g + 1
                neighbor.h = math.sqrt((end.x - x) * 2 + (end.y - y) * 2)
                neighbor.f = neighbor.g + neighbor.h
                
                # Añadir a la open set
                heapq.heappush(open_set, (neighbor.f, neighbor))
    
    # Reconstruir la ruta en forma de lista de nodos
    path = []
    while end_node:
        path.append((end_node.x, end_node.y))
        end_node = end_node.parent
    path.reverse()
    return path

# Generar comandos para cada paso en la ruta
def generate_commands(path):
    commands = []
    current_direction = 'UP'  # Suponemos que el robot empieza orientado hacia arriba

    for i in range(1, len(path)):
        x0, y0 = path[i - 1]
        x1, y1 = path[i]
        distance = 48  # Distancia entre celdas (puedes ajustarlo)

        # Determinar la nueva dirección
        if x1 > x0:
            new_direction = 'RIGHT'
        elif x1 < x0:
            new_direction = 'LEFT'
        elif y1 > y0:
            new_direction = 'UP'
        elif y1 < y0:
            new_direction = 'DOWN'
        print(new_direction)
        # Determinar los comandos de giro necesarios
        if new_direction != current_direction:
            if current_direction == 'UP':
                # commands.append("direccion Actual: "+current_direction)
                # commands.append("nueva direccion: "+new_direction)
                if new_direction == 'RIGHT':
                    commands.append("GIRA DERECHA")
                    commands.append(f"250,-245,1n")
                elif new_direction == 'LEFT':
                    commands.append("GIRA IZQUIERDA")
                    commands.append(f"-250,244,2n")
                elif new_direction == 'DOWN':
                    commands.append("GIRA 180")
                    commands.append(f"250,-243,3.5n")
            elif current_direction == 'DOWN':
                # commands.append("direccion Actual: "+current_direction)
                # commands.append("nueva direccion: "+new_direction)
                if new_direction == 'RIGHT':
                    commands.append("GIRA IZQUIERDA")
                    commands.append(f"-250,244,2n")
                elif new_direction == 'LEFT':
                    commands.append("GIRA DERECHA")
                    commands.append(f"250,-245,2n")
                elif new_direction == 'UP':
                    commands.append("GIRA 180")
                    commands.append(f"250,-243,3.5n")
            elif current_direction == 'LEFT':
                # commands.append("direccion Actual: "+current_direction)
                # commands.append("nueva direccion: "+new_direction)
                if new_direction == 'UP':
                    commands.append("GIRA DERECHA")
                    commands.append(f"250,-245,2n")
                elif new_direction == 'DOWN':
                    commands.append("GIRA IZQUIERDA")
                    commands.append(f"-250,244,2n")
                elif new_direction == 'RIGHT':
                    commands.append("GIRA 180")
                    commands.append(f"250,-243,3.5n")
            elif current_direction == 'RIGHT':
                # commands.append("direccion Actual: "+current_direction)
                # commands.append("nueva direccion: "+new_direction)
                if new_direction == 'UP':
                    commands.append("GIRA IZQUIERDA")
                    commands.append(f"-250,244,2n")
                elif new_direction == 'DOWN':
                    commands.append("GIRA DERECHA")
                    commands.append(f"250,-245,2n")
                elif new_direction == 'LEFT':
                    commands.append("GIRA 180")
                    commands.append(f"250,-243,3.5n")
        
        # Después de girar, actualizar la dirección actual
        current_direction = new_direction
        
        # Agregar el comando de movimiento en la nueva dirección
        commands.append(f"MUEVE recto")
        print("MOV RECTO")
        commands.append(f"248,250,{distance}n")
    
    return commands

# Crear una lista para almacenar la matriz leída
matriz_cuadricula = []

# Leer el archivo y reconstruir la matriz
with open("matriz.txt", "r") as archivo:
    for linea in archivo:
        # Convertimos cada línea en una lista de enteros
        fila = list(map(int, linea.split()))
        matriz_cuadricula.append(fila)

# matriz_cuadricula ahora contiene la matriz original
print(matriz_cuadricula)

# Crear una lista para almacenar la matriz leída
inicio_fin = []

# Leer el archivo y reconstruir la matriz
with open("inicioFin.txt", "r") as archivo:
    for linea in archivo:
        # Convertimos cada línea en una lista de enteros
        fila = list(map(int, linea.split()))
        inicio_fin.append(fila)

# matriz_cuadricula ahora contiene la matriz original
print(inicio_fin)


# Ejemplo de grid (0=camino, 1=obstáculo)
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0]
]
grid = matriz_cuadricula
# Definir el nodo inicial y el destino
print(inicio_fin[0][0])
print(inicio_fin[1][0])
start = Node(0,0)
end = Node(1,0)
start = Node(inicio_fin[0][0],inicio_fin[0][1])
end = Node(inicio_fin[1][0],inicio_fin[1][1])

# Encontrar la ruta
path = a_star(start, end, grid)
print("Ruta:", path)

# Generar y mostrar los comandos
commands = generate_commands(path)
print("Comandos:", commands)
#print(len(commands)/2)
# Guardar en un archivo de texto
with open("comandos.txt", "w") as file:
    for comando in commands:
        file.write(comando + "\n")
    print("Comandos guardados")

with open("direcciones.txt", "w") as file:
    for comando in commands:
        file.write(comando + "\n")
    print("direcciones guardados")