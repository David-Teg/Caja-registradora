# ============================================================
# login.py
# Maneja la ventana de login, registro de usuario y cambio
# de contraseña. Las credenciales se guardan en usuarios.csv
# ============================================================

import os
import hashlib
import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk

USUARIOS_CSV = 'usuarios.csv'

# ============================================================
# --- UTILIDADES ---
# ============================================================

def _hash(password):
    """Convierte la contraseña a un hash SHA-256 para no guardarla en texto plano."""
    return hashlib.sha256(password.encode()).hexdigest()

def _cargar_usuarios():
    """Carga el CSV de usuarios. Si no existe, devuelve DataFrame vacío."""
    if os.path.exists(USUARIOS_CSV):
        return pd.read_csv(USUARIOS_CSV)
    return pd.DataFrame(columns=['usuario', 'password_hash'])

def _guardar_usuarios(df):
    df.to_csv(USUARIOS_CSV, index=False)

def _hay_usuarios():
    df = _cargar_usuarios()
    return not df.empty

def _verificar(usuario, password):
    df = _cargar_usuarios()
    fila = df[df['usuario'] == usuario.strip().lower()]
    if fila.empty:
        return False
    return fila.iloc[0]['password_hash'] == _hash(password)

def _usuario_existe(usuario):
    df = _cargar_usuarios()
    return usuario.strip().lower() in df['usuario'].values


# ============================================================
# --- VENTANA DE LOGIN ---
# ============================================================

