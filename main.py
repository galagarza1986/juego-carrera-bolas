import tkinter as tk

from model.corredor import Corredor
from model.carrera import Carrera
from view.carrera_view import CarreraView
from controller.carrera_controller import CarreraController


def main():
    """
    Punto de entrada del programa.

    Aquí se construyen:
    - el modelo principal
    - los corredores
    - la vista
    - el controlador
    """
    root = tk.Tk()

    # Modelo principal.
    carrera = Carrera(meta=760)

    # Corredores del juego.
    carrera.agregar_corredor(Corredor("Rojo", "#e74c3c"))
    carrera.agregar_corredor(Corredor("Azul", "#3498db"))
    carrera.agregar_corredor(Corredor("Verde", "#27ae60"))
    carrera.agregar_corredor(Corredor("Amarillo", "#f1c40f"))

    # Vista.
    vista = CarreraView(root)

    # Controlador.
    CarreraController(carrera, vista)

    root.mainloop()


if __name__ == "__main__":
    main()
