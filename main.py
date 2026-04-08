# ============================================================
# main.py
# Punto de entrada del programa.
# Muestra el login antes de abrir el sistema principal.
# ============================================================

from login import mostrar_login


def main():
    def iniciar_sistema():
        from tkinter import Tk
        from interfaz import construir_interfaz

        aplicacion = Tk()
        aplicacion.geometry('1280x720')
        aplicacion.title('Mi Restaurante - Sistema Gastronómico')
        aplicacion.config(bg='#1a1a2e')

        construir_interfaz(aplicacion)

        def al_cerrar():
            from logica import guardar_mozos
            guardar_mozos()
            aplicacion.destroy()

        aplicacion.protocol("WM_DELETE_WINDOW", al_cerrar)
        aplicacion.mainloop()

    # Mostrar login primero. Si es exitoso, llama a iniciar_sistema()
    mostrar_login(iniciar_sistema)


if __name__ == '__main__':
    main()
