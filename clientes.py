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

# Ventana clientes
def ventana_clientes():
    top = tk.Toplevel()
    top.title("Gestion de Clientes")
    top.geometry("1266x600")

    frame_clientes = ttk.Label(top)
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

    btn_agregar_cliente = ttk.Button(frame_botones, text="Nuevo Cliente", image=icono_agregar,compound=tk.LEFT,style="Boton.TButton", command=lambda: ventana_nuevo_cliente(lista_clientes))
    btn_editar_cliente = ttk.Button(frame_botones, text="Editar Cliente",image=icono_editar,compound=tk.LEFT,style="Boton.TButton")
    btn_eliminar_cliente = ttk.Button(frame_botones,text="Eliminar Cliente",image=icono_eliminar,compound=tk.LEFT,style="Boton.TButton")

    btn_agregar_cliente.pack(side=tk.LEFT, padx=5)
    btn_editar_cliente.pack(side=tk.LEFT, padx=5)
    btn_eliminar_cliente.pack(side=tk.LEFT, padx=5)

    lista_clientes = ttk.Treeview(frame_clientes, columns=("ID","Nombre","Apellido","Celular","Dirección"), show="headings")

    for col in ("ID","Nombre","Apellido","Celular","Dirección"):
        lista_clientes.heading(col, text=col, anchor="center")

    for col in ("ID","Nombre","Apellido","Celular","Dirección"):
        lista_clientes.column(col, anchor="center")
        
    lista_clientes.pack(fill="both", expand=True)


    actualizar_lista_clientes(lista_clientes)

    top.icono_agregar = icono_agregar
    top.icono_editar = icono_editar
    top.icono_eliminar = icono_eliminar