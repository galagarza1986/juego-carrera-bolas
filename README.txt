Juego 2D con hilos en Python usando tkinter y MVC.

Estructura:
- model/
- view/
- controller/
- main.py

Descripción:
Se trata de una carrera visual de varios corredores.
Cada corredor avanza en su propio hilo.
La interfaz gráfica se construye con tkinter sobre un Canvas.

Puntos didácticos:
- Creación de hilos con threading
- Múltiples hilos
- Sincronización con Lock
- Uso de Queue para comunicar hilos con la interfaz
- Organización básica con MVC

Importante:
En tkinter no se recomienda modificar la interfaz directamente
desde hilos secundarios. Por eso este proyecto usa una cola (Queue)
y el método after() para actualizar la ventana desde el hilo principal.
