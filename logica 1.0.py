# ============================================================
# logica.py
# Contiene todas las funciones que hacen cálculos o modifican
# datos: calculadora, pedidos, recibo, mozos y mesas.
# La interfaz llama a estas funciones cuando el usuario
# hace clic en un botón.
# ============================================================

import random
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog, END, Toplevel, StringVar
from tkinter import ttk

import datos


# ============================================================
# --- MENÚ (Tab Menú) ---
# ============================================================

def agregar_producto(entry_nombre, entry_precio, combo_categoria, tabla_menu):
    """Agrega un nuevo producto al menú."""
    nombre    = entry_nombre.get().strip().lower()
    precio_str = entry_precio.get().strip()
    categoria = combo_categoria.get()

    if not nombre:
        messagebox.showerror("Error", "El nombre no puede estar vacío.")
        return
    try:
        precio = float(precio_str)
        if precio <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número mayor a 0.")
        return

    if nombre in datos.df_menu['nombre'].values:
        messagebox.showerror("Error", f"Ya existe un producto llamado '{nombre}'.")
        return

    import pandas as pd
    nueva_fila = pd.DataFrame([{'nombre': nombre, 'precio': precio, 'categoria': categoria}])
    datos.df_menu = pd.concat([datos.df_menu, nueva_fila], ignore_index=True)
    datos.df_menu.to_csv(datos.MENU_CSV, index=False)
    actualizar_tabla_menu(tabla_menu)
    entry_nombre.delete(0, END)
    entry_precio.delete(0, END)


