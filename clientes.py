import tkinter as tk;
import re 
import styles
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import conectar_bd

def validar_labels (label):
    patron = r'^[a-zA-Z]+$'
    if re.match(patron, label):
        return True
    else:
        return False
    
def validar_celular (celular):
    patron = r'^\d+$'
    if re.match(patron, celular):
        return True
    else:
        return False

# Guarda cambios en la bd y verifica errores de parametros
def alta_cliente(entry_nombre, entry_apellido, entry_celular, entry_direccion, lista_clientes, top_cliente):

    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    celular = entry_celular.get()
    direccion = entry_direccion.get()

    if not nombre :
        messagebox.showerror("Error", "El nombre es obligatorio")
        return

    # Control de errores

    if not validar_labels(nombre):
        messagebox.showerror("Error", "El nombre solo debe llevar letras A-Z a-z")
        return
    
    if not nombre:
        messagebox.showerror("Error", "El nombre es obligatorio")
        return
    
    if not validar_labels(apellido):
        messagebox.showerror("Error", "El apellido solo debe llevar letras A-Z a-z")
        return

    if not apellido:
        messagebox.showerror("Error", "El apellido es obligatorio")
        return

    if not validar_celular(celular):
        messagebox.showerror("Error", " Celular: Solo puede ingresar números")
        return

    conn = conectar_bd()
    c = conn.cursor()
    c.execute("INSERT INTO Clientes (nombre, apellido, celular, direccion) VALUES (?, ?, ?, ?)",
            (nombre,apellido,celular,direccion))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Cliente dado de alta correctamente")
    top_cliente.destroy()
    actualizar_lista_clientes(lista_clientes)

# Funcion editar cliente
def editar_cliente(lista_clientes):
    # Abrimos la nueva ventana
    top_editar = tk.Toplevel()
    top_editar.title("Editar cliente")
    top_editar.geometry("300x400")

    # Creamos el frame
    frame_editar = ttk.LabelFrame(top_editar, text="Editar cliente")
    frame_editar.pack(padx=10, pady=10, fill="both", expand=True)

    # Creamos labels y entrys de la nueva ventana
    label_nombre = ttk.Label(frame_editar, text="Nombre")
    entry_nombre = ttk.Entry(frame_editar)
    label_apellido = ttk.Label(frame_editar, text="Apellido")
    entry_apellido = ttk.Entry(frame_editar)
    label_celular = ttk.Label(frame_editar, text="Celular")
    entry_celular = ttk.Entry(frame_editar)
    label_direccion = ttk.Label(frame_editar, text="Direccion")
    entry_direccion = ttk.Entry(frame_editar)

    seleccionado = lista_clientes.selection()
    id_cliente, nombre, apellido, celular, direccion = lista_clientes.item(seleccionado, "values")

    if not seleccionado:
        messagebox.showerror("Error","Selecciona un cliente para editar")
        return

    # Funcion para guardar cambios en BD
    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nuevo_apellido = entry_apellido.get()
        nuevo_celular = entry_celular.get()
        nuevo_direccion = entry_direccion.get()
        
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("UPDATE Clientes SET nombre=?, apellido=?, celular=?, direccion=? WHERE id_cliente=?", 
                (nuevo_nombre, nuevo_apellido, nuevo_celular, nuevo_direccion, id_cliente))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        top_editar.destroy()
        actualizar_lista_clientes(lista_clientes)
    
    # Creamos boton para guardar los datos editados
    btn_guardar_cambios = ttk.Button(frame_editar, text="Guardar Cambios", command=guardar_cambios)

    # Agregamos a la ventana
    label_nombre.pack()
    entry_nombre.insert(0, nombre)
    entry_nombre.pack()

    label_apellido.pack()
    entry_apellido.insert(0, apellido)
    entry_apellido.pack()

    label_celular.pack()
    entry_celular.insert(0, celular)
    entry_celular.pack()

    label_direccion.pack()
    entry_direccion.insert(0, direccion)
    entry_direccion.pack()

    btn_guardar_cambios.pack()

# Funcion eliminar cliente
def eliminar_cliente(lista_clientes):

    select = lista_clientes.selection()

    if not select :
        messagebox.showerror("Error","Selecciona un cliente para eliminar")
        return
    
    item = lista_clientes.item(select)
    id_cliente = item["values"][0]
    nombre_cliente = item["values"][1]
    apellido_cliente = item["values"][2]

    respuesta = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al cliente {nombre_cliente} {apellido_cliente} ?")

    if respuesta:
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("DELETE FROM Clientes WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito","Cliente eliminado correctamente")
        actualizar_lista_clientes(lista_clientes)

