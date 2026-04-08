# ============================================================
# interfaz.py
# Construye toda la interfaz gráfica: ventana, pestañas,
# paneles, botones, tablas y checkboxes.
# Cada sección está claramente separada por comentarios.
# ============================================================

import sys
from tkinter import *
from tkinter import ttk
try:
    from tkcalendar import DateEntry
    TKCALENDAR_OK = True
except ImportError:
    TKCALENDAR_OK = False

import datos
import logica


def _aplicar_estilo_ttk():
    estilo = ttk.Style()
    estilo.theme_use('clam')
    for nombre in ('TNotebook', 'Dark.TNotebook'):
        estilo.configure(nombre, background='#1a1a2e', borderwidth=0, tabmargins=[0,0,0,0])
        estilo.configure(f'{nombre}.Tab', background='#0f3460', foreground='#e0e0e0',
                         padding=[14, 7], font=('Arial', 10, 'bold'), borderwidth=0)
        estilo.map(f'{nombre}.Tab',
                   background=[('selected', '#2ecc71'), ('active', '#16213e')],
                   foreground=[('selected', '#0a3d1f'), ('active', '#e0e0e0')])
    estilo.configure('TFrame', background='#1a1a2e')
    estilo.configure('Treeview', background='#16213e', foreground='#e0e0e0',
                     fieldbackground='#16213e', rowheight=28, font=('Arial', 10), borderwidth=0)
    estilo.configure('Treeview.Heading', background='#0f3460', foreground='#e0e0e0',
                     font=('Arial', 10, 'bold'), relief='flat')
    estilo.map('Treeview',
               background=[('selected', '#0f3460')],
               foreground=[('selected', '#2ecc71')])
    estilo.configure('TScrollbar', background='#0f3460', troughcolor='#16213e',
                     arrowcolor='#e0e0e0', borderwidth=0)
    estilo.configure('TCombobox', fieldbackground='#16213e', background='#0f3460',
                     foreground='#e0e0e0', selectbackground='#0f3460',
                     selectforeground='#e0e0e0', arrowcolor='#e0e0e0')
    estilo.map('TCombobox',
               fieldbackground=[('readonly', '#16213e')],
               foreground=[('readonly', '#e0e0e0')],
               background=[('readonly', '#0f3460')])


def construir_interfaz(aplicacion):
    """
    Función principal. Recibe la ventana (Tk) ya creada en main.py
    y construye todo lo que hay dentro de ella.
    """
    _aplicar_estilo_ttk()
    aplicacion.config(bg='#1a1a2e')

    # --------------------------------------------------------
    # NOTEBOOK: las 3 pestañas
    # --------------------------------------------------------
    ventana = ttk.Notebook(aplicacion)
    ventana.config(style='Dark.TNotebook')
    ventana.pack(fill="both", expand=True)

    tab1 = Frame(ventana, bg='#1a1a2e')   # Restaurante
    tab2 = Frame(ventana, bg='#1a1a2e')   # Mozos
    tab3 = Frame(ventana, bg='#1a1a2e')   # Mesas
    tab4 = Frame(ventana, bg='#1a1a2e')   # Historial
    tab5 = Frame(ventana, bg='#1a1a2e')   # Menú

    ventana.add(tab1, text="Restaurante")
    ventana.add(tab2, text="Mozo")
    ventana.add(tab3, text="Mesas")
    ventana.add(tab4, text="Historial")
    ventana.add(tab5, text="Menú")

    # --------------------------------------------------------
    # TAB 4 — HISTORIAL (se construye primero para poder pasarlo a tab1)
    # --------------------------------------------------------
    tabla_historial = _construir_tab_historial(tab4)

    # --------------------------------------------------------
    # TAB 3 — MESAS (se construye antes que tab1 para pasar la tabla)
    # --------------------------------------------------------
    tabla_mesas = _construir_tab_mesas(tab3)

    # --------------------------------------------------------
    # TAB 1 — RESTAURANTE
    # --------------------------------------------------------
    tab1._recargar_menu_ref = [None]  # referencia al recargador del combo
    _construir_tab_restaurante(tab1, lambda: tabla_historial, lambda: tabla_mesas)

    # --------------------------------------------------------
    # TAB 2 — MOZOS
    # --------------------------------------------------------
    _construir_tab_mozos(tab2)

    # --------------------------------------------------------
    # TAB 5 — MENÚ
    # --------------------------------------------------------
    _construir_tab_menu(tab5, recargar_menu_ref=tab1._recargar_menu_ref)


# ============================================================
# TAB 1 — RESTAURANTE (función interna)
# ============================================================

