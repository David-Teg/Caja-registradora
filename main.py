# ============================================================
# main.py
# Punto de entrada del programa.
# Solo crea la ventana principal y arranca la aplicación.
# Para ejecutar el programa: python main.py
# ============================================================

from tkinter import Tk
from interfaz import construir_interfaz


def main():
    # Crear la ventana principal
    aplicacion = Tk()
    aplicacion.geometry('1280x720')
    aplicacion.title('Mi Restaurante - Sistema Gastronómico')
    aplicacion.config(bg='#1a1a2e')

    # Construir toda la interfaz dentro de esa ventana
    construir_interfaz(aplicacion)

    # Guardar mozos automáticamente al cerrar la ventana
    def al_cerrar():
        from logica import guardar_mozos
        guardar_mozos()
        aplicacion.destroy()

    aplicacion.protocol("WM_DELETE_WINDOW", al_cerrar)

    # Mantener la ventana abierta
    aplicacion.mainloop()


if __name__ == '__main__':
    main()