# Funcion agregar cliente
def ventana_nuevo_cliente(lista_clientes):
    top_cliente = tk.Toplevel()
    top_cliente.title("Alta cliente")
    top_cliente.geometry("600x400")

    frame_clientes = ttk.LabelFrame(top_cliente, text="Alta cliente")
    frame_clientes.pack(padx=10, pady=10, fill="both", expand=True)

    label_nombre = ttk.Label(frame_clientes, text="Nombre:")
    entry_nombre = ttk.Entry(frame_clientes)
    label_apellido = ttk.Label(frame_clientes, text="Apellido:")
    entry_apellido = ttk.Entry(frame_clientes)
    label_celular = ttk.Label(frame_clientes, text="Celular:")
    entry_celular = ttk.Entry(frame_clientes)
    label_direccion = ttk.Label(frame_clientes, text="Direccion:")
    entry_direccion = ttk.Entry(frame_clientes)

    btn_alta_cliente = ttk.Button(frame_clientes, text="Aceptar", 
                                command=lambda: alta_cliente(entry_nombre, entry_apellido, entry_celular, entry_direccion, lista_clientes, top_cliente))

    label_nombre.pack()
    entry_nombre.pack()
    label_apellido.pack()
    entry_apellido.pack()
    label_celular.pack()
    entry_celular.pack()
    label_direccion.pack()
    entry_direccion.pack()
    btn_alta_cliente.pack()

# Lista clientes
def actualizar_lista_clientes(lista_clientes):
    lista_clientes.delete(*lista_clientes.get_children())
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT * FROM Clientes")
    for fila in c.fetchall():
        fila_mayus = tuple(str(valor).upper() for valor in fila)
        lista_clientes.insert("", tk.END, values=fila_mayus)
    conn.close()

def centrar_ventana(root, ancho, alto):

    # Obtenemos las dimensiones de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    # Calculamos las coordenadas x e y para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    # Establecemos la geometría de la ventana
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

# Ventana clientes
def ventana_clientes(ventana_principal):
    top = tk.Toplevel()
    top.title("Gestion de Clientes")
    ancho = 1600
    alto = 900
    centrar_ventana(top, ancho, alto)

    top.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(top, ventana_principal))

    frame_clientes = ttk.LabelFrame(top, text="Gestion de Clientes")
    frame_clientes.pack(padx=10, pady=10, fill="both", expand=True)


    # Traemos las imagenes para usarlas
    try:
        icono_agregar = ImageTk.PhotoImage(Image.open("./assets/icons/agregar_p.png").resize((20, 20)))
        icono_editar = ImageTk.PhotoImage(Image.open("./assets/icons/editar_p.png").resize((20, 20)))
        icono_eliminar = ImageTk.PhotoImage(Image.open("./assets/icons/delete_p.png").resize((20, 20)))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron los archivos de iconos.")
        return

    # Traemos los estilos para los botones
    styles.configurar_estilos()

    frame_botones = ttk.Frame(frame_clientes)
    frame_botones.pack(pady=10)

    btn_agregar_cliente = ttk.Button(frame_botones, text="Nuevo Cliente", image=icono_agregar,compound=tk.LEFT,style="Boton.TButton", 
                                    command=lambda: ventana_nuevo_cliente(lista_clientes))
    btn_editar_cliente = ttk.Button(frame_botones, text="Editar Cliente",image=icono_editar,compound=tk.LEFT,style="Boton.TButton",
                                    command=lambda: editar_cliente(lista_clientes))
    btn_eliminar_cliente = ttk.Button(frame_botones,text="Eliminar Cliente",image=icono_eliminar,compound=tk.LEFT,style="Boton.TButton",
                                    command=lambda: eliminar_cliente(lista_clientes))

    btn_agregar_cliente.pack(side=tk.LEFT, padx=5)
    btn_editar_cliente.pack(side=tk.LEFT, padx=5)
    btn_eliminar_cliente.pack(side=tk.LEFT, padx=5)

    lista_clientes = ttk.Treeview(frame_clientes, columns=("ID","Nombre","Apellido","Celular","Dirección"), show="headings")

    for col in ("ID","Nombre","Apellido","Celular","Dirección"):
        lista_clientes.heading(col, text=col, anchor="center")

    lista_clientes.column("ID", width=80, anchor="center")
    lista_clientes.column("Nombre", width=200, anchor="center")
    lista_clientes.column("Apellido", width=200, anchor="center")
    lista_clientes.column("Celular", width=200, anchor="center")
    lista_clientes.column("Dirección", width=200, anchor="center")
        
    lista_clientes.pack(fill="both", expand=True)


    actualizar_lista_clientes(lista_clientes)

    top.icono_agregar = icono_agregar
    top.icono_editar = icono_editar
    top.icono_eliminar = icono_eliminar

# Función para cerrar la ventana de proveedores y mostrar la ventana principal
def cerrar_ventana(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()  # Cierra la ventana secundaria
    ventana_principal.deiconify()  # Muestra la ventana principal