def _construir_tab_restaurante(tab1, get_tabla_historial=None, get_tabla_mesas=None):
    """Pestaña restaurante con menú desplegable, pedido por mesa y panel izquierda/derecha."""

    # Panel superior
    panel_superior = Frame(tab1, bg='#0f3460')
    panel_superior.pack(side=TOP, fill='x')

    Label(panel_superior, text='Sistema Gastronómico',
          fg='#e0e0e0', font=('Dosis', 48), bg='#0f3460'
          ).grid(row=0, column=0, columnspan=5, pady=(8, 4))

    Label(panel_superior, text='Mesa activa:',
          font=('Dosis', 13, 'bold'), bg='#0f3460', fg='#e0e0e0'
          ).grid(row=1, column=0, padx=10, pady=6)

    var_mesa_activa = StringVar()
    combo_mesas = ttk.Combobox(panel_superior, textvariable=var_mesa_activa,
                                state='readonly', width=22, font=('Dosis', 12))
    combo_mesas.grid(row=1, column=1, padx=10, pady=6)

    def actualizar_combo_mesas():
        mesas_ocupadas = datos.df_mesas[datos.df_mesas["Estado"] == "Ocupada"]
        opciones = [f"Mesa {row['Mesa']} - {row['Mozo']}"
                    for _, row in mesas_ocupadas.iterrows()]
        combo_mesas["values"] = opciones
        if opciones and var_mesa_activa.get() not in opciones:
            combo_mesas.current(0)
        elif not opciones:
            var_mesa_activa.set("")
        if get_tabla_mesas:
            tabla = get_tabla_mesas()
            for item in tabla.get_children():
                tabla.delete(item)
            for _, row in datos.df_mesas.iterrows():
                tabla.insert("", "end", values=(row["Mesa"], row["Estado"], row["Mozo"]))

    Button(panel_superior, text="Abrir Mesa", bg="#2ecc71", fg="#0a3d1f",
           font=('Dosis', 11, 'bold'), width=12,
           command=lambda: logica.ocupar_mesa_desde_restaurante(actualizar_combo_mesas)
           ).grid(row=1, column=2, padx=10, pady=6)

    Button(panel_superior, text="Cerrar Mesa", bg="#e94560", fg="#e0e0e0",
           font=('Dosis', 11, 'bold'), width=12,
           command=lambda: _cerrar_mesa_actual()
           ).grid(row=1, column=3, padx=10, pady=6)

    Button(panel_superior, text="Contraseña", bg="#0f3460", fg="#e0e0e0",
           font=('Dosis', 10, 'bold'), width=10,
           command=lambda: __import__('login').ventana_cambiar_password()
           ).grid(row=1, column=4, padx=5, pady=6)

    Button(panel_superior, text="Exit", bg="#333333", fg="#e0e0e0",
           font=('Dosis', 11, 'bold'), width=6,
           command=sys.exit
           ).grid(row=1, column=5, padx=10, pady=6)

    actualizar_combo_mesas()

    # Cuerpo dividido en dos columnas
    frame_cuerpo = Frame(tab1, bg='#1a1a2e')
    frame_cuerpo.pack(fill="both", expand=True, padx=10, pady=10)

    # IZQUIERDA: selección de producto
    frame_izq = Frame(frame_cuerpo, bg='#16213e', bd=1, relief=RIDGE, padx=15, pady=15)
    frame_izq.pack(side=LEFT, fill="both", expand=True, padx=(0, 8))

    Label(frame_izq, text="Agregar al pedido",
          font=("Arial", 13, "bold"), bg='#16213e', fg='#e0e0e0').pack(pady=(0, 12))

    Label(frame_izq, text="Producto:", font=("Arial", 11),
          bg='#16213e', fg='#aaaaaa').pack(anchor="w")

    var_producto = StringVar()
    combo_producto = ttk.Combobox(frame_izq, textvariable=var_producto,
                                   state="readonly", font=("Arial", 11), width=35)
    combo_producto.pack(pady=(2, 12), fill="x")

    def recargar_combo_productos():
        orden_cat = {'comida': 0, 'bebida': 1, 'postre': 2}
        menu_ord = datos.df_menu.copy()
        menu_ord['orden'] = menu_ord['categoria'].map(orden_cat).fillna(3)
        menu_ord = menu_ord.sort_values(['orden', 'nombre']).reset_index(drop=True)
        vals = [f"{r['nombre'].title()} (${r['precio']}) - {r['categoria']}"
                for _, r in menu_ord.iterrows()]
        combo_producto['values'] = vals
        if vals:
            combo_producto.current(0)

    recargar_combo_productos()
    # Exponer para que la pestaña Menú pueda llamarla
    if hasattr(tab1, '_recargar_menu_ref'):
        tab1._recargar_menu_ref[0] = recargar_combo_productos

    Label(frame_izq, text="Cantidad:", font=("Arial", 11),
          bg='#16213e', fg='#aaaaaa').pack(anchor="w")

    frame_cant = Frame(frame_izq, bg='#16213e')
    frame_cant.pack(fill="x", pady=(2, 16))

    var_cantidad = StringVar(value="1")
    Entry(frame_cant, textvariable=var_cantidad,
          font=("Arial", 14), width=6, justify="center",
          bg='#1a1a2e', fg='#e0e0e0', insertbackground='#e0e0e0'
          ).pack(side=LEFT, padx=(0, 8))

    Button(frame_cant, text="-", bg='#0f3460', fg='#e0e0e0',
           font=("Arial", 12, "bold"), width=3,
           command=lambda: var_cantidad.set(str(max(1, int(var_cantidad.get() or 1) - 1)))
           ).pack(side=LEFT, padx=2)
    Button(frame_cant, text="+", bg='#0f3460', fg='#e0e0e0',
           font=("Arial", 12, "bold"), width=3,
           command=lambda: var_cantidad.set(str(int(var_cantidad.get() or 1) + 1))
           ).pack(side=LEFT, padx=2)

    Button(frame_izq, text="+ Agregar al pedido", bg='#2ecc71', fg='#0a3d1f',
           font=("Arial", 12, "bold"),
           command=lambda: _agregar_item()
           ).pack(fill="x", pady=(0, 8))

    Button(frame_izq, text="- Quitar seleccionado", bg='#e94560', fg='#e0e0e0',
           font=("Arial", 12, "bold"),
           command=lambda: _quitar_item()
           ).pack(fill="x")

    Label(frame_izq, text="Calculadora",
          font=("Arial", 11), bg='#16213e', fg='#aaaaaa').pack(anchor="w", pady=(20, 4))
    frame_calc = Frame(frame_izq, bg='#16213e')
    frame_calc.pack(fill="x")
    _construir_calculadora(frame_calc)

    # DERECHA: pedido actual
    frame_der = Frame(frame_cuerpo, bg='#16213e', bd=1, relief=RIDGE, padx=15, pady=15)
    frame_der.pack(side=RIGHT, fill="both", expand=True, padx=(8, 0))

    Label(frame_der, text="Pedido actual",
          font=("Arial", 13, "bold"), bg='#16213e', fg='#e0e0e0').pack(pady=(0, 10))

    frame_tabla = Frame(frame_der, bg='#16213e')
    frame_tabla.pack(fill="both", expand=True)

    cols = ("Producto", "Cant.", "Precio unit.", "Subtotal")
    tabla_pedido = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=12)
    for col in cols:
        tabla_pedido.heading(col, text=col)
    tabla_pedido.column("Producto",     width=150, anchor="w")
    tabla_pedido.column("Cant.",        width=50,  anchor="center")
    tabla_pedido.column("Precio unit.", width=90,  anchor="center")
    tabla_pedido.column("Subtotal",     width=80,  anchor="center")
    scroll_ped = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_pedido.yview)
    tabla_pedido.configure(yscrollcommand=scroll_ped.set)
    tabla_pedido.pack(side=LEFT, fill="both", expand=True)
    scroll_ped.pack(side=LEFT, fill="y")

    frame_totales = Frame(frame_der, bg='#0f3460', pady=10, padx=10)
    frame_totales.pack(fill="x", pady=(10, 8))

    var_subtotal  = StringVar(value="$0.00")
    var_impuestos = StringVar(value="$0.00")
    var_total_str = StringVar(value="$0.00")

    for lbl, var, color in [("Subtotal:", var_subtotal, "#e0e0e0"),
                              ("Impuestos:", var_impuestos, "#f39c12"),
                              ("Total:", var_total_str, "#2ecc71")]:
        fila = Frame(frame_totales, bg='#0f3460')
        fila.pack(fill="x")
        Label(fila, text=lbl, font=("Arial", 11), bg='#0f3460', fg='#aaaaaa',
              width=12, anchor="w").pack(side=LEFT)
        Label(fila, textvariable=var, font=("Arial", 12, "bold"),
              bg='#0f3460', fg=color).pack(side=RIGHT)

    frame_btns = Frame(frame_der, bg='#16213e')
    frame_btns.pack(fill="x", pady=(4, 0))

    Button(frame_btns, text="Guardar Recibo", bg='#0f3460', fg='#e0e0e0',
           font=("Arial", 10, "bold"),
           command=lambda: _guardar_recibo()
           ).pack(side=LEFT, padx=4, fill="x", expand=True)

    Button(frame_btns, text="Resetear", bg='#16213e', fg='#aaaaaa',
           font=("Arial", 10, "bold"), bd=1,
           command=lambda: _resetear()
           ).pack(side=LEFT, padx=4, fill="x", expand=True)

    # Pedidos por mesa: { "Mesa 1 - david": [items...] }
    pedidos_por_mesa = {}

    def _pedido_de_mesa():
        mesa = var_mesa_activa.get()
        if not mesa:
            return []
        if mesa not in pedidos_por_mesa:
            pedidos_por_mesa[mesa] = []
        return pedidos_por_mesa[mesa]

    def _recalcular():
        pedido = _pedido_de_mesa()
        sub = sum(i["cantidad"] * i["precio"] for i in pedido)
        imp = round(sub * 0.21, 2)
        tot = round(sub + imp, 2)
        var_subtotal.set(f"${round(sub,2)}")
        var_impuestos.set(f"${imp}")
        var_total_str.set(f"${tot}")

    def _refrescar_tabla():
        for item in tabla_pedido.get_children():
            tabla_pedido.delete(item)
        for item in _pedido_de_mesa():
            tabla_pedido.insert("", "end", values=(
                item["nombre"].title(), item["cantidad"],
                f"${item['precio']}",
                f"${round(item['cantidad']*item['precio'],2)}"
            ))
        _recalcular()

    combo_mesas.bind("<<ComboboxSelected>>", lambda e: _refrescar_tabla())

    def _agregar_item():
        from tkinter import messagebox
        if not var_mesa_activa.get():
            messagebox.showwarning("Sin mesa", "Abrí una mesa primero.")
            return
        seleccion = var_producto.get()
        if not seleccion:
            return
        try:
            cantidad = int(var_cantidad.get())
            if cantidad < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return
        nombre = seleccion.split(" ($")[0].lower()
        precio = float(seleccion.split("($")[1].split(")")[0])
        pedido = _pedido_de_mesa()
        for item in pedido:
            if item["nombre"] == nombre:
                item["cantidad"] += cantidad
                _refrescar_tabla()
                return
        pedido.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
        _refrescar_tabla()
        var_cantidad.set("1")

    def _quitar_item():
        selected = tabla_pedido.selection()
        if not selected:
            return
        idx = tabla_pedido.index(selected[0])
        pedido = _pedido_de_mesa()
        if 0 <= idx < len(pedido):
            pedido.pop(idx)
            _refrescar_tabla()

    def _guardar_recibo():
        from tkinter import filedialog, messagebox
        import random
        from datetime import datetime
        pedido = _pedido_de_mesa()
        if not pedido:
            messagebox.showwarning("Vacío", "No hay ítems en el pedido.")
            return
        archivo = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        if archivo:
            fecha = datetime.now()
            lineas = [
                f"N# - {random.randint(1000,9999)}  {fecha.day}/{fecha.month}/{fecha.year} {fecha.hour}:{fecha.minute:02d}",
                f"Mesa: {var_mesa_activa.get()}",
                "=" * 44,
            ]
            for item in pedido:
                sub = item["cantidad"] * item["precio"]
                lineas.append(f"{item['nombre'].title():<20} x{item['cantidad']}  ${item['precio']}  = ${round(sub,2)}")
            lineas += ["=" * 44,
                       f"Subtotal: {var_subtotal.get()}",
                       f"Impuestos: {var_impuestos.get()}",
                       f"TOTAL: {var_total_str.get()}",
                       "Lo esperamos pronto"]
            archivo.write("\n".join(lineas))
            archivo.close()
            messagebox.showinfo("Guardado", "Recibo guardado.")

    def _resetear():
        from tkinter import messagebox
        pedido = _pedido_de_mesa()
        if pedido and not messagebox.askyesno("Resetear", "¿Limpiar el pedido?"):
            return
        pedido.clear()
        _refrescar_tabla()

    def _cerrar_mesa_actual():
        from tkinter import messagebox
        import random, pandas as pd
        from datetime import datetime
        seleccion = var_mesa_activa.get()
        if not seleccion:
            messagebox.showwarning("Sin mesa", "Seleccioná una mesa.")
            return
        pedido = _pedido_de_mesa()
        if not pedido:
            messagebox.showwarning("Vacío", "No hay ítems en el pedido.")
            return
        num_mesa = int(seleccion.split(" - ")[0].replace("Mesa ", ""))
        mozo = seleccion.split(" - ")[1]
        if not messagebox.askyesno("Cerrar Mesa", f"Cerrar Mesa {num_mesa} con {mozo}?"):
            return
        fecha = datetime.now()
        sub = sum(i["cantidad"] * i["precio"] for i in pedido)
        imp = round(sub * 0.21, 2)
        tot = round(sub + imp, 2)
        nueva_fila = pd.DataFrame([{
            "Fecha": f"{fecha.day}/{fecha.month}/{fecha.year}",
            "Hora": f"{fecha.hour:02d}:{fecha.minute:02d}",
            "Recibo": f"N# - {random.randint(1000,9999)}",
            "Mesa": num_mesa, "Mozo": mozo,
            "Subtotal": round(sub,2), "Impuestos": imp, "Total": tot,
        }])
        datos.df_historial = pd.concat([datos.df_historial, nueva_fila], ignore_index=True)
        datos.df_historial.to_csv(datos.HISTORIAL_CSV, index=False)
        datos.df_mesas.loc[datos.df_mesas["Mesa"] == num_mesa, ["Estado","Mozo"]] = ["Libre","-"]
        if get_tabla_historial:
            th = get_tabla_historial()
            th.insert("", "end", values=(nueva_fila.iloc[0]["Fecha"], nueva_fila.iloc[0]["Hora"],
                                          nueva_fila.iloc[0]["Recibo"], num_mesa, mozo,
                                          round(sub,2), imp, tot))
        if seleccion in pedidos_por_mesa:
            del pedidos_por_mesa[seleccion]
        actualizar_combo_mesas()
        _refrescar_tabla()
        messagebox.showinfo("Cerrada", f"Mesa {num_mesa} cerrada. Total: ${tot}")