def editar_producto(tabla_menu):
    """Edita el nombre y precio del producto seleccionado."""
    from tkinter import Toplevel, Label, Entry, Button, StringVar
    selected = tabla_menu.selection()
    if not selected:
        messagebox.showwarning("Atención", "Seleccioná un producto para editar.")
        return

    valores = tabla_menu.item(selected, "values")
    nombre_viejo = valores[0]
    precio_viejo = valores[1]
    cat_vieja    = valores[2]

    ventana = Toplevel()
    ventana.title("Editar Producto")
    ventana.geometry("300x220")
    ventana.grab_set()
    ventana.config(bg='#1a1a2e')

    Label(ventana, text="Nombre:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(15, 2))
    entry_nombre = Entry(ventana, font=("Arial", 12), width=20,
                         bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_nombre.insert(0, nombre_viejo)
    entry_nombre.pack()

    Label(ventana, text="Precio:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(10, 2))
    entry_precio = Entry(ventana, font=("Arial", 12), width=20,
                         bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_precio.insert(0, str(precio_viejo))
    entry_precio.pack()

    def confirmar():
        nuevo_nombre = entry_nombre.get().strip().lower()
        nuevo_precio_str = entry_precio.get().strip()
        if not nuevo_nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número mayor a 0.")
            return

        datos.df_menu.loc[datos.df_menu['nombre'] == nombre_viejo.lower(), ['nombre', 'precio']] = [nuevo_nombre, nuevo_precio]
        datos.df_menu.to_csv(datos.MENU_CSV, index=False)
        actualizar_tabla_menu(tabla_menu)
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    Button(ventana, text="Confirmar", bg="#2ecc71", fg="#0a3d1f", command=confirmar).pack(side="left", padx=25, pady=15)
    Button(ventana, text="Cancelar",  bg="#e94560", fg="#e0e0e0", command=cancelar).pack(side="right", padx=25, pady=15)
    ventana.wait_window()


def eliminar_producto(tabla_menu):
    """Elimina el producto seleccionado del menú."""
    selected = tabla_menu.selection()
    if not selected:
        messagebox.showwarning("Atención", "Seleccioná un producto para eliminar.")
        return
    nombre = tabla_menu.item(selected, "values")[0]
    if messagebox.askyesno("Eliminar", f"¿Seguro que querés eliminar '{nombre}'?"):
        datos.df_menu = datos.df_menu[datos.df_menu['nombre'] != nombre].reset_index(drop=True)
        datos.df_menu.to_csv(datos.MENU_CSV, index=False)
        actualizar_tabla_menu(tabla_menu)


def actualizar_tabla_menu(tabla_menu):
    """Recarga la tabla del menú con los datos actuales."""
    for item in tabla_menu.get_children():
        tabla_menu.delete(item)
    for _, row in datos.df_menu.iterrows():
        tabla_menu.insert("", "end", values=(row['nombre'].title(), row['precio'], row['categoria']))



# ============================================================
# --- CALCULADORA ---
# ============================================================

# 'operador' guarda la operación que se va armando
# por ejemplo: "12+5" o "3*4"
operador = ''

def click_boton(numero, visor_calculadora):
    global operador
    operador = operador + numero
    visor_calculadora.delete(0, END)
    visor_calculadora.insert(END, operador)

def borrar(visor_calculadora):
    global operador
    operador = ''
    visor_calculadora.delete(0, END)

def obtener_resultado(visor_calculadora):
    global operador
    try:
        resultado = str(eval(operador))
        visor_calculadora.delete(0, END)
        visor_calculadora.insert(0, resultado)
        operador = ''
    except Exception:
        messagebox.showerror('Error', 'Operación inválida')
        operador = ''
        visor_calculadora.delete(0, END)


# ============================================================
# --- PEDIDOS (Tab Restaurante) ---
# ============================================================

def revisar_check(variables_comida, cuadros_comida, texto_comida,
                  variables_bebidas, cuadros_bebidas, texto_bebidas,
                  variables_postres, cuadros_postres, texto_postres):
    """
    Se ejecuta cada vez que el usuario tilda o destilda un checkbox.
    Si está tildado: habilita el campo de cantidad.
    Si no está tildado: deshabilita el campo y lo pone en '0'.
    """
    from tkinter import NORMAL, DISABLED

    for x, cuadro in enumerate(cuadros_comida):
        if variables_comida[x].get() == 1:
            cuadro.config(state=NORMAL)
            if cuadro.get() == '0':
                cuadro.delete(0, END)
            cuadro.focus()
        else:
            cuadro.config(state=DISABLED)
            texto_comida[x].set('0')

    for x, cuadro in enumerate(cuadros_bebidas):
        if variables_bebidas[x].get() == 1:
            cuadro.config(state=NORMAL)
            if cuadro.get() == '0':
                cuadro.delete(0, END)
            cuadro.focus()
        else:
            cuadro.config(state=DISABLED)
            texto_bebidas[x].set('0')

    for x, cuadro in enumerate(cuadros_postres):
        if variables_postres[x].get() == 1:
            cuadro.config(state=NORMAL)
            if cuadro.get() == '0':
                cuadro.delete(0, END)
            cuadro.focus()
        else:
            cuadro.config(state=DISABLED)
            texto_postres[x].set('0')


def _leer_cantidad(valor):
    """
    Convierte el texto de un campo de cantidad a número entero.
    Devuelve el número, o None si el valor no es válido.
    Un valor válido es un número entero mayor o igual a 1.
    """
    try:
        numero = int(valor)
        if numero < 1:
            return None
        return numero
    except ValueError:
        return None


def calcular_total(texto_comida, texto_bebidas, texto_postres,
                   variables_comida, variables_bebidas, variables_postres,
                   var_costo_comida, var_costo_bebidas, var_costo_postres,
                   var_subtotal, var_impuestos, var_total):
    """
    Recorre todas las cantidades ingresadas, multiplica por los precios
    y calcula: subtotal, impuestos (21%) y total.
    Solo valida y suma los ítems que tienen el checkbox tildado.
    Si una cantidad tildada es inválida (letras, 0, negativo),
    muestra un mensaje de error y cancela el cálculo.
    Devuelve True si el cálculo fue exitoso, False si hubo un error.
    """
    sub_total_comida = 0
    for p, cantidad in enumerate(texto_comida):
        if variables_comida[p].get() == 0:  # no tildado, se omite
            continue
        num = _leer_cantidad(cantidad.get())
        if num is None:
            messagebox.showerror(
                'Cantidad inválida',
                f'La cantidad de "{datos.df_menu[datos.df_menu["categoria"]=="comida"]["nombre"].iloc[p]}" no es válida.\n'
                f'Ingresá un número entero mayor o igual a 1.'
            )
            return False
        sub_total_comida += num * datos.df_menu[datos.df_menu["categoria"]=="comida"]["precio"].iloc[p]
    print(sub_total_comida)  # debug - eliminar cuando todo esté OK

    sub_total_bebidas = 0
    for p, cantidad in enumerate(texto_bebidas):
        if variables_bebidas[p].get() == 0:  # no tildado, se omite
            continue
        num = _leer_cantidad(cantidad.get())
        if num is None:
            messagebox.showerror(
                'Cantidad inválida',
                f'La cantidad de "{datos.df_menu[datos.df_menu["categoria"]=="bebida"]["nombre"].iloc[p]}" no es válida.\n'
                f'Ingresá un número entero mayor o igual a 1.'
            )
            return False
        sub_total_bebidas += num * datos.df_menu[datos.df_menu["categoria"]=="bebida"]["precio"].iloc[p]
    print(sub_total_bebidas)  # debug

    sub_total_postre = 0
    for p, cantidad in enumerate(texto_postres):
        if variables_postres[p].get() == 0:  # no tildado, se omite
            continue
        num = _leer_cantidad(cantidad.get())
        if num is None:
            messagebox.showerror(
                'Cantidad inválida',
                f'La cantidad de "{datos.df_menu[datos.df_menu["categoria"]=="postre"]["nombre"].iloc[p]}" no es válida.\n'
                f'Ingresá un número entero mayor o igual a 1.'
            )
            return False
        sub_total_postre += num * datos.df_menu[datos.df_menu["categoria"]=="postre"]["precio"].iloc[p]
    print(sub_total_postre)  # debug

    sub_total = sub_total_comida + sub_total_bebidas + sub_total_postre
    impuestos  = sub_total * 0.21
    total      = sub_total + impuestos

    var_costo_comida.set(f'${round(sub_total_comida, 2)}')
    var_costo_bebidas.set(f'${round(sub_total_bebidas, 2)}')
    var_costo_postres.set(f'${round(sub_total_postre, 2)}')
    var_subtotal.set(f'{round(sub_total, 2)}')
    var_impuestos.set(f'{round(impuestos, 2)}')
    var_total.set(f'{round(total, 2)}')
    return True


def _seleccionar_mesa():
    """
    Muestra una ventana emergente con las mesas ocupadas para que
    el usuario elija a cuál pertenece el pedido.
    Devuelve una tupla (numero_mesa, nombre_mozo) o (None, None) si cancela
    o si no hay mesas ocupadas.
    """
    mesas_ocupadas = datos.df_mesas[datos.df_mesas["Estado"] == "Ocupada"]

    if mesas_ocupadas.empty:
        messagebox.showwarning(
            "Sin mesas ocupadas",
            "No hay mesas ocupadas.\nOcupá una mesa en la pestaña Mesas antes de generar el recibo."
        )
        return None, None

    # Armar las opciones: "Mesa 3 - Mozo: Juan"
    opciones = [
        f"Mesa {row['Mesa']} - Mozo: {row['Mozo']}"
        for _, row in mesas_ocupadas.iterrows()
    ]

    resultado = {"mesa": None, "mozo": None}

    ventana = Toplevel()
    ventana.title("Seleccionar Mesa")
    ventana.geometry("320x160")
    ventana.grab_set()
    ventana.config(bg='#1a1a2e')

    from tkinter import Label, Button
    Label(ventana, text="¿A qué mesa pertenece este pedido?",
          font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=12)

    var_seleccion = StringVar()
    combo = ttk.Combobox(ventana, textvariable=var_seleccion,
                         values=opciones, state="readonly", width=35)
    combo.current(0)
    combo.pack(pady=5)

    def confirmar():
        seleccion = var_seleccion.get()  # "Mesa 3 - Mozo: Juan"
        partes    = seleccion.split(" - Mozo: ")
        resultado["mesa"] = partes[0].replace("Mesa ", "")
        resultado["mozo"] = partes[1]
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    Button(ventana, text="Confirmar", bg="#2ecc71", fg="#0a3d1f", command=confirmar).pack(side="left", padx=30, pady=10)
    Button(ventana, text="Cancelar",  bg="#e94560", fg="#e0e0e0",     command=cancelar).pack(side="right", padx=30, pady=10)

    ventana.wait_window()
    return resultado["mesa"], resultado["mozo"]


def _guardar_en_historial(num_recibo, fecha, mesa, mozo,
                           var_subtotal, var_impuestos, var_total,
                           tabla_historial=None):
    """
    Agrega una fila al DataFrame de historial y la persiste en historial.csv.
    Si se pasa tabla_historial (el widget de la pestaña), también actualiza la vista.
    """
    import pandas as pd

    nueva_fila = pd.DataFrame([{
        'Fecha':     f'{fecha.day}/{fecha.month}/{fecha.year}',
        'Hora':      f'{fecha.hour:02d}:{fecha.minute:02d}',
        'Recibo':    num_recibo,
        'Mesa':      mesa,
        'Mozo':      mozo,
        'Subtotal':  var_subtotal.get(),
        'Impuestos': var_impuestos.get(),
        'Total':     var_total.get(),
    }])

    datos.df_historial = pd.concat([datos.df_historial, nueva_fila], ignore_index=True)
    datos.df_historial.to_csv(datos.HISTORIAL_CSV, index=False)

    # Si la pestaña historial está abierta, refrescar la tabla
    if tabla_historial is not None:
        tabla_historial.insert("", "end", values=(
            nueva_fila.iloc[0]['Fecha'],
            nueva_fila.iloc[0]['Hora'],
            nueva_fila.iloc[0]['Recibo'],
            nueva_fila.iloc[0]['Mesa'],
            nueva_fila.iloc[0]['Mozo'],
            nueva_fila.iloc[0]['Subtotal'],
            nueva_fila.iloc[0]['Impuestos'],
            nueva_fila.iloc[0]['Total'],
        ))


def generar_recibo(texto_recibo, texto_comida, texto_bebidas, texto_postres,
                   variables_comida, variables_bebidas, variables_postres,
                   var_costo_comida, var_costo_bebidas, var_costo_postres,
                   var_subtotal, var_impuestos, var_total,
                   tabla_historial=None):
    """
    Genera el texto del recibo en el área de texto de la derecha.
    Primero calcula el total automáticamente (por si el usuario no lo hizo).
    Si hay algún error en las cantidades, cancela y muestra el error.
    Solo muestra los ítems con cantidad mayor a 0.
    """
    # Calcular primero. Si hay error, calcular_total muestra el mensaje y devuelve False.
    ok = calcular_total(texto_comida, texto_bebidas, texto_postres,
                        variables_comida, variables_bebidas, variables_postres,
                        var_costo_comida, var_costo_bebidas, var_costo_postres,
                        var_subtotal, var_impuestos, var_total)
    if not ok:
        return

    # Pedir mesa y mozo antes de generar
    mesa, mozo = _seleccionar_mesa()
    if mesa is None:
        return

    texto_recibo.delete(1.0, END)

    num_recibo  = f'N# - {random.randint(1000, 9999)}'
    fecha       = datetime.now()
    fecha_recibo = f'{fecha.day}/{fecha.month}/{fecha.year} - {fecha.hour}:{fecha.minute}'

    texto_recibo.insert(END, f'Datos:\t{num_recibo}\t\t{fecha_recibo}\n ')
    texto_recibo.insert(END, f'Mesa:\t{mesa}\t\tMozo: {mozo}\n ')
    texto_recibo.insert(END, '*' * 52 + '\n')
    texto_recibo.insert(END, 'Items\t\tCant.\tCosto Items\n')
    texto_recibo.insert(END, '-' * 54 + '\n')

    for x, comida in enumerate(texto_comida):
        if comida.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="comida"]["nombre"].iloc[x]}\t\t{comida.get()}\t'
                                     f'$ {int(comida.get()) * datos.df_menu[datos.df_menu["categoria"]=="comida"]["precio"].iloc[x]}\n')

    for x, bebida in enumerate(texto_bebidas):
        if bebida.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="bebida"]["nombre"].iloc[x]}\t\t{bebida.get()}\t'
                                     f'$ {int(bebida.get()) * datos.df_menu[datos.df_menu["categoria"]=="bebida"]["precio"].iloc[x]}\n')

    for x, postre in enumerate(texto_postres):
        if postre.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="postre"]["nombre"].iloc[x]}\t\t{postre.get()}\t'
                                     f'$ {int(postre.get()) * datos.df_menu[datos.df_menu["categoria"]=="postre"]["precio"].iloc[x]}\n')

    texto_recibo.insert(END, '-' * 54 + '\n')
    texto_recibo.insert(END, f'Costo de la Comida:\t\t\t{var_costo_comida.get()}\n')
    texto_recibo.insert(END, f'Costo de la Bebida:\t\t\t{var_costo_bebidas.get()}\n')
    texto_recibo.insert(END, f'Costo del Postre:\t\t\t{var_costo_postres.get()}\n')
    texto_recibo.insert(END, '-' * 54 + '\n')
    texto_recibo.insert(END, f'Sub-total:\t\t\t{var_subtotal.get()}\n ')
    texto_recibo.insert(END, f'Impuestos:\t\t\t{var_impuestos.get()}\n ')
    texto_recibo.insert(END, f'Total:\t\t\t{var_total.get()}\n ')
    texto_recibo.insert(END, '*' * 47 + '\n')
    texto_recibo.insert(END, 'Lo esperamos pronto')

    # Guardar en historial automáticamente
    _guardar_en_historial(num_recibo, fecha, mesa, mozo,
                          var_subtotal, var_impuestos, var_total,
                          tabla_historial)


