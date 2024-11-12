import tkinter as tk
from tkinter import messagebox

class GridBuilder:
    def __init__(self, root, rows=6, cols=6):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.start = None
        self.end = None
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.create_grid()
        self.inicio = [-1,-1]
        self.final = [-1,-1]

    def create_grid(self):
        # Crear botones en forma de cuadrícula
        for i in range(self.rows):
            for j in range(self.cols):
                button = tk.Button(self.root, width=4, height=2,
                                   command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        # Instrucciones y selección de modo
        self.mode = tk.StringVar(value="start")
        self.create_mode_selector()

    def create_mode_selector(self):
        # Crear botones de selección de modo
        modes_frame = tk.Frame(self.root)
        modes_frame.grid(row=self.rows, column=0, columnspan=self.cols)

        # Radio botones para elegir el tipo de celda
        tk.Radiobutton(modes_frame, text="Inicio (Rojo)", variable=self.mode, value="start").pack(side=tk.LEFT)
        tk.Radiobutton(modes_frame, text="Final (Verde)", variable=self.mode, value="end").pack(side=tk.LEFT)
        tk.Radiobutton(modes_frame, text="Obstáculo (Azul)", variable=self.mode, value="obstacle").pack(side=tk.LEFT)
        tk.Radiobutton(modes_frame, text="Limpiar", variable=self.mode, value="clear").pack(side=tk.LEFT)

    def on_click(self, i, j):
        mode = self.mode.get()

        # Asignar color y valor en la matriz según el modo seleccionado
        if mode == "start":
            if self.start:
                prev_i, prev_j = self.start
                self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.grid[prev_i][prev_j] = 0
            self.buttons[i][j].config(bg="red")
            #self.grid[i][j] = "S"
            self.start = (i, j)
            self.inicio=[i,j]

        elif mode == "end":
            if self.end:
                prev_i, prev_j = self.end
                self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.grid[prev_i][prev_j] = 0
            self.buttons[i][j].config(bg="green")
            #self.grid[i][j] = "E"
            self.end = (i, j)
            self.final=[i,j]

        elif mode == "obstacle":
            self.buttons[i][j].config(bg="blue")
            self.grid[i][j] = 1
# Guardar la matriz en un archivo de texto
            with open("matriz.txt", "w") as archivo:
                for fila in self.grid:
                    archivo.write(" ".join(map(str, fila)) + "\n")
                print("Matriz guardada")

        elif mode == "clear":
            self.buttons[i][j].config(bg="SystemButtonFace")
            if (i, j) == self.start:
                self.start = None
            elif (i, j) == self.end:
                self.end = None
            self.grid[i][j] = 0

        print(self.final)
        print(self.inicio)
        with open("inicioFin.txt", "w") as archivo:
            archivo.write(" ".join(map(str, self.inicio)) + "\n")
            archivo.write(" ".join(map(str, self.final)) + "\n")
            print("incio/fin guardada")

    def get_grid(self):
        return self.grid

# Crear ventana de Tkinter y ejecutar la aplicación
root = tk.Tk()
root.title("Construccion de Matriz de Obstaculos")

app = GridBuilder(root)
root.mainloop()