def _generar_items(panel, categoria):
    """
    Genera los checkboxes y entries leyendo productos dinámicamente desde datos.df_menu.
    Devuelve tres listas: variables (IntVar), cuadros (Entry) y textos (StringVar).
    """
    variables = []
    cuadros   = []
    textos    = []

    productos = datos.df_menu[datos.df_menu['categoria'] == categoria]['nombre'].tolist()

    for i, nombre in enumerate(productos):
        var = IntVar()
        variables.append(var)

        cb = Checkbutton(panel,
                         text=nombre.title(),
                         font=('Dosis', 14, 'bold'),
                         onvalue=1, offvalue=0,
                         variable=var,
                         bg='#16213e', fg='#e0e0e0',
                         selectcolor='#0f3460',
                         activebackground='#16213e', activeforeground='#e0e0e0')
        cb.grid(row=i, column=0, sticky=W)

        texto = StringVar()
        texto.set('0')
        textos.append(texto)

        entry = Entry(panel,
                      font=('Dosis', 14, 'bold'),
                      bd=1, width=6,
                      state=DISABLED,
                      textvariable=texto,
                      bg='#16213e', fg='#e0e0e0',
                      disabledbackground='#16213e',
                      disabledforeground='#aaaaaa',
                      insertbackground='#e0e0e0')
        entry.grid(row=i, column=1)
        cuadros.append(entry)

    return variables, cuadros, textos