def guardar_recibo(texto_recibo):
    """Abre un cuadro de diálogo para guardar el recibo como .txt"""
    info_recibo = texto_recibo.get(1.0, END)
    archivo = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if archivo:  # el usuario puede cancelar el diálogo
        archivo.write(info_recibo)
        archivo.close()
        messagebox.showinfo('Información', 'Su recibo ha sido guardado')


def resetear_pedido(texto_recibo,
                    texto_comida, texto_bebidas, texto_postres,
                    cuadros_comida, cuadros_bebidas, cuadros_postres,
                    variables_comida, variables_bebidas, variables_postres,
                    var_costo_comida, var_costo_bebidas, var_costo_postres,
                    var_subtotal, var_impuestos, var_total):
    """Limpia todo el pedido: desmarca checkboxes, pone cantidades en 0 y borra el recibo."""
    from tkinter import DISABLED

    texto_recibo.delete(1.0, END)

    for texto in texto_comida:
        texto.set('0')
    for texto in texto_bebidas:
        texto.set('0')
    for texto in texto_postres:
        texto.set('0')

    for cuadro in cuadros_comida + cuadros_bebidas + cuadros_postres:
        cuadro.config(state=DISABLED)

    for variable in variables_comida + variables_bebidas + variables_postres:
        variable.set(0)

    var_costo_comida.set('')
    var_costo_bebidas.set('')
    var_costo_postres.set('')
    var_subtotal.set('')
    var_impuestos.set('')
    var_total.set('')


