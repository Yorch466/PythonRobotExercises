import cv2
import numpy as np

# Cargar la imagen y convertirla a escala de grises
ruta_imagen = './matrizColoresFijo.jpeg'
imagen = cv2.imread(ruta_imagen)
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

frameHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
# Rango de color rojo en HSV (dividido en dos partes) es el inicio
nb_rojo_1 = np.array([0, 100, 100], np.uint8)
nm_rojo_1 = np.array([10, 255, 255], np.uint8)
nb_rojo_2 = np.array([160, 100, 100], np.uint8)
nm_rojo_2 = np.array([180, 255, 255], np.uint8)
mask_rojo_1 = cv2.inRange(frameHSV, nb_rojo_1, nm_rojo_1)
mask_rojo_2 = cv2.inRange(frameHSV, nb_rojo_2, nm_rojo_2)
mask_rojo = cv2.add(mask_rojo_1, mask_rojo_2)  # Combinar ambas máscaras para el rojo

# Rango de color azul en HSV pared
nb_azul = np.array([100, 150, 110], np.uint8)  # Saturación y valor aumentados
nm_azul = np.array([140, 255, 255], np.uint8)
mask_azul = cv2.inRange(frameHSV, nb_azul, nm_azul)

# Rango de color verde en HSV final
nb_verde = np.array([40, 50, 50], np.uint8)
nm_verde = np.array([90, 255, 255], np.uint8)
mask_verde = cv2.inRange(frameHSV, nb_verde, nm_verde)

# Aplicar detección de bordes----------------------------
bordes = cv2.Canny(gris, 50, 150, apertureSize=3)