def _construir_panel_costos(panel_costo,
                              var_costo_comida, var_costo_bebidas, var_costo_postres,
                              var_subtotal, var_impuestos, var_total):
    """Crea las etiquetas y fields de solo lectura para los totales."""

    items_izq = [
        ('Costo Comida',  var_costo_comida,  0),
        ('Costo Bebidas', var_costo_bebidas, 1),
        ('Costo Postres', var_costo_postres, 2),
    ]
    items_der = [
        ('Subtotal',   var_subtotal,  0),
        ('Impuestos',  var_impuestos, 1),
        ('Total',      var_total,     2),
    ]

    for texto, var, fila in items_izq:
        Label(panel_costo, text=texto, font=('Dosis', 12, 'bold'), bg='#0f3460', fg='#e0e0e0').grid(row=fila, column=0)
        Entry(panel_costo, font=('Dosis', 14, 'bold'), bd=1, width=10, state='readonly', textvariable=var, bg='#16213e', fg='#2ecc71', readonlybackground='#16213e').grid(row=fila, column=1, padx=41)

    for texto, var, fila in items_der:
        Label(panel_costo, text=texto, font=('Dosis', 12, 'bold'), bg='#0f3460', fg='#e0e0e0').grid(row=fila, column=2)
        Entry(panel_costo, font=('Dosis', 14, 'bold'), bd=1, width=10, state='readonly', textvariable=var, bg='#16213e', fg='#2ecc71', readonlybackground='#16213e').grid(row=fila, column=3, padx=41)


def _construir_botones_principales(panel_botones, texto_recibo,
                                    texto_comida, texto_bebidas, texto_postres,
                                    cuadros_comida, cuadros_bebidas, cuadros_postres,
                                    variables_comida, variables_bebidas, variables_postres,
                                    var_costo_comida, var_costo_bebidas, var_costo_postres,
                                    var_subtotal, var_impuestos, var_total,
                                    get_tabla_historial=None):
    """Crea los botones Total, Recibo, Guardar, Resetear y Exit."""

    comandos = [
        ('Total',    lambda: logica.calcular_total(
                        texto_comida, texto_bebidas, texto_postres,
                        variables_comida, variables_bebidas, variables_postres,
                        var_costo_comida, var_costo_bebidas, var_costo_postres,
                        var_subtotal, var_impuestos, var_total)),
        ('Recibo',   lambda: logica.generar_recibo(
                        texto_recibo,
                        texto_comida, texto_bebidas, texto_postres,
                        variables_comida, variables_bebidas, variables_postres,
                        var_costo_comida, var_costo_bebidas, var_costo_postres,
                        var_subtotal, var_impuestos, var_total,
                        get_tabla_historial() if get_tabla_historial else None)),
        ('Guardar',  lambda: logica.guardar_recibo(texto_recibo)),
        ('Resetear', lambda: logica.resetear_pedido(
                        texto_recibo,
                        texto_comida, texto_bebidas, texto_postres,
                        cuadros_comida, cuadros_bebidas, cuadros_postres,
                        variables_comida, variables_bebidas, variables_postres,
                        var_costo_comida, var_costo_bebidas, var_costo_postres,
                        var_subtotal, var_impuestos, var_total)),
        ('Exit',     sys.exit),
    ]

    for col, (nombre, comando) in enumerate(comandos):
        Button(panel_botones,
               text=nombre,
               font=('Dosis', 14, 'bold'),
               fg='#e0e0e0', bg='#0f3460',
               bd=1, width=8,
               command=comando
               ).grid(row=0, column=col)


