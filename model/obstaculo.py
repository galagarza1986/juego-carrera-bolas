class Obstaculo:
    """
    Modelo que representa a un obstaculo dentro del juego.
    Guarda su nombre, categoria y posición actual.
    """

    def __init__(self, nombre: str, categoria: str):
        self.nombre = nombre
        self.categoria = categoria
        self.posicion = 0

    def reiniciar(self):
        """Vuelve la posición del obstaculo a cero."""
        self.posicion = 0
