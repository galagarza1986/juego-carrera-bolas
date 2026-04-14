import random
import threading
import time
from queue import Queue, Empty


class CarreraController:
    """
    Controlador del juego.
    Coordina la lógica entre el modelo y la vista.

    También maneja:
    - la creación de hilos
    - la sincronización con Lock
    - la cola de eventos hacia tkinter
    """

    def __init__(self, carrera, vista):
        self.carrera = carrera
        self.vista = vista

        # Lock para proteger la sección crítica.
        self.lock = threading.Lock()

        # Cola para enviar eventos desde los hilos hacia la interfaz.
        self.eventos = Queue()

        # Lista de hilos creados.
        self.hilos = []

        # Bandera de control.
        self.detener = False

        self._configurar_vista()

    def _configurar_vista(self):
        """Conecta botones y dibuja la escena inicial."""
        self.vista.btn_iniciar.config(command=self.iniciar_carrera)
        self.vista.btn_reiniciar.config(command=self.reiniciar_carrera)
        self.vista.dibujar_escena(self.carrera)

        # after() permite revisar periódicamente la cola
        # desde el hilo principal de tkinter.
        self.vista.root.after(50, self.procesar_eventos)

    def procesar_eventos(self):
        """
        Atiende los eventos enviados por los hilos.

        Esta función se ejecuta repetidamente en el hilo principal de tkinter,
        lo cual evita actualizar la interfaz directamente desde hilos secundarios.
        """
        try:
            while True:
                evento = self.eventos.get_nowait()
                tipo = evento["tipo"]

                if tipo == "avance":
                    self.vista.actualizar_corredor(evento["nombre"], evento["posicion"])

                elif tipo == "estado":
                    self.vista.mostrar_estado(evento["mensaje"])

                elif tipo == "ganador":
                    self.vista.marcar_ganador(evento["nombre"])
                    self.vista.mostrar_estado(f"Ganó {evento['nombre']} la carrera.")
                    self.vista.activar_inicio()

        except Empty:
            pass

        # Se vuelve a programar la revisión de la cola.
        self.vista.root.after(50, self.procesar_eventos)

    def worker_corredor(self, corredor):
        """
        Función que ejecuta cada hilo.
        Cada corredor avanza en intervalos aleatorios y con pasos aleatorios.
        """
        while True:
            time.sleep(random.uniform(0.08, 0.25))

            with self.lock:
                # Si ya se pidió detener o ya existe un ganador, el hilo termina.
                if self.detener or self.carrera.ganador is not None:
                    break

                avance = random.randint(3, 15)
                corredor.posicion += avance

                # No permitimos que sobrepase demasiado la meta visual.
                if corredor.posicion > self.carrera.meta:
                    corredor.posicion = self.carrera.meta

                # Enviamos el cambio a la interfaz.
                self.eventos.put({
                    "tipo": "avance",
                    "nombre": corredor.nombre,
                    "posicion": corredor.posicion
                })

                # Si llegó a la meta y no había ganador, se declara ganador.
                if corredor.posicion >= self.carrera.meta and self.carrera.ganador is None:
                    self.carrera.ganador = corredor
                    self.carrera.en_curso = False

                    self.eventos.put({
                        "tipo": "ganador",
                        "nombre": corredor.nombre
                    })
                    break

    def iniciar_carrera(self):
        """
        Inicia la carrera creando un hilo por corredor.
        """
        if self.carrera.en_curso:
            return

        self.carrera.reiniciar()
        self.detener = False
        self.hilos.clear()
        self.carrera.en_curso = True

        self.vista.dibujar_escena(self.carrera)
        self.vista.desactivar_inicio()
        self.eventos.put({
            "tipo": "estado",
            "mensaje": "Carrera iniciada. Los hilos están avanzando..."
        })

        for corredor in self.carrera.corredores:
            hilo = threading.Thread(target=self.worker_corredor, args=(corredor,), daemon=True)
            self.hilos.append(hilo)
            hilo.start()

    def reiniciar_carrera(self):
        """
        Reinicia la carrera y la interfaz.
        """
        self.detener = True
        self.carrera.reiniciar()
        self.vista.dibujar_escena(self.carrera)
        self.vista.activar_inicio()
        self.eventos.put({
            "tipo": "estado",
            "mensaje": "Carrera reiniciada. Lista para iniciar nuevamente."
        })