def _construir_calculadora(panel_calculadora):
    """Crea el visor y los botones de la calculadora."""

    visor = Entry(panel_calculadora, font=('Dosis', 16, 'bold'), width=32, bd=1, bg='#16213e', fg='#e0e0e0', insertbackground='#e0e0e0')
    visor.grid(row=0, column=0, columnspan=4)

    # Cada botón lleva: (texto visible, valor que se envía a logica)
    botones = [
        ('7', '7'), ('8', '8'), ('9', '9'), ('+', '+'),
        ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
        ('1', '1'), ('2', '2'), ('3', '3'), ('x', '*'),
        ('=', '='), ('B', 'B'), ('0', '0'), ('/', '/'),
    ]

    fila, columna = 1, 0
    for texto, valor in botones:
        if valor == '=':
            cmd = lambda: logica.obtener_resultado(visor)
        elif valor == 'B':
            cmd = lambda: logica.borrar(visor)
        else:
            cmd = lambda v=valor: logica.click_boton(v, visor)

        Button(panel_calculadora,
               text=texto,
               font=('Dosis', 16, 'bold'),
               fg='#e0e0e0', bg='#0f3460',
               bd=1, width=9,
               command=cmd
               ).grid(row=fila, column=columna)

        columna += 1
        if columna == 4:
            columna = 0
            fila   += 1


# ============================================================
# TAB 2 — MOZOS (función interna)
# ============================================================