# Detectar líneas usando la transformada de Hough
lineas = cv2.HoughLinesP(bordes, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

# Inicializar listas para las líneas horizontales y verticales
lineas_horizontales = []
lineas_verticales = []
# Filtrar líneas horizontales y verticales
for linea in lineas:
    x1, y1, x2, y2 = linea[0]  # Cada línea debe tener el formato (x1, y1, x2, y2)
    
    # Detectar si es horizontal o vertical
    if abs(y2 - y1) < 10:  # Línea horizontal (diferencia pequeña en y)
        lineas_horizontales.append(y1)
    elif abs(x2 - x1) < 10:  # Línea vertical (diferencia pequeña en x)
        lineas_verticales.append(x1)

# Ordenar y eliminar duplicados
lineas_horizontales = sorted(set(lineas_horizontales))
lineas_verticales = sorted(set(lineas_verticales))

#agrupar lineas
# Umbral de cercanía entre números
umbral = 30

# Crear grupos de números cercanos vertical
grupos = []
grupo_actual = [lineas_verticales[0]]

for num in lineas_verticales[1:]:
    if num - grupo_actual[-1] <= umbral:
        grupo_actual.append(num)
    else:
        grupos.append(grupo_actual)
        grupo_actual = [num]
grupos.append(grupo_actual)  # Añadir el último grupo
# Obtener el valor central de cada grupo
valores_centrales = [int(np.median(grupo)) for grupo in grupos]
#print(valores_centrales)
#print(lineas_verticales)
lineas_verticales = valores_centrales

# Crear grupos de números cercanos vertical
grupos = []
grupo_actual = [lineas_horizontales[0]]

for num in lineas_horizontales[1:]:
    if num - grupo_actual[-1] <= umbral:
        grupo_actual.append(num)
    else:
        grupos.append(grupo_actual)
        grupo_actual = [num]
grupos.append(grupo_actual)  # Añadir el último grupo
# Obtener el valor central de cada grupo
valores_centrales = [int(np.median(grupo)) for grupo in grupos]
#print(valores_centrales)
#print(lineas_verticales)
lineas_horizontales = valores_centrales

# Determinar la cantidad de celdas de la cuadrícula
num_filas = len(lineas_horizontales) - 1
num_columnas = len(lineas_verticales) - 1
print(num_filas)
print(num_columnas)
# Crear la matriz con el tamaño de la cuadrícula y rellenarla con ceros
matriz_cuadricula = np.zeros((num_filas, num_columnas), dtype=int)

# Mostrar la imagen con las líneas de la cuadrícula detectadas (opcional)
for y in lineas_horizontales:
    cv2.line(imagen, (0, y), (imagen.shape[1], y), (0, 255, 0), 2)
for x in lineas_verticales:
    cv2.line(imagen, (x, 0), (x, imagen.shape[0]), (0, 255, 0), 2)

# Contorno colores----------------------------
inicioRed = None
finalGreen = None
contorno, noseusa = cv2.findContours(mask_rojo.copy(),1,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imagen, contorno, -1,(0,0,255),3)
if len(contorno) > 0:
    c = max(contorno, key=cv2.contourArea)
    M = cv2.moments(c)

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(imagen, (cx, cy), 8, (0, 0, 255),-1)

    i=-1
    for y in lineas_horizontales:
        if cy < y:
            matrizY=i
            break
        i+=1
    i=-1
    for x in lineas_verticales:
        if cx < x:
            matrizX=i
            break
        i+=1
    #print(matrizX)
    #print(matrizY)
    #matriz_cuadricula[matrizY][matrizX]=1
    inicioRed = [matrizY,matrizX]

'''
# Aplicar detección de bordes del color azul
bordes = cv2.Canny(mask_azul, 50, 150, apertureSize=3)
# Detectar líneas usando la transformada de Hough
lineasA = cv2.HoughLinesP(bordes, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
# Inicializar listas para las líneas horizontales y verticales
lineas_horizontalesA = []
lineas_verticalesA = []
# Filtrar líneas horizontales y verticales
for linea in lineasA:
    x1, y1, x2, y2 = linea[0]  # Cada línea debe tener el formato (x1, y1, x2, y2)
    
    # Detectar si es horizontal o vertical
    if abs(y2 - y1) < 10:  # Línea horizontal (diferencia pequeña en y)
        lineas_horizontalesA.append(y1)
    elif abs(x2 - x1) < 10:  # Línea vertical (diferencia pequeña en x)
        lineas_verticalesA.append(x1)

# Ordenar y eliminar duplicados
lineas_horizontalesA = sorted(set(lineas_horizontalesA))
lineas_verticalesA = sorted(set(lineas_verticalesA))


# Mostrar la imagen con las líneas de la cuadrícula detectadas (opcional)100, 150, 50
for y in lineas_horizontalesA:
    cv2.line(imagen, (0, y), (imagen.shape[1], y), (255, 255, 0), 2)
for x in lineas_verticalesA:
    cv2.line(imagen, (x, 0), (x, imagen.shape[0]), (255, 255, 0), 2)

'''


contorno, noseusa = cv2.findContours(mask_azul.copy(),1,cv2.CHAIN_APPROX_NONE)
contornos, _ = cv2.findContours(mask_azul.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print(contornos)
cv2.drawContours(imagen, contorno, -1,(255,0,0),3)
if len(contornos) > 0:
    c = max(contorno, key=cv2.contourArea)
    M = cv2.moments(c)

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(imagen, (cx, cy), 8, (0, 0, 255),-1)
    
    i=-1
    for y in lineas_horizontales:
        if cy < y:
            matrizY=i
            break
        i+=1
    i=-1
    for x in lineas_verticales:
        if cx < x:
            matrizX=i
            break
        i+=1
    #print(matrizX)
    #print(matrizY)
    matriz_cuadricula[matrizY][matrizX]=1



### no se que 
# Mostrar la imagen con las líneas de la cuadrícula detectadas (opcional)
for y in lineas_horizontales:
    cv2.line(imagen, (0, y), (imagen.shape[1], y), (0, 255, 0), 2)
for x in lineas_verticales:
    cv2.line(imagen, (x, 0), (x, imagen.shape[0]), (0, 255, 0), 2)

# Procesar cada contorno azul encontrado
for contorno in contornos:
    # Calcular el momento del contorno
    M = cv2.moments(contorno)
    if M['m00'] != 0:
        # Calcular el centroide
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(imagen, (cx, cy), 5, (255, 0, 0), -1)  # Dibujar el centroide en la imagen

        # Determinar la celda de la cuadrícula en la que se encuentra el centroide
        matrizX, matrizY = -1, -1
        for i, y in enumerate(lineas_horizontales):
            if cy < y:
                matrizY = i - 1
                break
        for i, x in enumerate(lineas_verticales):
            if cx < x:
                matrizX = i - 1
                break
        
        if matrizY >= 0 and matrizX >= 0:
            matriz_cuadricula[matrizY][matrizX] = 1  # Marca las celdas con azul en la matriz


contorno, noseusa = cv2.findContours(mask_verde.copy(),1,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imagen, contorno, -1,(255,255,255),3)
if len(contorno) > 0:
    c = max(contorno, key=cv2.contourArea)
    M = cv2.moments(c)

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(imagen, (cx, cy), 8, (0, 0, 255),-1)

    i=-1
    for y in lineas_horizontales:
        if cy < y:
            matrizY=i
            break
        i+=1
    i=-1
    for x in lineas_verticales:
        if cx < x:
            matrizX=i
            break
        i+=1
    #print(matrizX)
    #print(matrizY)
    #matriz_cuadricula[matrizY][matrizX]=3
    finalGreen = [matrizY,matrizX]
 

# Factor de escala (por ejemplo, 0.5 para reducirla a la mitad)
factor_escala = 0.5
# Redimensionamos la imagen
imagen_redimensionada = cv2.resize(imagen, (0, 0), fx=factor_escala, fy=factor_escala)
cv2.imshow('Cuadricula detectada', imagen_redimensionada)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Matriz de la cuadricula:")
print(matriz_cuadricula)

# Guardar la matriz en un archivo de texto
with open("matriz.txt", "w") as archivo:
    for fila in matriz_cuadricula:
        archivo.write(" ".join(map(str, fila)) + "\n")
    print("Matriz guardada")
print(inicioRed)
print(finalGreen)
with open("inicioFin.txt", "w") as archivo:
    archivo.write(" ".join(map(str, inicioRed)) + "\n")
    archivo.write(" ".join(map(str, finalGreen)) + "\n")
    print("incio/fin guardada")