# ============================================================
# --- MOZOS (Tab Mozos) ---
# ============================================================

def agregar_mozo(entry_mozo, tabla_mozos):
    """Lee el nombre del Entry y agrega un nuevo mozo a la lista."""
    global contador_id_mozo  # no está en datos porque se modifica acá
    nombre = entry_mozo.get().strip()
    if nombre:
        datos.mozos.append((datos.contador_id_mozo, nombre))
        datos.contador_id_mozo += 1
        actualizar_lista_mozos(tabla_mozos)
        guardar_mozos()
        entry_mozo.delete(0, END)


def eliminar_mozo(tabla_mozos):
    """Elimina el mozo seleccionado en la tabla."""
    selected = tabla_mozos.selection()
    if selected:
        mozo_id = int(tabla_mozos.item(selected, "values")[0])
        datos.mozos = [m for m in datos.mozos if m[0] != mozo_id]
        actualizar_lista_mozos(tabla_mozos)
        guardar_mozos()


def actualizar_lista_mozos(tabla_mozos):
    """Recarga la tabla de mozos con los datos actuales."""
    for item in tabla_mozos.get_children():
        tabla_mozos.delete(item)

    # Contar cuántas mesas tiene asignadas cada mozo
    mesas_por_mozo = {}
    for _, row in datos.df_mesas.iterrows():
        if row["Mozo"] != "-":
            mesas_por_mozo.setdefault(row["Mozo"], []).append(str(row["Mesa"]))

    for m in datos.mozos:
        mesas_asignadas = mesas_por_mozo.get(m[1], [])
        mesas_str = ", ".join(mesas_asignadas) if mesas_asignadas else "-"
        estado    = "Ocupado" if mesas_asignadas else "Libre"
        tabla_mozos.insert("", "end", values=(m[0], m[1], mesas_str, estado))