def _construir_tab_mozos(tab2):

    # Contenedor principal dividido en dos columnas
    frame_principal = Frame(tab2, bg='#1a1a2e')
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    # ---- COLUMNA IZQUIERDA: gestión ----
    frame_izq = Frame(frame_principal, bg='#1a1a2e')
    frame_izq.pack(side=LEFT, fill="both", expand=True, padx=(0, 10))

    Label(frame_izq, text="Gestión de Mozos",
          font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#e0e0e0").pack(pady=(0, 10))

    entry_mozo = Entry(frame_izq, font=("Arial", 12),
                       bg="#16213e", fg="#e0e0e0", insertbackground="#e0e0e0")
    entry_mozo.pack(pady=5, fill="x")

    # Tabla de mozos
    tabla_mozos = ttk.Treeview(frame_izq,
                                columns=("ID", "Nombre", "Mesas", "Estado"),
                                show="headings", height=8)
    tabla_mozos.heading("ID",     text="ID")
    tabla_mozos.heading("Nombre", text="Nombre")
    tabla_mozos.heading("Mesas",  text="Mesas Asignadas")
    tabla_mozos.heading("Estado", text="Estado")
    tabla_mozos.column("ID",     width=40,  anchor="center")
    tabla_mozos.column("Nombre", width=100, anchor="center")
    tabla_mozos.column("Mesas",  width=120, anchor="center")
    tabla_mozos.column("Estado", width=80,  anchor="center")
    tabla_mozos.pack(pady=10, fill="x")

    frame_botones = Frame(frame_izq, bg='#1a1a2e')
    frame_botones.pack(pady=5)

    Button(frame_botones, text="Agregar Mozo", bg="#2ecc71", fg="#0a3d1f",
           font=("Arial", 10, "bold"),
           command=lambda: [logica.agregar_mozo(entry_mozo, tabla_mozos),
                            actualizar_stats()]
           ).pack(side="left", padx=4)

    Button(frame_botones, text="Editar Mozo", bg="#f39c12", fg="#3d2000",
           font=("Arial", 10, "bold"),
           command=lambda: [logica.editar_mozo(tabla_mozos),
                            actualizar_stats()]
           ).pack(side="left", padx=4)

    Button(frame_botones, text="Eliminar Mozo", bg="#e94560", fg="#e0e0e0",
           font=("Arial", 10, "bold"),
           command=lambda: [logica.eliminar_mozo(tabla_mozos),
                            actualizar_stats()]
           ).pack(side="left", padx=4)

    Button(frame_botones, text="Guardar", bg="#0f3460", fg="#e0e0e0",
           font=("Arial", 10, "bold"),
           command=logica.guardar_mozos
           ).pack(side="left", padx=4)

    # ---- COLUMNA DERECHA: panel de estadísticas ----
    frame_der = Frame(frame_principal, bg='#1a1a2e', width=380)
    frame_der.pack(side=RIGHT, fill="both", padx=(10, 0))
    frame_der.pack_propagate(False)

    Label(frame_der, text="Resumen en tiempo real",
          font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#e0e0e0").pack(pady=(0, 12))

    # Tarjetas de métricas
    frame_cards = Frame(frame_der, bg='#1a1a2e')
    frame_cards.pack(fill="x", pady=(0, 14))

    var_total   = StringVar(value="0")
    var_ocup    = StringVar(value="0")
    var_libres  = StringVar(value="0")

    for col, (label, var, color) in enumerate([
        ("Total mozos",    var_total,  "#2ecc71"),
        ("Ocupados ahora", var_ocup,   "#f39c12"),
        ("Libres ahora",   var_libres, "#e0e0e0"),
    ]):
        card = Frame(frame_cards, bg='#16213e', bd=0)
        card.grid(row=0, column=col, padx=5, sticky="ew")
        frame_cards.columnconfigure(col, weight=1)
        # Borde de acento izquierdo simulado con un frame delgado
        Frame(card, bg=color, width=4).pack(side=LEFT, fill="y")
        inner = Frame(card, bg='#16213e', padx=10, pady=12)
        inner.pack(side=LEFT, fill="both", expand=True)
        Label(inner, text=label, font=("Arial", 10), bg='#16213e', fg='#aaaaaa').pack(anchor="w")
        Label(inner, textvariable=var, font=("Arial", 26, "bold"),
              bg='#16213e', fg=color).pack(anchor="w")

    # Lista de estado actual de cada mozo
    Label(frame_der, text="Estado actual",
          font=("Arial", 11), bg="#1a1a2e", fg="#aaaaaa").pack(anchor="w", pady=(0, 6))

    frame_lista = Frame(frame_der, bg='#16213e', bd=1, relief=RIDGE)
    frame_lista.pack(fill="both", expand=True)

    # Canvas + scrollbar para la lista de mozos
    canvas_mozos = Canvas(frame_lista, bg='#16213e', highlightthickness=0)
    scroll_lista = ttk.Scrollbar(frame_lista, orient="vertical",
                                  command=canvas_mozos.yview)
    canvas_mozos.configure(yscrollcommand=scroll_lista.set)
    canvas_mozos.pack(side=LEFT, fill="both", expand=True)
    scroll_lista.pack(side=RIGHT, fill="y")

    frame_scroll = Frame(canvas_mozos, bg='#16213e')
    canvas_mozos.create_window((0, 0), window=frame_scroll, anchor="nw")

    def actualizar_stats():
        """Recalcula y redibuja el panel de estadísticas."""
        # Limpiar lista
        for w in frame_scroll.winfo_children():
            w.destroy()

        mesas_por_mozo = {}
        for _, row in datos.df_mesas.iterrows():
            if row["Mozo"] != "-":
                mesas_por_mozo.setdefault(row["Mozo"], []).append(str(int(row["Mesa"])))

        total  = len(datos.mozos)
        ocup   = sum(1 for m in datos.mozos if m[1] in mesas_por_mozo)
        libres = total - ocup

        var_total.set(str(total))
        var_ocup.set(str(ocup))
        var_libres.set(str(libres))

        for m in datos.mozos:
            mesas = mesas_por_mozo.get(m[1], [])
            ocupado = len(mesas) > 0

            fila = Frame(frame_scroll, bg='#16213e')
            fila.pack(fill="x", padx=8, pady=4)

            # Avatar con iniciales
            iniciales = m[1][:2].upper()
            av = Frame(fila, bg='#0f3460', width=34, height=34)
            av.pack(side=LEFT)
            av.pack_propagate(False)
            Label(av, text=iniciales, font=("Arial", 11, "bold"),
                  bg='#0f3460', fg='#e0e0e0').place(relx=0.5, rely=0.5, anchor="center")

            # Nombre
            Label(fila, text=m[1].title(), font=("Arial", 11),
                  bg='#16213e', fg='#e0e0e0', width=10, anchor="w"
                  ).pack(side=LEFT, padx=8)

            # Badge de estado
            if ocupado:
                badge_bg   = "#f39c12"
                badge_fg   = "#3d2000"
                badge_text = f"Ocupado — Mesa{'s' if len(mesas) > 1 else ''} {', '.join(mesas)}"
            else:
                badge_bg   = "#2ecc71"
                badge_fg   = "#0a3d1f"
                badge_text = "Libre"

            Label(fila, text=badge_text, font=("Arial", 10, "bold"),
                  bg=badge_bg, fg=badge_fg,
                  padx=8, pady=2).pack(side=RIGHT)

            # Separador
            Frame(frame_scroll, bg='#2a2a4e', height=1).pack(fill="x", padx=8)

        frame_scroll.update_idletasks()
        canvas_mozos.configure(scrollregion=canvas_mozos.bbox("all"))

    # Cargar datos al iniciar
    logica.actualizar_lista_mozos(tabla_mozos)
    actualizar_stats()


# ============================================================
# TAB 3 — MESAS (función interna)
# ============================================================

def _construir_tab_mesas(tab3):

    frame_mesas = Frame(tab3, bd=1, relief=RIDGE, padx=20, pady=20, bg='#1a1a2e')
    frame_mesas.pack(fill="both", expand=True)

    # Tabla de mesas
    tabla_mesas = ttk.Treeview(frame_mesas,
                                columns=("Mesa", "Estado", "Mozo"),
                                show="headings")
    tabla_mesas.heading("Mesa",   text="Mesa")
    tabla_mesas.heading("Estado", text="Estado")
    tabla_mesas.heading("Mozo",   text="Mozo")
    tabla_mesas.pack(fill="both", expand=True)

    # Cargar datos iniciales en la tabla
    for _, row in datos.df_mesas.iterrows():
        tabla_mesas.insert("", "end", values=(row["Mesa"], row["Estado"], row["Mozo"]))

    # Botones de acción (Ocupar/Liberar se movieron a la pestaña Restaurante)
    botones_mesas = [
        ("Guardar Estado", "lightblue",  lambda: logica.guardar_mesas()),
        ("Cargar Estado",  "orange",     lambda: logica.cargar_mesas(tabla_mesas)),
        ("Liberar Todas",  "red",        lambda: logica.liberar_todas(tabla_mesas)),
        ("Agregar Mesa",   "lightblue",  lambda: logica.agregar_mesa(tabla_mesas)),
        ("Eliminar Mesa",  "gray",       lambda: logica.eliminar_mesa(tabla_mesas)),
    ]

    for texto, color, comando in botones_mesas:
        btn = Button(frame_mesas, text=texto, bg=color, command=comando)
        if color == "red":
            btn.config(fg="#e0e0e0")
        if color == "gray":
            btn.config(fg="#e0e0e0")
        btn.pack(side=LEFT, padx=10)

    return tabla_mesas


# ============================================================
# TAB 4 — HISTORIAL (función interna)
# ============================================================

def _construir_tab_historial(tab4):
    """
    Construye la pestaña de historial con dos subtabs:
    - Historial de Pedidos: tabla con todos los recibos
    - Resumen por Mozo: estadísticas filtradas por rango de fechas
    Devuelve el widget tabla_historial para que generar_recibo
    pueda agregar filas en tiempo real.
    """
    import datos

    # Subtabs dentro de la pestaña Historial
    subtabs = ttk.Notebook(tab4)
    subtabs.config(style='Dark.TNotebook')
    subtabs.pack(fill="both", expand=True)

    sub1 = Frame(subtabs, bg='#1a1a2e')   # Historial de pedidos
    sub2 = Frame(subtabs, bg='#1a1a2e')   # Resumen por mozo

    subtabs.add(sub1, text="Historial de Pedidos")
    subtabs.add(sub2, text="Resumen por Mozo")

    # --------------------------------------------------------
    # SUBTAB 1 — Historial de Pedidos (igual que antes)
    # --------------------------------------------------------
    frame = Frame(sub1, bd=1, relief=RIDGE, padx=20, pady=20, bg='#1a1a2e')
    frame.pack(fill="both", expand=True)

    Label(frame, text="Historial de Pedidos",
          font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#e0e0e0").pack(pady=10)

    columnas = ("Fecha", "Hora", "Recibo", "Mesa", "Mozo", "Subtotal", "Impuestos", "Total")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=15)

    anchos = [90, 60, 90, 60, 100, 80, 80, 80]
    for col, ancho in zip(columnas, anchos):
        tabla.heading(col, text=col)
        tabla.column(col, width=ancho, anchor="center")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)
    tabla.pack(side="left", fill="both", expand=True)
    scroll.pack(side="left", fill="y")

    for _, row in datos.df_historial.iterrows():
        tabla.insert("", "end", values=tuple(row))

    frame_botones = Frame(sub1, pady=10, bg='#1a1a2e')
    frame_botones.pack()

    def limpiar_historial():
        import pandas as pd
        from tkinter import messagebox
        if messagebox.askyesno("Limpiar historial",
                               "¿Seguro que querés borrar todo el historial?\nEsta acción no se puede deshacer."):
            datos.df_historial = pd.DataFrame(columns=datos.HISTORIAL_COLUMNAS)
            datos.df_historial.to_csv(datos.HISTORIAL_CSV, index=False)
            for item in tabla.get_children():
                tabla.delete(item)

    Button(frame_botones, text="Limpiar Historial",
           bg="#e94560", fg="#e0e0e0", font=("Arial", 11),
           command=limpiar_historial).pack(side="left", padx=10)

    # --------------------------------------------------------
    # SUBTAB 2 — Resumen por Mozo con filtro de fechas
    # --------------------------------------------------------
    _construir_resumen_mozos(sub2)

    return tabla


def _construir_resumen_mozos(sub2):
    """
    Subtab con filtro de fechas y tabla de resumen por mozo.
    Muestra: Mozo | Mesas Atendidas | Total Vendido
    usando groupby de pandas sobre el historial filtrado.
    """
    import datos
    import pandas as pd
    from datetime import datetime

    frame_top = Frame(sub2, pady=15, bg='#1a1a2e')
    frame_top.pack(fill="x", padx=20)

    Label(frame_top, text="Resumen por Mozo",
          font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#e0e0e0").pack(pady=(0, 10))

    # --- Fila de filtros ---
    frame_filtros = Frame(frame_top, bg='#1a1a2e')
    frame_filtros.pack()

    Label(frame_filtros, text="Desde:", font=("Arial", 11), bg="#1a1a2e", fg="#e0e0e0").grid(row=0, column=0, padx=5)
    Label(frame_filtros, text="Hasta:", font=("Arial", 11), bg="#1a1a2e", fg="#e0e0e0").grid(row=0, column=2, padx=5)

    if TKCALENDAR_OK:
        # DateEntry: calendario desplegable, formato dd/mm/yyyy
        entry_desde = DateEntry(frame_filtros, font=("Arial", 11), width=12,
                                date_pattern="dd/mm/yyyy",
                                background="darkblue", foreground="white",
                                borderwidth=2)
        entry_hasta = DateEntry(frame_filtros, font=("Arial", 11), width=12,
                                date_pattern="dd/mm/yyyy",
                                background="darkblue", foreground="white",
                                borderwidth=2)
    else:
        # Fallback si tkcalendar no está instalado
        entry_desde = Entry(frame_filtros, font=("Arial", 11), width=12)
        entry_desde.insert(0, "dd/mm/aaaa")
        entry_hasta = Entry(frame_filtros, font=("Arial", 11), width=12)
        entry_hasta.insert(0, "dd/mm/aaaa")

    entry_desde.grid(row=0, column=1, padx=5)
    entry_hasta.grid(row=0, column=3, padx=5)

    # --- Tabla de resultados ---
    frame_tabla = Frame(sub2, padx=20, bg='#1a1a2e')
    frame_tabla.pack(fill="both", expand=True)

    cols_resumen = ("Mozo", "Mesas Atendidas", "Total Vendido")
    tabla_resumen = ttk.Treeview(frame_tabla, columns=cols_resumen,
                                  show="headings", height=10)
    tabla_resumen.heading("Mozo",            text="Mozo")
    tabla_resumen.heading("Mesas Atendidas", text="Mesas Atendidas")
    tabla_resumen.heading("Total Vendido",   text="Total Vendido ($)")
    tabla_resumen.column("Mozo",            width=150, anchor="center")
    tabla_resumen.column("Mesas Atendidas", width=140, anchor="center")
    tabla_resumen.column("Total Vendido",   width=150, anchor="center")

    scroll_r = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_resumen.yview)
    tabla_resumen.configure(yscrollcommand=scroll_r.set)
    tabla_resumen.pack(side="left", fill="both", expand=True)
    scroll_r.pack(side="left", fill="y")

    # --- Etiqueta de totales generales ---
    var_totales = StringVar()
    Label(sub2, textvariable=var_totales,
          font=("Arial", 11, "bold"), fg="#e0e0e0").pack(pady=8)

    # --- Función que calcula el resumen ---
    def calcular_resumen():
        from tkinter import messagebox

        # Obtener fechas: DateEntry devuelve objeto date, Entry devuelve string
        try:
            if TKCALENDAR_OK:
                fecha_desde = datetime.combine(entry_desde.get_date(), datetime.min.time())
                fecha_hasta = datetime.combine(entry_hasta.get_date(), datetime.min.time())
            else:
                desde_str = entry_desde.get().strip()
                hasta_str = entry_hasta.get().strip()
                fecha_desde = datetime.strptime(desde_str, "%d/%m/%Y")
                fecha_hasta = datetime.strptime(hasta_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Fecha inválida",
                                 "Usá el formato dd/mm/aaaa.\nEjemplo: 15/03/2026")
            return

        if fecha_desde > fecha_hasta:
            messagebox.showerror("Rango inválido",
                                 "La fecha de inicio no puede ser mayor a la fecha de fin.")
            return

        df = datos.df_historial.copy()
        if df.empty:
            messagebox.showinfo("Sin datos", "El historial está vacío.")
            return

        # Convertir la columna Fecha a datetime para poder comparar
        df["Fecha_dt"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y", dayfirst=True)

        # Filtrar por rango
        df_filtrado = df[
            (df["Fecha_dt"] >= fecha_desde) &
            (df["Fecha_dt"] <= fecha_hasta)
        ]

        if df_filtrado.empty:
            messagebox.showinfo("Sin datos",
                                "No hay pedidos en el rango de fechas seleccionado.")
            var_totales.set("")
            for item in tabla_resumen.get_children():
                tabla_resumen.delete(item)
            return

        # Convertir Total a número (viene como string "$15.12" o "15.12")
        df_filtrado = df_filtrado.copy()
        df_filtrado["Total_num"] = (
            df_filtrado["Total"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.strip()
            .astype(float)
        )

        # groupby: agrupar por mozo, contar mesas y sumar total
        resumen = df_filtrado.groupby("Mozo").agg(
            Mesas=("Mesa",      "count"),
            Total=("Total_num", "sum")
        ).reset_index().sort_values("Total", ascending=False)

        # Limpiar tabla y cargar resultados
        for item in tabla_resumen.get_children():
            tabla_resumen.delete(item)

        for _, row in resumen.iterrows():
            tabla_resumen.insert("", "end", values=(
                row["Mozo"],
                int(row["Mesas"]),
                f"${round(row['Total'], 2)}"
            ))

        # Totales generales al pie
        total_general  = resumen["Total"].sum()
        mesas_general  = resumen["Mesas"].sum()
        mejor_mozo     = resumen.iloc[0]["Mozo"]
        var_totales.set(
            f"Total del período: ${round(total_general, 2)}  |  "
            f"Mesas atendidas: {int(mesas_general)}  |  "
            f"Mozo estrella: {mejor_mozo} ⭐"
        )

    Button(frame_filtros, text="Ver Resumen", bg="#2ecc71",
           font=("Arial", 11, "bold"),
           command=calcular_resumen).grid(row=0, column=4, padx=15)


# ============================================================
# TAB 5 — MENÚ (función interna)
# ============================================================

def _construir_tab_menu(tab5, recargar_menu_ref=None):
    """Pestaña de gestión del menú: agregar, editar y eliminar productos."""

    frame = Frame(tab5, bg='#1a1a2e', padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    Label(frame, text="Gestión del Menú",
          font=("Arial", 14, "bold"), bg='#1a1a2e', fg='#e0e0e0').pack(pady=(0, 15))

    # ---- Formulario de alta ----
    frame_form = Frame(frame, bg='#16213e', padx=15, pady=12)
    frame_form.pack(fill="x", pady=(0, 15))

    Label(frame_form, text="Nombre:", font=("Arial", 11), bg='#16213e', fg='#e0e0e0').grid(row=0, column=0, padx=8, pady=4, sticky="w")
    entry_nombre = Entry(frame_form, font=("Arial", 11), width=18,
                         bg='#1a1a2e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_nombre.grid(row=0, column=1, padx=8, pady=4)

    Label(frame_form, text="Precio ($):", font=("Arial", 11), bg='#16213e', fg='#e0e0e0').grid(row=0, column=2, padx=8, pady=4, sticky="w")
    entry_precio = Entry(frame_form, font=("Arial", 11), width=10,
                         bg='#1a1a2e', fg='#e0e0e0', insertbackground='#e0e0e0')
    entry_precio.grid(row=0, column=3, padx=8, pady=4)

    Label(frame_form, text="Categoría:", font=("Arial", 11), bg='#16213e', fg='#e0e0e0').grid(row=0, column=4, padx=8, pady=4, sticky="w")
    combo_cat = ttk.Combobox(frame_form, values=["comida", "bebida", "postre"],
                              state="readonly", width=10, font=("Arial", 11))
    combo_cat.current(0)
    combo_cat.grid(row=0, column=5, padx=8, pady=4)

    Button(frame_form, text="Agregar Producto", bg='#2ecc71', fg='#0a3d1f',
           font=("Arial", 10, "bold"),
           command=lambda: [logica.agregar_producto(entry_nombre, entry_precio, combo_cat, tabla_menu),
                           recargar_menu_ref[0]() if recargar_menu_ref and recargar_menu_ref[0] else None]
           ).grid(row=0, column=6, padx=15, pady=4)

    # ---- Tabla del menú ----
    frame_tabla = Frame(frame, bg='#1a1a2e')
    frame_tabla.pack(fill="both", expand=True)

    tabla_menu = ttk.Treeview(frame_tabla,
                               columns=("Nombre", "Precio", "Categoría"),
                               show="headings", height=16)
    tabla_menu.heading("Nombre",    text="Nombre")
    tabla_menu.heading("Precio",    text="Precio ($)")
    tabla_menu.heading("Categoría", text="Categoría")
    tabla_menu.column("Nombre",    width=200, anchor="w")
    tabla_menu.column("Precio",    width=100, anchor="center")
    tabla_menu.column("Categoría", width=100, anchor="center")

    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_menu.yview)
    tabla_menu.configure(yscrollcommand=scroll.set)
    tabla_menu.pack(side=LEFT, fill="both", expand=True)
    scroll.pack(side=LEFT, fill="y")

    # ---- Botones de acción ----
    frame_btns = Frame(frame, bg='#1a1a2e', pady=10)
    frame_btns.pack()

    Button(frame_btns, text="Editar Producto", bg='#f39c12', fg='#3d2000',
           font=("Arial", 10, "bold"),
           command=lambda: [logica.editar_producto(tabla_menu),
                           recargar_menu_ref[0]() if recargar_menu_ref and recargar_menu_ref[0] else None]
           ).pack(side=LEFT, padx=8)

    Button(frame_btns, text="Eliminar Producto", bg='#e94560', fg='#e0e0e0',
           font=("Arial", 10, "bold"),
           command=lambda: [logica.eliminar_producto(tabla_menu),
                           recargar_menu_ref[0]() if recargar_menu_ref and recargar_menu_ref[0] else None]
           ).pack(side=LEFT, padx=8)

    # Cargar productos al iniciar
    logica.actualizar_tabla_menu(tabla_menu)
