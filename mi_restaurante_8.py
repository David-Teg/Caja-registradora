from tkinter import *
import random
from datetime import datetime 
from tkinter import filedialog, messagebox
import csv
import re
import os
import sys


operador = ''

precios_comida = [1.32, 1.65, 2.31, 3.22, 1.22, 1.99, 2.05, 2.65]
precios_bebidas = [0.25, 0.99, 1.21, 1.54, 1.08, 1.10, 2.00, 1.58]
precios_postres = [1.54, 1.68, 1.32, 1.97, 2.55, 2.14, 1.94, 1.74]

# Función para validar la fecha de nacimiento
def validar_fecha(fecha):
    """
    Valida si una fecha dada en formato de cadena es válida.

    Intenta convertir la cadena de fecha proporcionada al formato de fecha DD/MM/AAAA.
    Si la conversión es exitosa, la fecha es considerada válida y se retorna True.
    Si la conversión falla debido a un formato incorrecto o una fecha inválida, se captura
    la excepción y se retorna False.

    Args:
        fecha (str): La fecha en formato de cadena a validar.

    Returns:
        bool: True si la fecha es válida, False en caso contrario.
    """
    try:
        # Intenta convertir la fecha a un objeto datetime utilizando el formato DD/MM/AAAA
        return bool(datetime.strptime(fecha, "%d/%m/%Y"))
    except ValueError:
        # Si ocurre un error (fecha no válida), retorna False
        return False

# Función para solicitar los datos del usuario
def solicitar_datos():
    """
    Solicita los datos del usuario y los valida.

    Pide al usuario que ingrese los siguientes datos:
        - ID de usuario (solo números)
        - Nombre (solo letras)
        - Apellido (solo letras)
        - Número de documento (solo números, 8 dígitos)
        - Fecha de nacimiento (DD/MM/AAAA)
        - Teléfono (solo números, entre 7 y 15 dígitos)
        - Domicilio (no puede estar vacío)

    Muestra un resumen de los datos ingresados y pide al usuario que confirme
    si son correctos. Si no son correctos, vuelve a solicitar los datos.

    Returns:
        dict: Los datos del usuario si son correctos, None si no son correctos.
    """
    print("Por favor, ingrese los datos requeridos:")

    # Solicita el ID de usuario y valida que sea un número positivo
    while True:
        try:
            id_usuario = int(input("ID de usuario (solo números): "))
            if id_usuario <= 0:
                raise ValueError("El ID debe ser un número positivo.")
        except ValueError as e:
            print(f"Error: {e}")
            continue
        break

    # Solicita el nombre y valida que contenga solo letras
    while True:
        nombre = input("Nombre: ").strip()
        if not nombre.isalpha():
            print("Error: El nombre solo debe contener letras.")
            continue
        break

    # Solicita el apellido y valida que contenga solo letras
    
    while True:
        apellido = input("Apellido: ").strip()
        if not apellido.isalpha():
            print("Error: El apellido solo debe contener letras.")
            continue
        break

    # Solicita el número de documento y valida que sea un número de 8 dígitos
    while True:
        try:
            documento = input("Número de documento (solo números): ").strip()
            if not documento.isdigit() or len(documento) != 8:
                raise ValueError("El documento debe tener exactamente 8 dígitos.")
        except ValueError as e:
            print(f"Error: {e}")
            continue
        break

    # Solicita la fecha de nacimiento y valida su formato (DD/MM/AAAA)
    while True:
        fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ").strip()
        if not validar_fecha(fecha_nacimiento):
            print("Error: Fecha inválida. Use el formato DD/MM/AAAA.")
            continue
        break

    # Solicita el teléfono y valida que sea un número con entre 7 y 15 dígitos
    while True:
        telefono = input("Teléfono (solo números): ").strip()
        if not telefono.isdigit() or len(telefono) < 7 or len(telefono) > 15:
            print("Error: El teléfono debe tener entre 7 y 15 dígitos.")
            continue
        break

    # Solicita el domicilio y valida que no esté vacío
    while True:
        domicilio = input("Domicilio: ").strip()
        if not domicilio:
            print("Error: El domicilio no puede estar vacío.")
            continue
        break


    # Muestra un resumen de los datos ingresados por el usuario
    print("\nResumen de datos ingresados:")
    print(f"ID: {id_usuario}")
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Documento: {documento}")
    print(f"Fecha de nacimiento: {fecha_nacimiento}")
    print(f"Teléfono: {telefono}")
    print(f"Domicilio: {domicilio}")

    # Pide al usuario que confirme si los datos son correctos
    confirmar = input("\n¿Son correctos estos datos? (S/N): ").strip().lower()
    if confirmar == 's':
        
        return {
            "ID": id_usuario,
            "Nombre": nombre,
            "Apellido": apellido,
            "Documento": documento,
            "Fecha de nacimiento": fecha_nacimiento,
            "Teléfono": telefono,
            "Domicilio": domicilio,
        }
    else:
        # Si no son correctos, solicita los datos nuevamente
        print("Volviendo a solicitar los datos...\n")
        return solicitar_datos()

