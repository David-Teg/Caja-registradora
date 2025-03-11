import csv
import os
from tkinter import *
import random


operador = ''

precios_comida = [1.32, 1.65, 2.31, 3.22, 1.22, 1.99, 2.05, 2.65]
precios_bebidas = [0.25, 0.99, 1.21, 1.54, 1.08, 1.10, 2.00, 1.58]
precios_postres = [1.54, 1.68, 1.32, 1.97, 2.55, 2.14, 1.94, 1.74]

# --- Gestión de Clientes ---

def agregar_cliente():
    id_cliente = input("Ingrese el ID del cliente: ")
    nombre = input("Ingrese el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    documento = input("Ingrese el número de documento: ")
    fecha_nacimiento = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
    telefono = input("Ingrese el teléfono: ")
    domicilio = input("Ingrese el domicilio: ")

    with open('clientes.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_cliente, nombre, apellido, documento, fecha_nacimiento, telefono, domicilio])
        print("Cliente agregado exitosamente.")

def consultar_clientes():
    if not os.path.exists('clientes.csv'):
        print("No hay clientes registrados.")
        return
    
    with open('clientes.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def eliminar_cliente():
    id_cliente = input("Ingrese el ID del cliente a eliminar: ")
    clientes = []

    with open('clientes.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != id_cliente:  # Mantener solo los que no coinciden con el ID
                clientes.append(row)

    with open('clientes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(clientes)
        print("Cliente eliminado exitosamente.")

def actualizar_cliente():
    id_cliente = input("Ingrese el ID del cliente a actualizar: ")
    clientes = []

    with open('clientes.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id_cliente:
                nombre = input("Ingrese el nuevo nombre del cliente: ")
                apellido = input("Ingrese el nuevo apellido del cliente: ")
                documento = input("Ingrese el nuevo número de documento: ")
                fecha_nacimiento = input("Ingrese la nueva fecha de nacimiento (YYYY-MM-DD): ")
                telefono = input("Ingrese el nuevo teléfono: ")
                domicilio = input("Ingrese el nuevo domicilio: ")
                clientes.append([id_cliente, nombre, apellido, documento, fecha_nacimiento, telefono, domicilio])
                print("Cliente actualizado exitosamente.")
            else:
                clientes.append(row)

    with open('clientes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(clientes)

def menu_clientes():
    while True:
        print("\n--- Menú de Gestión de Clientes ---")
        print("1. Ingreso de Datos")
        print("2. Consulta de Datos")
        print("3. Eliminación de Datos")
        print("4. Actualización de Datos")
        print("5. Listar Clientes")
        print("6. Continuar al Programa Principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_cliente()
        elif opcion == '2':
            consultar_clientes()
        elif opcion == '3':
            eliminar_cliente()
        elif opcion == '4':
            actualizar_cliente()
        elif opcion == '5':
            consultar_clientes()  # Para listar clientes
        elif opcion == '6':
            print("Cargando el programa principal...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# --- Programa Principal ---
def programa_principal():
    root = Tk()
    root.title("Gestión de Restaurante")
    root.geometry("1160x600+0+0")

def click_boton(numero):
    global operador
    operador = operador + numero
    visor_calculadora.delete(0, END)
    visor_calculadora.insert(END,operador)
    
def borrar():
    global operador
    operador = ''
    visor_calculadora.delete(0, END)   
    
def obtener_resultado():
    global operador
    resultado = str(eval(operador))
    visor_calculadora.delete(0, END)
    visor_calculadora.insert(0, resultado)
    operador = ''
    
def revisar_check():
    x=0
    for c in cuadros_comida:
        if variables_comida[x].get() == 1:
            cuadros_comida[x].config(state=NORMAL)
            if cuadros_comida[x].get()=='0':
                cuadros_comida[x].delete(0, END)
            cuadros_comida[x].focus()
        else:
            cuadros_comida[x].config(state=DISABLED)
            texto_comida[x].set('0')
        x += 1
        
    x=0
    for c in cuadros_bebidas:
        if variables_bebidas[x].get() == 1:
            cuadros_bebidas[x].config(state=NORMAL)
            if cuadros_bebidas[x].get()=='0':
                cuadros_bebidas[x].delete(0, END)
            cuadros_bebidas[x].focus()
        else:
            cuadros_bebidas[x].config(state=DISABLED)
            texto_bebidas[x].set('0')
        x += 1

    x=0
    for c in cuadros_postres:
        if variables_postres[x].get() == 1:
            cuadros_postres[x].config(state=NORMAL)
            if cuadros_postres[x].get()=='0':
                cuadros_postres[x].delete(0, END)
            cuadros_postres[x].focus()
        else:
            cuadros_postres[x].config(state=DISABLED)
            texto_postres[x].set('0')
        x += 1
        
def total():
        sub_total_comida = 0
        p = 0
        
        for cantidad in texto_comida:
            sub_total_comida += float(cantidad.get()) * precios_comida[p]

            p+=1
        print(sub_total_comida)
        
        sub_total_bebidas = 0
        p = 0
        for cantidad in texto_bebidas:
            sub_total_bebidas +=  float(cantidad.get()) * precios_bebidas[p]
            p+=1
        print(sub_total_bebidas)
        
        sub_total_postre = 0
        p = 0
        for cantidad in texto_postres:
            sub_total_postre += float(cantidad.get()) * precios_postres[p]
            p+=1
        print(sub_total_postre)
            
        sub_total = sub_total_bebidas + sub_total_comida + sub_total_postre
        impuestos = sub_total * 0.5
        total = sub_total + impuestos
        
        var_costo_bebidas.set(f'${round(sub_total_bebidas, 2)}')
        var_costo_comida.set(f'${round(sub_total_comida, 2)}')
        var_costo_postres.set(f'${round(sub_total_postre, 2)}')
        var_subtotal.set(f'{round(sub_total, 2)}')
        var_impuestos.set(f'{round(sub_total, 2)}')
        var_total.set(f'{round(sub_total, 2)}')

def recibo():
    texto_recibo.delete(1.0, END)
    num_recibo = f'N# - {random.randint(1000, 9999)}'
    fecha = datetime.datetime.now()
    fecha_recibo = f'{fecha.day} / {fecha.month} / {fecha.year} - {fecha.hour}:{fecha.minute}'
    texto_recibo.insert(END, f'Datos:\t{num_recibo}\t\t{fecha_recibo}\n ')
    texto_recibo.insert(END, f'*' * 52 + '\n')
    texto_recibo.insert(END, 'Items\t\tCant.\tCosto Items\n')
    texto_recibo.insert(END, f'-' * 54 + '\n')
    
    x = 0 
    for comida in texto_comida:
        if comida.get() != '0':
            texto_recibo.insert(END, f'{lista_comida[x]}\t\t{comida.get()}\t'
                                f'$ {int(comida.get()) * precios_comida[x]}\n')
        x += 1
    
    x = 0    
    for bebidas in texto_bebidas:
        if bebidas.get() != '0':
            texto_recibo.insert(END, f'{lista_bebidas[x]}\t\t{bebidas.get()}\t'
                                f'$ {int(bebidas.get()) * precios_bebidas[x]}\n')
        x += 1
    x = 0    
    for postres in texto_postres:
        if postres.get() != '0':
            texto_recibo.insert(END, f'{lista_postre[x]}\t\t{postres.get()}\t'
                                f'$ {int(postres.get()) * precios_postres[x]}\n')
        x += 1
    
    texto_recibo.insert(END, f'-' * 54 + '\n')
    texto_recibo.insert(END, f'Costo de la Comida:\t\t\t{var_costo_comida.get()} ')
    texto_recibo.insert(END, f'Costo de la Bebida:\t\t\t{var_costo_bebidas.get()} ')
    texto_recibo.insert(END, f'Costo de la Postre:\t\t\t{var_costo_postres.get()} ')
    texto_recibo.insert(END, f'-' * 54 + '\n')   
    texto_recibo.insert(END, f'Sub-total:\t\t\t{var_subtotal.get()}\n ')
    texto_recibo.insert(END, f'Imouestos:\t\t\t{var_impuestos.get()}\n ')
    texto_recibo.insert(END, f'Total:\t\t\t{var_total.get()}\n ')
    texto_recibo.insert(END, f'*' * 47 + '\n')
    texto_recibo.insert(END, 'Lo esperamos pronto')
    
def guardar():
    info_recibo = texto_recibo.get(1.0, END)
    archivo= filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    archivo.write(info_recibo)
    archivo.close()
    messagebox.showinfo('Informacion', 'Su recibo ha sido guardado')
    
def resetear():
    texto_recibo.delete(1.0, END)
    
    for texto in texto_comida:
        texto.set('0')
    for texto in texto_bebidas:
        texto.set('0')
    for texto in texto_postres:
        texto.set('0')
        
    for cuadro in cuadros_comida:
        cuadro.config(state=DISABLED)
    for cuadro in cuadros_postres:
        cuadro.config(state=DISABLED)
    for cuadro in cuadros_bebidas:
        cuadro.config(state=DISABLED)
        
    for variable in variables_comida:
        variables.set(0)
    for variable in variables_bebidas:
        variables.set(0)
    for variable in variables_postres:
        variables.set(0)
        
    var_costo_comida.set('')
    var_costo_bebidas.set('')
    var_costo_postres.set('')
    var_subtotal.set('')
    var_impuestos.set('')
    var_total.set('')
    
    
        
# iniciar tkinter
aplicacion = Tk()

    #tamaño de la ventana
aplicacion.geometry('1160x600+0+0')

#evitar maximizar
aplicacion.resizable(0, 0)

#titulo de la ventana
aplicacion.title('Mi Restaurante - Sistema Grastronómico')

#color de fondo de la ventana
aplicacion.config(bg='burlywood')

#panel superior
panel_superior = Frame(aplicacion, bd=1, relief=RIDGE)
panel_superior.pack(side=TOP)

#etiqueta titulo
etiqueta_titulo = Label(panel_superior, text='Sistema Gastronómico', fg='azure4',
                        font=('dosis', 58), bg='burlywood', width=27)

etiqueta_titulo.grid(row=0, column=0)

#panel izquierdo
panel_izquierdo = Frame(aplicacion, bd=1, relief=RIDGE)
panel_izquierdo.pack(side=LEFT)

#panel costos
panel_costo = Frame(panel_izquierdo, bd=1, relief=RIDGE, bg= 'azure4', padx=35)
panel_costo.pack(side=BOTTOM)

#panel comida
panel_comida = LabelFrame(panel_izquierdo, text='Comida',font=('dosis',19,'bold'), 
                        bd=1, relief= RIDGE, fg='azure4' )
panel_comida.pack(side=LEFT)

#panel bebidas
panel_bebidas = LabelFrame(panel_izquierdo, text='Bebidas',font=('dosis',19,'bold'), 
                        bd=1, relief= RIDGE, fg='azure4' )
panel_bebidas.pack(side=LEFT)

#panel postres
panel_postres = LabelFrame(panel_izquierdo, text='Postres',font=('dosis',19,'bold'), 
                        bd=1, relief= RIDGE, fg='azure4' )
panel_postres.pack(side=LEFT)

#panel derecha
panel_derecha = Frame(aplicacion, bd=1, relief=RIDGE)
panel_derecha.pack(side=RIGHT)

#panel calculadora
panel_calculadora = Frame(panel_derecha, bd=1, relief=RIDGE, bg='burlywood')
panel_calculadora.pack()

#panel recibo
panel_recibo = Frame(panel_derecha, bd=1, relief=RIDGE, bg='burlywood')
panel_recibo.pack()

#panel botones
panel_botones = Frame(panel_derecha, bd=1, relief=RIDGE, bg='burlywood')
panel_botones.pack()

#lista de produtos
lista_comida = ['pollo', 'cerdo', 'vacio', 'longitas', 'pizza', 'lazaña', 'spaguetti', 'milanesa']
lista_bebidas = ['cola', 'saborizada', 'agua', 'vino tinto', 'vino blnaco', 'cerveza', 'chop', 'exprimido']
lista_postre = ['flan', 'budin', 'torta', 'helado', 'fruta', 'yogur', 'queso', 'batata']

# genenerar items comida
variables_comida = []
cuadros_comida = []
texto_comida = []
contador = 0
for comida in lista_comida:
    #crear checkbutton
    variables_comida.append('')
    variables_comida[contador] = IntVar()
    comida = Checkbutton(panel_comida,
                        text=comida.title(),
                        font=('Dosis', 19, 'bold'), 
                        onvalue=1,
                        offvalue=0, 
                        variable=variables_comida[contador],
                        command=revisar_check)
    
    comida.grid(row=contador, 
                column=0, 
                sticky=W)
    
    #crear los cuadros de entrada
    cuadros_comida.append('')
    texto_comida.append('')
    texto_comida[contador] = StringVar() 
    texto_comida[contador].set('0')
    cuadros_comida[contador] = Entry(panel_comida,
                                    font=( 'Dosis', 18, 'bold'),
                                    bd=1,
                                    width=6,
                                    state=DISABLED,
                                    textvariable=texto_comida[contador])
    cuadros_comida[contador].grid(row=contador,
                                column=1)
    

    contador += 1
    
# genenerar items bbebidas
cuadros_bebidas = []
texto_bebidas = []
variables_bebidas = []

contador = 0
#crear checkbutton
for bebidas in lista_bebidas:
    variables_bebidas.append('')
    variables_bebidas[contador] = IntVar()
    bebidas = Checkbutton(panel_bebidas,
                        text=bebidas.title(),
                        font=('Dosis', 19, 'bold'), 
                        onvalue=1,
                        offvalue=0,
                        variable=variables_bebidas[contador],
                        command=revisar_check)
    bebidas.grid(row=contador,
                column=0,
                sticky=W)
    
    #crear los cuadros de entrada
    cuadros_bebidas.append('')
    texto_bebidas.append('')
    texto_bebidas[contador] = StringVar() 
    texto_bebidas[contador].set('0')
    cuadros_bebidas[contador] = Entry(panel_bebidas,
                                    font=( 'Dosis', 18, 'bold'),
                                    bd=1,
                                    width=6,
                                    state=DISABLED,
                                    textvariable=texto_bebidas[contador])
    
    cuadros_bebidas[contador].grid(row=contador,
                                column=1)
    contador += 1
    
# genenerar items postres
cuadros_postres = []
texto_postres = []
variables_postres = []

contador = 0
for postres in lista_postre: 
    #crear checkbutton
    variables_postres.append('')
    variables_postres[contador] = IntVar()
    postres = Checkbutton(panel_postres,
                        text=postres.title(),
                        font=('Dosis', 19, 'bold'), 
                        onvalue=1,
                        offvalue=0,
                        variable=variables_postres[contador],
                        command=revisar_check)
    postres.grid(row=contador,
                column=0, 
                sticky=W)
    
    #crear los cuadros de entrada
    cuadros_postres.append('')
    texto_postres.append('')
    texto_postres[contador] = StringVar() 
    texto_postres[contador].set('0')
    cuadros_postres[contador] = Entry(panel_postres,
                                    font=( 'Dosis', 18, 'bold'),
                                    bd=1,
                                    width=6,
                                    state=DISABLED,
                                    textvariable=texto_postres[contador])
    
    cuadros_postres[contador].grid(row=contador,
                                column=1)
    
    contador += 1

# variables
var_costo_comida = StringVar()
var_costo_bebidas = StringVar()
var_costo_postres = StringVar()
var_subtotal = StringVar()
var_impuestos = StringVar()
var_total = StringVar()


# etiquetas de costos y campos de entradas 
etiqueta_costo_comida = Label(panel_costo,
                            text='Costo Comida',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_costo_comida.grid(row=0, column=0)

texto_costo_comida = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_costo_comida)
texto_costo_comida.grid(row=0, column=1, padx=41)

# etiquetas de costos y campos de entradas 
etiqueta_costo_bebidas = Label(panel_costo,
                            text='Costo Bebidas',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_costo_bebidas.grid(row=1, column=0)

texto_costo_bebidas = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_costo_bebidas)
texto_costo_bebidas.grid(row=1, column=1, padx=41)

# etiquetas de costos y campos de entradas 
etiqueta_costo_postres = Label(panel_costo,
                            text='Costo Postres',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_costo_postres.grid(row=2, column=0)

texto_costo_postres = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_costo_postres)
texto_costo_postres.grid(row=2, column=1, padx=41)

# etiquetas de costos y campos de entradas 
etiqueta_subtotal = Label(panel_costo,
                            text='Subtotal',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_subtotal.grid(row=0, column=2)

texto_subtotal = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_subtotal)
texto_subtotal.grid(row=0, column=3, padx=41)

# etiquetas de costos y campos de entradas 
etiqueta_impuestos = Label(panel_costo,
                            text='Impuestos',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_impuestos.grid(row=1, column=2)

texto_impuestos = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_impuestos)
texto_impuestos.grid(row=1, column=3, padx=41)

# etiquetas de costos y campos de entradas 
etiqueta_total = Label(panel_costo,
                            text='Total',
                            font=('Dosis',12,'bold'),
                            bg='azure4',
                            fg='white',)
etiqueta_total.grid(row=2, column=2)

texto_total = Entry(panel_costo,
                            font=('Dosis',14,'bold'),
                            bd=1,
                            width=10,
                            state='readonly',
                            textvariable=var_total)
texto_total.grid(row=2, column=3, padx=41)

#botones
botones = ['total','recibo','guardar','resetear']
botones_creados = []
columnas = 0

for boton in botones:
    boton = Button(panel_botones,
                    text=boton.title(),
                    font=('Dosis', 14, 'bold'),
                    fg='white',
                    bg='azure4',
                    bd=1,
                    width=9)
    
    botones_creados.append(boton)

    boton.grid(row=0,
                column=columnas,)
    columnas += 1

botones_creados[0].config(command=total)
botones_creados[1].config(command=recibo)
botones_creados[2].config(command=guardar)
botones_creados[3].config(command=resetear)

#area de recibo
texto_recibo = Text(panel_recibo,
                    font=('Dosis', 12, 'bold'),
                    bd=1,
                    width=42,
                    height=10)

texto_recibo.grid(row=0,
                    column=0)

#calculadora

visor_calculadora = Entry(panel_calculadora,
                        font=('Dosis',16,'bold'),
                        width=32,
                        bd=1)

visor_calculadora.grid(row=0,
                    column=0,
                    columnspan=4)

botones_calculadora = ['7','8','9','+'
                    ,'4','5','6','-',
                    '1','2','3','x',
                    '=','B','0','/']

botones_guardados = []  

fila = 1
columna = 0

for boton in botones_calculadora:
    boton = Button(panel_calculadora,
                text=boton.title(),
                font=('Dosis',16,'bold'),
                fg='white',
                bg='azure4',
                bd=1,
                width=8)
    
    botones_guardados.append(boton)
    
    boton.grid(row=fila,
            column=columna)
    
    if columna == 3:
        fila += 1
    columna += 1
    if columna == 4:
        columna=0
        
botones_guardados[0].config(command=lambda : click_boton('7'))
botones_guardados[1].config(command=lambda : click_boton('8'))
botones_guardados[2].config(command=lambda : click_boton('9'))
botones_guardados[3].config(command=lambda : click_boton('+'))
botones_guardados[4].config(command=lambda : click_boton('4'))
botones_guardados[5].config(command=lambda : click_boton('5'))
botones_guardados[6].config(command=lambda : click_boton('6'))
botones_guardados[7].config(command=lambda : click_boton('-'))
botones_guardados[8].config(command=lambda : click_boton('1'))
botones_guardados[9].config(command=lambda : click_boton('2'))
botones_guardados[10].config(command=lambda : click_boton('3'))
botones_guardados[11].config(command=lambda : click_boton('*'))
botones_guardados[12].config(command=obtener_resultado)
botones_guardados[13].config(command=borrar)
botones_guardados[14].config(command=lambda : click_boton('0'))
botones_guardados[15].config(command=lambda : click_boton('/'))

root.mainloop()

# --- Flujo del Programa ---


if __name__ == "__main__":
    print("Bienvenido al Sistema de Gestión del Restaurante")
    menu_clientes()  # Submenú de clientes
    programa_principal()  # Programa gráfico principal