def editar_mozo(tabla_mozos):
    """Permite editar el ID y nombre del mozo seleccionado."""
    from tkinter import Toplevel, Label, Entry, Button, StringVar, IntVar
    selected = tabla_mozos.selection()
    if not selected:
        messagebox.showwarning("Atención", "Seleccioná un mozo para editar.")
        return

    valores      = tabla_mozos.item(selected, "values")
    mozo_id_viejo = int(valores[0])
    nombre_viejo  = valores[1]

    ventana = Toplevel()
    ventana.title("Editar Mozo")
    ventana.geometry("300x200")
    ventana.grab_set()
    ventana.config(bg='#1a1a2e')

    Label(ventana, text="Nuevo ID:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(15, 2))
    entry_id = Entry(ventana, font=("Arial", 12), width=10, bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_id.insert(0, str(mozo_id_viejo))
    entry_id.pack()

    Label(ventana, text="Nombre:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(10, 2))
    entry_nombre = Entry(ventana, font=("Arial", 12), width=20, bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_nombre.insert(0, nombre_viejo)
    entry_nombre.pack()

    def confirmar():
        nuevo_id_str = entry_id.get().strip()
        nuevo_nombre = entry_nombre.get().strip()

        if not nuevo_nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        try:
            nuevo_id = int(nuevo_id_str)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        # Verificar que el ID nuevo no esté en uso por otro mozo
        ids_existentes = [m[0] for m in datos.mozos if m[0] != mozo_id_viejo]
        if nuevo_id in ids_existentes:
            messagebox.showerror("Error", f"El ID {nuevo_id} ya está en uso por otro mozo.")
            return

        # Actualizar en la lista
        datos.mozos = [
            (nuevo_id, nuevo_nombre) if m[0] == mozo_id_viejo else m
            for m in datos.mozos
        ]
        # Actualizar contador si el nuevo ID es mayor al actual
        if nuevo_id >= datos.contador_id_mozo:
            datos.contador_id_mozo = nuevo_id + 1

        actualizar_lista_mozos(tabla_mozos)
        guardar_mozos()
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    Button(ventana, text="Confirmar", bg="#2ecc71", fg="#0a3d1f", command=confirmar).pack(side="left", padx=25, pady=15)
    Button(ventana, text="Cancelar",  bg="#e94560", fg="#e0e0e0",     command=cancelar).pack(side="right", padx=25, pady=15)

    ventana.wait_window()


def guardar_mozos():
    """Guarda la lista actual de mozos en mozos.csv"""
    import pandas as pd
    df = pd.DataFrame(datos.mozos, columns=['ID', 'Nombre'])
    df.to_csv(datos.MOZOS_CSV, index=False)


# ============================================================
# --- MESAS (Tab Mesas) ---
# ============================================================

def ocupar_mesa_desde_restaurante(callback_actualizar):
    """
    Igual que ocupar_mesa pero sin necesitar el widget tabla_mesas.
    Actualiza datos.df_mesas directamente y llama al callback
    para refrescar el combo de mesas en Restaurante.
    """
    from tkinter import Toplevel, Label, Button, StringVar

    if not datos.mozos:
        messagebox.showwarning("Atención", "Debe registrar mozos antes de abrir mesas.")
        return

    # Solo mesas libres
    mesas_libres = datos.df_mesas[datos.df_mesas["Estado"] == "Libre"]
    if mesas_libres.empty:
        messagebox.showwarning("Atención", "No hay mesas libres disponibles.")
        return

    # Armar opciones de mesas
    opciones_mesas = [f"Mesa {row['Mesa']}" for _, row in mesas_libres.iterrows()]

    # Armar opciones de mozos con estado
    mesas_por_mozo = {}
    for _, row in datos.df_mesas.iterrows():
        if row["Mozo"] != "-":
            mesas_por_mozo[row["Mozo"]] = mesas_por_mozo.get(row["Mozo"], 0) + 1

    opciones_mozos = []
    for m in datos.mozos:
        cantidad = mesas_por_mozo.get(m[1], 0)
        estado   = f"({cantidad} mesas)" if cantidad > 0 else "(libre)"
        opciones_mozos.append(f"{m[0]} - {m[1]} {estado}")

    resultado = {"mesa": None, "mozo": None}

    ventana = Toplevel()
    ventana.title("Abrir Mesa")
    ventana.geometry("320x220")
    ventana.grab_set()
    ventana.config(bg='#1a1a2e')

    Label(ventana, text="Seleccioná la mesa:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(15, 2))
    var_mesa = StringVar()
    combo_mesa = ttk.Combobox(ventana, textvariable=var_mesa,
                               values=opciones_mesas, state="readonly", width=30)
    combo_mesa.current(0)
    combo_mesa.pack(pady=4)

    Label(ventana, text="Seleccioná el mozo:", font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(8, 2))
    var_mozo = StringVar()
    combo_mozo = ttk.Combobox(ventana, textvariable=var_mozo,
                               values=opciones_mozos, state="readonly", width=30)
    combo_mozo.current(0)
    combo_mozo.pack(pady=4)

    def confirmar():
        mesa_str  = var_mesa.get().replace("Mesa ", "")
        mozo_str  = var_mozo.get().split(" - ")[1].split(" (")[0]
        resultado["mesa"] = int(mesa_str)
        resultado["mozo"] = mozo_str
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    Button(ventana, text="Abrir", bg="#2ecc71", fg="#0a3d1f", command=confirmar).pack(side="left", padx=30, pady=12)
    Button(ventana, text="Cancelar", bg="#e94560", fg="#e0e0e0",  command=cancelar).pack(side="right", padx=30, pady=12)

    ventana.wait_window()

    if resultado["mesa"] is None:
        return

    # Actualizar df_mesas
    datos.df_mesas.loc[
        datos.df_mesas["Mesa"] == resultado["mesa"],
        ["Estado", "Mozo"]
    ] = ["Ocupada", resultado["mozo"]]

    # Refrescar el combo en Restaurante
    callback_actualizar()
    messagebox.showinfo("Mesa abierta",
                        f"Mesa {resultado['mesa']} abierta para {resultado['mozo']}.")


def cerrar_mesa_y_recibo(num_mesa, mozo,
                          texto_recibo,
                          texto_comida, texto_bebidas, texto_postres,
                          variables_comida, variables_bebidas, variables_postres,
                          var_costo_comida, var_costo_bebidas, var_costo_postres,
                          var_subtotal, var_impuestos, var_total,
                          tabla_historial, callback_actualizar):
    """
    Genera el recibo para la mesa seleccionada y la libera automáticamente.
    Reemplaza el flujo manual de Recibo + Liberar Mesa.
    """
    from tkinter import messagebox

    # Calcular total primero
    ok = calcular_total(texto_comida, texto_bebidas, texto_postres,
                        variables_comida, variables_bebidas, variables_postres,
                        var_costo_comida, var_costo_bebidas, var_costo_postres,
                        var_subtotal, var_impuestos, var_total)
    if not ok:
        return

    # Confirmar cierre
    if not messagebox.askyesno("Cerrar Mesa",
                                f"¿Cerrás la Mesa {num_mesa} atendida por {mozo}?\n"
                                f"Se generará el recibo y la mesa quedará libre."):
        return

    # Generar el recibo con mesa y mozo ya conocidos (sin ventana emergente)
    texto_recibo.delete(1.0, END)

    num_recibo   = f'N# - {random.randint(1000, 9999)}'
    fecha        = datetime.now()
    fecha_recibo = f'{fecha.day}/{fecha.month}/{fecha.year} - {fecha.hour}:{fecha.minute}'

    texto_recibo.insert(END, f'Datos:\t{num_recibo}\t\t{fecha_recibo}\n ')
    texto_recibo.insert(END, f'Mesa:\t{num_mesa}\t\tMozo: {mozo}\n ')
    texto_recibo.insert(END, '*' * 52 + '\n')
    texto_recibo.insert(END, 'Items\t\tCant.\tCosto Items\n')
    texto_recibo.insert(END, '-' * 54 + '\n')

    for x, comida in enumerate(texto_comida):
        if variables_comida[x].get() == 1 and comida.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="comida"]["nombre"].iloc[x]}\t\t{comida.get()}\t'
                                     f'$ {int(comida.get()) * datos.df_menu[datos.df_menu["categoria"]=="comida"]["precio"].iloc[x]}\n')

    for x, bebida in enumerate(texto_bebidas):
        if variables_bebidas[x].get() == 1 and bebida.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="bebida"]["nombre"].iloc[x]}\t\t{bebida.get()}\t'
                                     f'$ {int(bebida.get()) * datos.df_menu[datos.df_menu["categoria"]=="bebida"]["precio"].iloc[x]}\n')

    for x, postre in enumerate(texto_postres):
        if variables_postres[x].get() == 1 and postre.get() != '0':
            texto_recibo.insert(END, f'{datos.df_menu[datos.df_menu["categoria"]=="postre"]["nombre"].iloc[x]}\t\t{postre.get()}\t'
                                     f'$ {int(postre.get()) * datos.df_menu[datos.df_menu["categoria"]=="postre"]["precio"].iloc[x]}\n')

    texto_recibo.insert(END, '-' * 54 + '\n')
    texto_recibo.insert(END, f'Costo de la Comida:\t\t\t{var_costo_comida.get()}\n')
    texto_recibo.insert(END, f'Costo de la Bebida:\t\t\t{var_costo_bebidas.get()}\n')
    texto_recibo.insert(END, f'Costo del Postre:\t\t\t{var_costo_postres.get()}\n')
    texto_recibo.insert(END, '-' * 54 + '\n')
    texto_recibo.insert(END, f'Sub-total:\t\t\t{var_subtotal.get()}\n ')
    texto_recibo.insert(END, f'Impuestos:\t\t\t{var_impuestos.get()}\n ')
    texto_recibo.insert(END, f'Total:\t\t\t{var_total.get()}\n ')
    texto_recibo.insert(END, '*' * 47 + '\n')
    texto_recibo.insert(END, 'Lo esperamos pronto')

    # Guardar en historial
    _guardar_en_historial(num_recibo, fecha, str(num_mesa), mozo,
                          var_subtotal, var_impuestos, var_total,
                          tabla_historial)

    # Liberar la mesa
    datos.df_mesas.loc[
        datos.df_mesas["Mesa"] == num_mesa,
        ["Estado", "Mozo"]
    ] = ["Libre", "-"]

    # Refrescar el combo
    callback_actualizar()

    messagebox.showinfo("Mesa cerrada",
                        f"Mesa {num_mesa} cerrada correctamente.")


