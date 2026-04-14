import tkinter as tk
from tkinter import ttk


class CarreraView:
    """
    Vista del juego.
    Se encarga de construir la interfaz gráfica y de mostrar
    visualmente la carrera sobre un Canvas.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Hilos 2D - Carrera MVC con Tkinter")
        self.root.geometry("980x560")
        self.root.resizable(False, False)

        # Referencias a elementos visuales.
        self.canvas = None
        self.lbl_estado = None
        self.btn_iniciar = None
        self.btn_reiniciar = None

        # Diccionarios para relacionar cada corredor con su figura y texto.
        self.figuras = {}
        self.textos = {}
        self.lane_y = {}

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Construye la ventana y sus controles."""
        marco_superior = ttk.Frame(self.root, padding=10)
        marco_superior.pack(fill="x")

        titulo = ttk.Label(
            marco_superior,
            text="Carrera de Hilos en Python",
            font=("Arial", 18, "bold")
        )
        titulo.pack(side="left")

        botones = ttk.Frame(marco_superior)
        botones.pack(side="right")

        self.btn_iniciar = ttk.Button(botones, text="Iniciar carrera")
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_reiniciar = ttk.Button(botones, text="Reiniciar")
        self.btn_reiniciar.pack(side="left", padx=5)

        self.lbl_estado = ttk.Label(
            self.root,
            text="Presione 'Iniciar carrera' para comenzar.",
            font=("Arial", 11)
        )
        self.lbl_estado.pack(fill="x", padx=10, pady=(0, 8))

        # Canvas principal donde se dibuja la carrera.
        self.canvas = tk.Canvas(
            self.root,
            width=940,
            height=430,
            bg="#e9f5ff",
            highlightthickness=1,
            highlightbackground="#9bb7d4"
        )
        self.canvas.pack(padx=20, pady=10)

    def dibujar_escena(self, carrera):
        """
        Dibuja la pista, la meta y los corredores.
        """
        self.canvas.delete("all")
        self.figuras.clear()
        self.textos.clear()
        self.lane_y.clear()

        # Fondo tipo pista.
        self.canvas.create_rectangle(20, 20, 900, 390, fill="#f7f7f7", outline="#cccccc")

        # Línea de salida.
        self.canvas.create_line(60, 30, 60, 380, fill="black", width=3)
        self.canvas.create_text(60, 12, text="Salida", font=("Arial", 10, "bold"))

        # Línea de meta.
        x_meta = 60 + carrera.meta
        self.canvas.create_line(x_meta, 30, x_meta, 380, fill="red", width=3)
        self.canvas.create_text(x_meta, 12, text="Meta", font=("Arial", 10, "bold"), fill="red")

        # Líneas horizontales de carriles.
        for y in [90, 170, 250, 330]:
            self.canvas.create_line(30, y + 25, 900, y + 25, fill="#d0d0d0", dash=(6, 3))

        # Dibujo de corredores.
        posiciones_y = [70, 150, 230, 310]

        for corredor, y in zip(carrera.corredores, posiciones_y):
            self.lane_y[corredor.nombre] = y

            # Etiqueta del corredor.
            self.canvas.create_text(40, y + 15, text=corredor.nombre, font=("Arial", 10, "bold"))

            # Figura principal del corredor.
            figura = self.canvas.create_oval(70, y, 110, y + 30, fill=corredor.color, outline="black")

            # Texto con la distancia recorrida.
            texto = self.canvas.create_text(130, y + 15, text="0 m", anchor="w", font=("Arial", 10))

            self.figuras[corredor.nombre] = figura
            self.textos[corredor.nombre] = texto

    def actualizar_corredor(self, nombre, posicion):
        """
        Mueve visualmente al corredor en el canvas y actualiza su texto.
        """
        if nombre not in self.figuras:
            return

        figura = self.figuras[nombre]
        texto = self.textos[nombre]
        y = self.lane_y[nombre]

        # La posición visual parte desde x = 70.
        x1 = 70 + posicion
        x2 = 110 + posicion

        self.canvas.coords(figura, x1, y, x2, y + 30)
        self.canvas.coords(texto, x2 + 15, y + 15)
        self.canvas.itemconfig(texto, text=f"{posicion} m")

    def mostrar_estado(self, mensaje):
        """Actualiza la etiqueta de estado."""
        self.lbl_estado.config(text=mensaje)

    def desactivar_inicio(self):
        """Desactiva el botón de inicio mientras la carrera está en curso."""
        self.btn_iniciar.config(state="disabled")

    def activar_inicio(self):
        """Activa nuevamente el botón de inicio."""
        self.btn_iniciar.config(state="normal")

    def marcar_ganador(self, nombre):
        """
        Resalta al ganador en pantalla.
        """
        if nombre in self.figuras:
            figura = self.figuras[nombre]
            self.canvas.itemconfig(figura, width=4)