# Función para guardar los datos de usuario en un archivo CSV
def guardar_usuario_en_csv(datos_usuario):
    """
    Guarda los datos de usuario en un archivo CSV.

    Abre el archivo en modo 'a' (agregar) para no sobrescribir los datos existentes.
    Si el archivo no existe o está vacío, escribe los encabezados.
    Luego, escribe los datos del nuevo usuario en el archivo.

    Args:
        datos_usuario (dict): Los datos del usuario a guardar.
    """
    archivo = "usuarios.csv"
    archivo_existe = os.path.exists(archivo)  # Verifica si el archivo existe
    
    # Abre el archivo en modo 'a' (agregar) para no sobrescribir los datos existentes
    with open(archivo, mode='a', newline='') as f: # Abre el archivo en modo 'a' (agregar)
        writer = csv.DictWriter(f, fieldnames=["ID", "Nombre", "Apellido", "Documento", "Fecha de nacimiento", "Teléfono", "Domicilio"])
        
        if not archivo_existe or os.stat(archivo).st_size == 0:
            writer.writeheader()  # Escribe los encabezados si el archivo es nuevo o está vacío
        
        writer.writerow(datos_usuario)  # Escribe los datos del nuevo usuario


# Función para verificar si el usuario ya está registrado
def verificar_usuario_existente():
    """
    Verifica si un usuario ya está registrado en el sistema.

    Lee el archivo CSV de usuarios y solicita al usuario ingresar su ID para iniciar sesión.
    Si el archivo no existe o no hay usuarios registrados, informa al usuario y permite crear uno nuevo.
    Si el ID ingresado coincide con un usuario registrado, devuelve los datos del usuario.
    Si el ID no coincide, solicita nuevamente el ID.

    Returns:
        dict or None: Los datos del usuario si el ID es válido, None si no hay usuarios registrados.
    """
    archivo = "usuarios.csv"
    # Verifica si el archivo de usuarios existe
    if not os.path.exists(archivo):
        print("No se encontraron usuarios registrados. Creando un nuevo usuario...\n")
        return None

    # Lee el archivo CSV
    with open(archivo, mode='r') as f: # Abre el archivo en modo lectura
        reader = csv.DictReader(f) # Crea un lector de CSV
        usuarios = list(reader) # Convierte el lector a una lista de usuarios

    # Si no hay usuarios, informa al usuario y permite crear uno nuevo
    if not usuarios:
        print("No se encontraron usuarios registrados. Creando un nuevo usuario...\n")
        return None

    # Solicita el ID de usuario para iniciar sesión
    while True: # Ciclo para solicitar el ID de usuario hasta que sea valido
        try: # Intenta convertir el ID ingresado a un entero
            id_usuario = int(input("Ingrese su ID de usuario para iniciar sesión: "))
        except ValueError: # Si ocurre un error, informa al usuario
            print("Error: Ingrese un ID válido.")
            continue # Vuelve a solicitar el ID

        # Busca el ID ingresado en los usuarios registrados
        for usuario in usuarios:
            if int(usuario["ID"]) == id_usuario: # Verifica si el ID coincide
                print(f"Bienvenido, {usuario['Nombre']} {usuario['Apellido']}!") # Muestra un mensaje de bienvenida
                return usuario   # Si el ID coincide, devuelve los datos del usuario

        # Si el ID no coincide con ninguno de los usuarios registrados, informa al usuario

        print("ID de usuario no encontrado. Intente nuevamente.")

# Función para agregar un nuevo usuario
def agregar_nuevo_usuario():
    """
    Agrega un nuevo usuario al sistema.

    Solicita los datos de usuario con la función solicitar_datos() y
    los guarda en un archivo CSV con la función guardar_usuario_en_csv().

    Luego, muestra un mensaje informando que el usuario ha sido creado con éxito.
    """
    print("\nAgregando un nuevo usuario...\n")
    # Solicita los datos del nuevo usuario
    datos_usuario = solicitar_datos()
    # Guarda los datos en el archivo CSV
    guardar_usuario_en_csv(datos_usuario)
    print("\nUsuario creado con éxito.\n")

# Función para iniciar sesión o crear un nuevo usuario
def iniciar_sesion_o_crear_usuario():
    """
    Inicia el programa principal.

    Muestra un menú para que el usuario elija si desea iniciar sesión como usuario existente
    o crear un nuevo usuario. Si elige iniciar sesión, verifica si el usuario existe.
    Si elige crear un nuevo usuario, agrega el usuario al archivo CSV.
    Si la opción no es válida, pide una nueva elección.

    Returns:
        bool: True si el usuario existe o se crea con éxito, False en caso contrario
    """
    while True:
        print("\nBienvenido al sistema.")
        # Muestra las opciones y solicita la elección
        opcion = input("¿Desea iniciar sesión como usuario existente (E) o crear un nuevo usuario (N)? (E/N): ").strip().lower()

        if opcion == 'e':
            # Si elige iniciar sesión, verifica si el usuario existe
            usuario_existente = verificar_usuario_existente()
            if usuario_existente:
                print("\nIniciando el programa...\n")
                return True
        elif opcion == 'n':
            # Si elige crear un nuevo usuario, agrega el usuario
            agregar_nuevo_usuario()
            return True
        else:
            # Si la opción no es válida, pide una nueva elección
            print("Opción no válida. Elija E o N.")

# Iniciar el programa
def iniciar_programa(): # Función que maneja el inicio de sesión o la creación de usuario
    # Llama a la función que maneja el inicio de sesión o la creación de usuario
    """
    Inicia el programa principal.

    Llama a la función que maneja el inicio de sesión o la creación de usuario,
    y si se inicia correctamente, muestra un mensaje de confirmación.
    """
    if iniciar_sesion_o_crear_usuario(): 
        print("\nPrograma iniciado exitosamente.")

# Llamamos a la función principal para iniciar el programa
if __name__ == "__main__": # Verifica si el archivo se esta ejecutando directamente
    iniciar_programa() 

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
    fecha = datetime.now()
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
        
    for variables in variables_comida:
        variables.set(0)
    for variables in variables_bebidas:
        variables.set(0)
    for variables in variables_postres:
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




#evitar que la pantalla se cierre
aplicacion.mainloop()