def ocupar_mesa(tabla_mesas):
    """Asigna un mozo a la mesa seleccionada usando un menú desplegable."""
    from tkinter import Toplevel, Label, Button, StringVar
    selected = tabla_mesas.selection()
    if not selected:
        return

    mesa = int(tabla_mesas.item(selected, "values")[0])

    if not datos.mozos:
        messagebox.showwarning("Atención", "Debe registrar mozos antes de ocupar mesas.")
        return

    # Armar opciones con estado de cada mozo
    mesas_por_mozo = {}
    for _, row in datos.df_mesas.iterrows():
        if row["Mozo"] != "-":
            mesas_por_mozo[row["Mozo"]] = mesas_por_mozo.get(row["Mozo"], 0) + 1

    opciones = []
    for m in datos.mozos:
        cantidad = mesas_por_mozo.get(m[1], 0)
        estado   = f"({cantidad} mesas)" if cantidad > 0 else "(libre)"
        opciones.append(f"{m[0]} - {m[1]} {estado}")

    resultado = {"mozo": None}

    ventana = Toplevel()
    ventana.title(f"Asignar mozo a Mesa {mesa}")
    ventana.geometry("320x160")
    ventana.grab_set()
    ventana.config(bg='#1a1a2e')

    Label(ventana, text=f"Seleccioná un mozo para la Mesa {mesa}:",
          font=("Arial", 11), bg='#1a1a2e', fg='#e0e0e0').pack(pady=12)

    var_sel = StringVar()
    combo = ttk.Combobox(ventana, textvariable=var_sel,
                         values=opciones, state="readonly", width=35)
    combo.current(0)
    combo.pack(pady=5)

    def confirmar():
        seleccion = var_sel.get()           # "1 - Juan (libre)"
        mozo_id   = int(seleccion.split(" - ")[0])
        mozo_nombre = seleccion.split(" - ")[1].split(" (")[0]
        resultado["mozo"] = (mozo_id, mozo_nombre)
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    Button(ventana, text="Confirmar", bg="#2ecc71", fg="#0a3d1f", command=confirmar).pack(side="left", padx=30, pady=10)
    Button(ventana, text="Cancelar",  bg="#e94560", fg="#e0e0e0",     command=cancelar).pack(side="right", padx=30, pady=10)

    ventana.wait_window()

    if resultado["mozo"] is None:
        return

    mozo_id, mozo_nombre = resultado["mozo"]
    tabla_mesas.item(selected, values=(mesa, "Ocupada", f"{mozo_nombre} (ID:{mozo_id})"))
    datos.df_mesas.loc[datos.df_mesas["Mesa"] == mesa, ["Estado", "Mozo"]] = ["Ocupada", mozo_nombre]


