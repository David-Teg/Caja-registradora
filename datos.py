# ============================================================
# datos.py
# Contiene todos los datos del sistema: listas de productos,
# precios, mesas y mozos. Si querés cambiar un precio o
# agregar un producto, usá la pestaña Menú del programa.
# ============================================================

import pandas as pd
import os

# --- MENÚ DINÁMICO ---
# Los productos se guardan en menu.csv con columnas: nombre, precio, categoria
# Si el archivo no existe, se crea con los productos por defecto.

MENU_CSV = 'menu.csv'

MENU_DEFAULT = {
    'nombre':    ['pollo', 'cerdo', 'vacio', 'longitas', 'pizza', 'lazaña', 'spaguetti', 'milanesa',
                  'coca cola', 'agua saborizada', 'agua', 'vino tinto', 'vino blanco', 'cerveza', 'chop', 'exprimido',
                  'flan', 'budin', 'torta', 'helado', 'fruta', 'yogur', 'queso', 'batata'],
    'precio':    [1.32, 1.65, 2.31, 3.22, 1.22, 1.99, 2.05, 2.65,
                  0.25, 0.99, 1.21, 1.54, 1.08, 1.10, 2.00, 1.58,
                  1.54, 1.68, 1.32, 1.97, 2.55, 2.14, 1.94, 1.74],
    'categoria': ['comida'] * 8 + ['bebida'] * 8 + ['postre'] * 8
}

def cargar_menu():
    """Carga el menú desde menu.csv. Si no existe, lo crea con los productos por defecto."""
    if os.path.exists(MENU_CSV):
        return pd.read_csv(MENU_CSV)
    df = pd.DataFrame(MENU_DEFAULT)
    df.to_csv(MENU_CSV, index=False)
    return df

df_menu = cargar_menu()

def get_productos(categoria):
    """Devuelve listas de nombres y precios para una categoría."""
    filtro = df_menu[df_menu['categoria'] == categoria]
    return filtro['nombre'].tolist(), filtro['precio'].tolist()

# Propiedades de acceso rápido (compatibilidad con el resto del código)
@property
def lista_comida_prop():
    return get_productos('comida')[0]

def _get_lista(cat):
    return df_menu[df_menu['categoria'] == cat]['nombre'].tolist()

def _get_precios(cat):
    return df_menu[df_menu['categoria'] == cat]['precio'].tolist()

# --- MESAS ---
mesas_data = {
    "Mesa":   [1, 2, 3, 4, 5],
    "Estado": ["Libre", "Libre", "Libre", "Libre", "Libre"],
    "Mozo":   ["-", "-", "-", "-", "-"]
}
df_mesas = pd.DataFrame(mesas_data)

# --- HISTORIAL DE PEDIDOS ---
HISTORIAL_CSV = 'historial.csv'
HISTORIAL_COLUMNAS = ['Fecha', 'Hora', 'Recibo', 'Mesa', 'Mozo', 'Subtotal', 'Impuestos', 'Total']

def cargar_historial():
    if os.path.exists(HISTORIAL_CSV):
        return pd.read_csv(HISTORIAL_CSV)
    return pd.DataFrame(columns=HISTORIAL_COLUMNAS)

df_historial = cargar_historial()

# --- MOZOS PERSISTENTES ---
MOZOS_CSV = 'mozos.csv'

def cargar_mozos():
    if os.path.exists(MOZOS_CSV):
        df = pd.read_csv(MOZOS_CSV)
        if df.empty:
            return [], 1
        return list(df.itertuples(index=False, name=None)), int(df['ID'].max()) + 1
    return [], 1

mozos, contador_id_mozo = cargar_mozos()
