# ============================================================
# logica.py
# Contiene todas las funciones que hacen cálculos o modifican
# datos: calculadora, pedidos, recibo, mozos y mesas.
# La interfaz llama a estas funciones cuando el usuario
# hace clic en un botón.
# ============================================================

import random
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog, END

import datos


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


def calcular_total(texto_comida, texto_bebidas, texto_postres,
                   var_costo_comida, var_costo_bebidas, var_costo_postres,
                   var_subtotal, var_impuestos, var_total):
    """
    Recorre todas las cantidades ingresadas, multiplica por los precios
    y calcula: subtotal, impuestos (21%) y total.
    Actualiza las variables de la interfaz con los resultados.
    """
    sub_total_comida = sum(
        float(cantidad.get()) * datos.precios_comida[p]
        for p, cantidad in enumerate(texto_comida)
    )
    print(sub_total_comida)  # debug - eliminar cuando todo esté OK

    sub_total_bebidas = sum(
        float(cantidad.get()) * datos.precios_bebidas[p]
        for p, cantidad in enumerate(texto_bebidas)
    )
    print(sub_total_bebidas)  # debug

    sub_total_postre = sum(
        float(cantidad.get()) * datos.precios_postres[p]
        for p, cantidad in enumerate(texto_postres)
    )
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


def generar_recibo(texto_recibo, texto_comida, texto_bebidas, texto_postres,
                   var_costo_comida, var_costo_bebidas, var_costo_postres,
                   var_subtotal, var_impuestos, var_total):
    """
    Genera el texto del recibo en el área de texto de la derecha.
    Solo muestra los ítems con cantidad mayor a 0.
    """
    texto_recibo.delete(1.0, END)

    num_recibo  = f'N# - {random.randint(1000, 9999)}'
    fecha       = datetime.now()
    fecha_recibo = f'{fecha.day}/{fecha.month}/{fecha.year} - {fecha.hour}:{fecha.minute}'

    texto_recibo.insert(END, f'Datos:\t{num_recibo}\t\t{fecha_recibo}\n ')
    texto_recibo.insert(END, '*' * 52 + '\n')
    texto_recibo.insert(END, 'Items\t\tCant.\tCosto Items\n')
    texto_recibo.insert(END, '-' * 54 + '\n')

    for x, comida in enumerate(texto_comida):
        if comida.get() != '0':
            texto_recibo.insert(END, f'{datos.lista_comida[x]}\t\t{comida.get()}\t'
                                     f'$ {int(comida.get()) * datos.precios_comida[x]}\n')

    for x, bebida in enumerate(texto_bebidas):
        if bebida.get() != '0':
            texto_recibo.insert(END, f'{datos.lista_bebidas[x]}\t\t{bebida.get()}\t'
                                     f'$ {int(bebida.get()) * datos.precios_bebidas[x]}\n')

    for x, postre in enumerate(texto_postres):
        if postre.get() != '0':
            texto_recibo.insert(END, f'{datos.lista_postre[x]}\t\t{postre.get()}\t'
                                     f'$ {int(postre.get()) * datos.precios_postres[x]}\n')

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
        entry_mozo.delete(0, END)


def eliminar_mozo(tabla_mozos):
    """Elimina el mozo seleccionado en la tabla."""
    selected = tabla_mozos.selection()
    if selected:
        mozo_id = int(tabla_mozos.item(selected, "values")[0])
        datos.mozos = [m for m in datos.mozos if m[0] != mozo_id]
        actualizar_lista_mozos(tabla_mozos)


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


# ============================================================
# --- MESAS (Tab Mesas) ---
# ============================================================

def ocupar_mesa(tabla_mesas):
    """Asigna un mozo a la mesa seleccionada."""
    selected = tabla_mesas.selection()
    if not selected:
        return

    mesa = int(tabla_mesas.item(selected, "values")[0])

    if not datos.mozos:
        messagebox.showwarning("Atención", "Debe registrar mozos antes de ocupar mesas.")
        return

    # Armar la lista de mozos con su estado actual
    mesas_por_mozo = {}
    for _, row in datos.df_mesas.iterrows():
        if row["Mozo"] != "-":
            mesas_por_mozo[row["Mozo"]] = mesas_por_mozo.get(row["Mozo"], 0) + 1

    info_mozos = []
    for m in datos.mozos:
        cantidad = mesas_por_mozo.get(m[1], 0)
        estado   = f"({cantidad} mesas)" if cantidad > 0 else "(libre)"
        info_mozos.append(f"{m[0]} - {m[1]} {estado}")

    mozo_input = simpledialog.askstring(
        "Asignar Mozo",
        "Ingrese ID o nombre del mozo:\n\n" + "\n".join(info_mozos)
    )

    if not mozo_input:
        return

    # Buscar el mozo por ID o nombre
    mozo_input    = mozo_input.strip().lower()
    mozo_encontrado = None

    for m in datos.mozos:
        if (str(m[0]) == mozo_input or
                m[1].lower() == mozo_input or
                f"{m[0]} - {m[1]}".lower() == mozo_input):
            mozo_encontrado = m
            break

    if not mozo_encontrado:
        messagebox.showerror("Error", "Mozo no encontrado. Intente con ID o nombre exacto.")
        return

    tabla_mesas.item(selected, values=(mesa, "Ocupada", f"{mozo_encontrado[1]} (ID:{mozo_encontrado[0]})"))
    datos.df_mesas.loc[datos.df_mesas["Mesa"] == mesa, ["Estado", "Mozo"]] = ["Ocupada", mozo_encontrado[1]]


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