def mostrar_login(on_success):
    """
    Muestra la ventana de login.
    - Si no hay usuarios registrados, va directo a la ventana de registro.
    - Si el login es exitoso, llama a on_success() y cierra la ventana.
    """
    if not _hay_usuarios():
        _ventana_registro(on_success, primer_uso=True)
        return

    ventana = Tk()
    ventana.title("Sistema Gastronómico — Iniciar Sesión")
    ventana.geometry("420x320")
    ventana.resizable(False, False)
    ventana.config(bg='#1a1a2e')
    ventana.eval('tk::PlaceWindow . center')

    # Título
    Label(ventana, text="Sistema Gastronómico",
          font=("Arial", 18, "bold"), bg='#1a1a2e', fg='#e0e0e0'
          ).pack(pady=(30, 4))
    Label(ventana, text="Iniciá sesión para continuar",
          font=("Arial", 11), bg='#1a1a2e', fg='#aaaaaa'
          ).pack(pady=(0, 20))

    # Campos
    frame = Frame(ventana, bg='#1a1a2e')
    frame.pack()

    Label(frame, text="Usuario:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=0, column=0, sticky="w", pady=6)
    entry_usuario = Entry(frame, font=("Arial", 12), width=22,
                          bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_usuario.grid(row=0, column=1, padx=10, pady=6)

    Label(frame, text="Contraseña:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=1, column=0, sticky="w", pady=6)
    entry_pass = Entry(frame, font=("Arial", 12), width=22, show="*",
                       bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_pass.grid(row=1, column=1, padx=10, pady=6)

    def intentar_login(event=None):
        usuario = entry_usuario.get().strip()
        password = entry_pass.get()
        if not usuario or not password:
            messagebox.showerror("Error", "Completá usuario y contraseña.", parent=ventana)
            return
        if _verificar(usuario, password):
            ventana.destroy()
            on_success()
        else:
            messagebox.showerror("Acceso denegado",
                                  "Usuario o contraseña incorrectos.", parent=ventana)
            entry_pass.delete(0, END)
            entry_pass.focus()

    # Enter para confirmar
    ventana.bind('<Return>', intentar_login)
    entry_usuario.focus()

    Button(ventana, text="Ingresar", bg='#2ecc71', fg='#0a3d1f',
           font=("Arial", 12, "bold"), width=18,
           command=intentar_login
           ).pack(pady=(20, 8))

    # Link para cambiar contraseña
    Label(ventana, text="¿Olvidaste la contraseña? Contactá al administrador.",
          font=("Arial", 9), bg='#1a1a2e', fg='#aaaaaa').pack()

    ventana.mainloop()


# ============================================================
# --- VENTANA DE REGISTRO ---
# ============================================================

def _ventana_registro(on_success, primer_uso=False):
    """Ventana para crear un nuevo usuario."""
    ventana = Tk()
    ventana.title("Crear usuario")
    ventana.geometry("420x380")
    ventana.resizable(False, False)
    ventana.config(bg='#1a1a2e')
    ventana.eval('tk::PlaceWindow . center')

    titulo = "Bienvenido — Creá tu usuario" if primer_uso else "Crear nuevo usuario"
    Label(ventana, text=titulo,
          font=("Arial", 16, "bold"), bg='#1a1a2e', fg='#e0e0e0'
          ).pack(pady=(30, 4))

    if primer_uso:
        Label(ventana, text="Es la primera vez que abrís el sistema.\nCreá un usuario para continuar.",
              font=("Arial", 10), bg='#1a1a2e', fg='#aaaaaa', justify=CENTER
              ).pack(pady=(0, 16))

    frame = Frame(ventana, bg='#1a1a2e')
    frame.pack()

    Label(frame, text="Usuario:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=0, column=0, sticky="w", pady=6)
    entry_usuario = Entry(frame, font=("Arial", 12), width=22,
                          bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_usuario.grid(row=0, column=1, padx=10, pady=6)

    Label(frame, text="Contraseña:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=1, column=0, sticky="w", pady=6)
    entry_pass = Entry(frame, font=("Arial", 12), width=22, show="*",
                       bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_pass.grid(row=1, column=1, padx=10, pady=6)

    Label(frame, text="Repetir:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=2, column=0, sticky="w", pady=6)
    entry_pass2 = Entry(frame, font=("Arial", 12), width=22, show="*",
                        bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_pass2.grid(row=2, column=1, padx=10, pady=6)

    entry_usuario.focus()

    def confirmar(event=None):
        usuario  = entry_usuario.get().strip().lower()
        password = entry_pass.get()
        password2 = entry_pass2.get()

        if not usuario or not password:
            messagebox.showerror("Error", "Completá todos los campos.", parent=ventana)
            return
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.", parent=ventana)
            return
        if password != password2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=ventana)
            return
        if _usuario_existe(usuario):
            messagebox.showerror("Error", f"El usuario '{usuario}' ya existe.", parent=ventana)
            return

        df = _cargar_usuarios()
        nueva_fila = pd.DataFrame([{'usuario': usuario, 'password_hash': _hash(password)}])
        df = pd.concat([df, nueva_fila], ignore_index=True)
        _guardar_usuarios(df)

        messagebox.showinfo("Listo", f"Usuario '{usuario}' creado correctamente.", parent=ventana)
        ventana.destroy()
        on_success()

    ventana.bind('<Return>', confirmar)

    Button(ventana, text="Crear usuario", bg='#2ecc71', fg='#0a3d1f',
           font=("Arial", 12, "bold"), width=18,
           command=confirmar
           ).pack(pady=(20, 0))

    ventana.mainloop()


# ============================================================
# --- VENTANA DE CAMBIO DE CONTRASEÑA ---
# ============================================================

def ventana_cambiar_password(parent=None):
    """
    Abre una ventana para cambiar la contraseña de un usuario existente.
    Se puede llamar desde cualquier parte del programa.
    """
    if not _hay_usuarios():
        messagebox.showwarning("Sin usuarios", "No hay usuarios registrados.")
        return

    ventana = Toplevel(parent) if parent else Tk()
    ventana.title("Cambiar contraseña")
    ventana.geometry("420x380")
    ventana.resizable(False, False)
    ventana.config(bg='#1a1a2e')
    if parent:
        ventana.grab_set()

    Label(ventana, text="Cambiar contraseña",
          font=("Arial", 16, "bold"), bg='#1a1a2e', fg='#e0e0e0'
          ).pack(pady=(30, 20))

    frame = Frame(ventana, bg='#1a1a2e')
    frame.pack()

    Label(frame, text="Usuario:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=0, column=0, sticky="w", pady=6)
    entry_usuario = Entry(frame, font=("Arial", 12), width=22,
                          bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_usuario.grid(row=0, column=1, padx=10, pady=6)

    Label(frame, text="Contraseña actual:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=1, column=0, sticky="w", pady=6)
    entry_actual = Entry(frame, font=("Arial", 12), width=22, show="*",
                         bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_actual.grid(row=1, column=1, padx=10, pady=6)

    Label(frame, text="Nueva contraseña:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=2, column=0, sticky="w", pady=6)
    entry_nueva = Entry(frame, font=("Arial", 12), width=22, show="*",
                        bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_nueva.grid(row=2, column=1, padx=10, pady=6)

    Label(frame, text="Repetir nueva:", font=("Arial", 11),
          bg='#1a1a2e', fg='#e0e0e0').grid(row=3, column=0, sticky="w", pady=6)
    entry_nueva2 = Entry(frame, font=("Arial", 12), width=22, show="*",
                         bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_nueva2.grid(row=3, column=1, padx=10, pady=6)

    entry_usuario.focus()

    def confirmar():
        usuario   = entry_usuario.get().strip().lower()
        actual    = entry_actual.get()
        nueva     = entry_nueva.get()
        nueva2    = entry_nueva2.get()

        if not all([usuario, actual, nueva, nueva2]):
            messagebox.showerror("Error", "Completá todos los campos.", parent=ventana)
            return
        if not _verificar(usuario, actual):
            messagebox.showerror("Error", "Usuario o contraseña actual incorrectos.", parent=ventana)
            return
        if len(nueva) < 4:
            messagebox.showerror("Error", "La nueva contraseña debe tener al menos 4 caracteres.", parent=ventana)
            return
        if nueva != nueva2:
            messagebox.showerror("Error", "Las nuevas contraseñas no coinciden.", parent=ventana)
            return

        df = _cargar_usuarios()
        df.loc[df['usuario'] == usuario, 'password_hash'] = _hash(nueva)
        _guardar_usuarios(df)
        messagebox.showinfo("Listo", "Contraseña actualizada correctamente.", parent=ventana)
        ventana.destroy()

    Button(ventana, text="Cambiar contraseña", bg='#2ecc71', fg='#0a3d1f',
           font=("Arial", 12, "bold"), width=18,
           command=confirmar
           ).pack(pady=(20, 0))

    if not parent:
        ventana.mainloop()