def liberar_mesa(tabla_mesas):
    """Libera la mesa seleccionada."""
    selected = tabla_mesas.selection()
    if selected:
        mesa = int(tabla_mesas.item(selected, "values")[0])
        tabla_mesas.item(selected, values=(mesa, "Libre", "-"))
        datos.df_mesas.loc[datos.df_mesas["Mesa"] == mesa, ["Estado", "Mozo"]] = ["Libre", "-"]


def liberar_todas(tabla_mesas):
    """Libera todas las mesas de una vez."""
    for item in tabla_mesas.get_children():
        mesa = int(tabla_mesas.item(item, "values")[0])
        tabla_mesas.item(item, values=(mesa, "Libre", "-"))
    datos.df_mesas["Estado"] = "Libre"
    datos.df_mesas["Mozo"]   = "-"


def agregar_mesa(tabla_mesas):
    """Agrega una nueva mesa ingresando su número."""
    nueva_mesa = simpledialog.askinteger("Agregar Mesa", "Número de mesa:")
    if nueva_mesa and nueva_mesa not in datos.df_mesas["Mesa"].values:
        import pandas as pd
        datos.df_mesas = pd.concat(
            [datos.df_mesas, pd.DataFrame({"Mesa": [nueva_mesa], "Estado": ["Libre"], "Mozo": ["-"]})],
            ignore_index=True
        )
        tabla_mesas.insert("", "end", values=(nueva_mesa, "Libre", "-"))
    else:
        messagebox.showwarning("Atención", "Número inválido o ya existente.")


def eliminar_mesa(tabla_mesas):
    """Elimina la mesa seleccionada."""
    selected = tabla_mesas.selection()
    if selected:
        mesa = int(tabla_mesas.item(selected, "values")[0])
        datos.df_mesas = datos.df_mesas[datos.df_mesas["Mesa"] != mesa]
        tabla_mesas.delete(selected)


def guardar_mesas():
    """Guarda el estado actual de las mesas en mesas.csv"""
    datos.df_mesas.to_csv("mesas.csv", index=False)
    messagebox.showinfo("Mesas", "Estado de las mesas guardado en mesas.csv")


def cargar_mesas(tabla_mesas):
    """Carga el estado de las mesas desde mesas.csv"""
    import pandas as pd
    datos.df_mesas = pd.read_csv("mesas.csv")
    for item in tabla_mesas.get_children():
        tabla_mesas.delete(item)
    for _, row in datos.df_mesas.iterrows():
        tabla_mesas.insert("", "end", values=(row["Mesa"], row["Estado"], row["Mozo"]))
