import serial
import time
import keyboard

# Leer el archivo comandos.txt y guardar en una lista
with open("comandos.txt", "r") as file:
    commands = [line.strip() for line in file]

# Configuración del puerto serial
puerto_serial = 'COM12'  # Cambiar según tu configuración
velocidad_baudios = 9600
dato = 0

try:
    # Abrir el puerto serial
    conexion = serial.Serial(puerto_serial, velocidad_baudios)
    print(f"Conectado a {puerto_serial} a {velocidad_baudios} baudios.")
    time.sleep(2)  # Esperar a que la conexión se establezca

    print("Presiona 'q' para salir.")
    i = 1
    ordenesLen = len(commands) // 2

    while True:
        if keyboard.is_pressed('q'):  # Presionar 'q' para salir
            print("Terminando la conexión.")
            break

        if keyboard.is_pressed('w'):  # Iniciar el proceso
            print("Inicio.")
            print(f"i: {i}")
            print(f"dato: {dato}")
            dato = 1
            time.sleep(0.1)

        if keyboard.is_pressed('e'):
            print(f"i: {i}")
            print(f"dato: {dato}")
            time.sleep(0.1)

        if keyboard.is_pressed('m'):
            dato += 2
            print(f"i: {i}")
            print(f"dato: {dato}")

        # Leer línea de datos desde el Bluetooth
        if conexion.in_waiting > 0:
            dato = conexion.readline().decode('utf-8').strip()
            print("Dato recibido:", dato)

        # Verificar que 'i' esté dentro del rango antes de acceder a 'commands'
        if str(dato) == str(i) and i < len(commands):
            print("COMANDO")
            if i - 1 < len(commands):
                print(commands[i - 1])
            if i < len(commands):
                print(commands[i])
                envio = commands[i]
                conexion.write(envio.encode())
            
            i += 2

            # Reiniciar si hemos llegado al final de los comandos
            if i >= len(commands):
                print("Todos los comandos ejecutados. Reiniciando...")
                i = 1
                dato = 0

        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Error de conexión serial: {e}")

finally:
    if 'conexion' in locals() and conexion.is_open:
        conexion.close()
        print("Conexión cerrada.")
