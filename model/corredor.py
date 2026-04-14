class Corredor:
    """
    Modelo que representa a un corredor dentro del juego.
    Guarda su nombre, color y posición actual.
    """

    def __init__(self, nombre: str, color: str):
        self.nombre = nombre
        self.color = color
        self.posicion = 0

    def reiniciar(self):
        """Vuelve la posición del corredor a cero."""
        self.posicion = 0
