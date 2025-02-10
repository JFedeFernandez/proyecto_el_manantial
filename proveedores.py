import tkinter as tk
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

# Funcion agregar proveedores
def agregar_proveedor(lista_proveedores):
    top_proveedor = tk.Toplevel()
    top_proveedor.title("Alta proveedor")
    top_proveedor.geometry("600x400")

    frame_proveedores = ttk.LabelFrame(top_proveedor, text="Alta proveedor")
    frame_proveedores.pack(padx=10,pady=10,fill="both", expand=True)

    def alta_proveedor(entry_nombre, entry_direccion, entry_celular):
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        celular = entry_celular.get()
        
        # Control de errores
        if not validar_labels(nombre):
            messagebox.showerror("Error", "El nombre solo debe llevar letras A-Z a-z")
            return
        
        if not nombre :
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if not validar_celular(celular):
            messagebox.showerror("Error", " Celular: Solo puede ingresar números")
            return
        
        if not celular:
            messagebox.showerror("Error", "Debe ingresar un numero de celular")
            return
    
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("INSERT INTO Proveedores (nombre, direccion, celular) VALUES (?, ?, ?)",
                (nombre,direccion, celular))
        conn.commit()
        messagebox.showinfo("Exito","Proveedor dado de alta correctamente")
        actualizar_lista_proveedores(lista_proveedores)
        top_proveedor.destroy()
        conn.close()
    
    label_nombre = ttk.Label(frame_proveedores, text="Nombre")
    entry_nombre = ttk.Entry(frame_proveedores)
    label_direccion = ttk.Label(frame_proveedores, text="Direccion")
    entry_direccion = ttk.Entry(frame_proveedores)
    label_celular = ttk.Label(frame_proveedores, text="Celular")
    entry_celular = ttk.Entry(frame_proveedores)

    btn_alta_proveedor = ttk.Button(frame_proveedores, text="Aceptar",
                                    command=lambda: alta_proveedor(entry_nombre, entry_direccion, entry_celular))

    label_nombre.pack()
    entry_nombre.pack()
    label_celular.pack()
    entry_celular.pack()
    label_direccion.pack()
    entry_direccion.pack()
    btn_alta_proveedor.pack()

# Funcion para editar proveedores
def editar_proveedor(lista_proveedores):
    seleccionado = lista_proveedores.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Selecciona un proveedor para editar")
        return
    
    item = lista_proveedores.item(seleccionado)
    id_proveedor, nombre, telefono, direccion = item["values"]

    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nuevo_telefono = entry_telefono.get()
        nuevo_direccion = entry_direccion.get()
        
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("UPDATE Proveedores SET nombre=?, direccion=?, celular=? WHERE id_proveedor=?", 
                (nuevo_nombre, nuevo_direccion, nuevo_telefono, id_proveedor))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
        top_editar.destroy()
        actualizar_lista_proveedores(lista_proveedores)
    
    top_editar = tk.Toplevel()
    top_editar.title("Editar Proveedor")
    top_editar.geometry("300x250")

    tk.Label(top_editar, text="Nombre:").pack()
    entry_nombre = tk.Entry(top_editar)
    entry_nombre.insert(0, nombre)
    entry_nombre.pack()
    
    tk.Label(top_editar, text="Celular:").pack()
    entry_telefono = tk.Entry(top_editar)
    entry_telefono.insert(0, telefono)
    entry_telefono.pack()
    
    tk.Label(top_editar, text="Dirección:").pack()
    entry_direccion = tk.Entry(top_editar)
    entry_direccion.insert(0, direccion)
    entry_direccion.pack()
    
    tk.Button(top_editar, text="Guardar Cambios", command=guardar_cambios).pack()

# Funcion para eliminar proveedor
def eliminar_proveedor(lista_proveedores):
    seleccionado = lista_proveedores.selection()
    if not seleccionado:
        # Asegurar que el messagebox esté en primer plano
        top = tk.Toplevel()
        top.withdraw()  # Ocultar la ventana temporal
        messagebox.showerror("Error", "Selecciona un proveedor para eliminar", parent=top)
        top.destroy()  # Cerrar la ventana temporal
        return
    
    item = lista_proveedores.item(seleccionado)
    id_proveedor = item["values"][0]

    top = tk.Toplevel()
    top.withdraw()  # Ocultar la ventana temporal
    respuesta = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al proveedor ID {id_proveedor}?",parent=top)
    top.destroy()
    
    if respuesta:
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("DELETE FROM Proveedores WHERE id_proveedor = ?", (id_proveedor,))
        conn.commit()
        conn.close()
        
        top = tk.Toplevel()
        top.withdraw()  # Ocultar la ventana temporal
        messagebox.showinfo("Éxito", "Proveedor eliminado correctamente", parent=top)
        top.destroy()  # Cerrar la ventana temporal
        actualizar_lista_proveedores(lista_proveedores)

# Función para actualizar la lista de proveedores
def actualizar_lista_proveedores(lista_proveedores):
    lista_proveedores.delete(*lista_proveedores.get_children())
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT * FROM Proveedores")
    for fila in c.fetchall():
        fila_mayus = tuple(str(valor).upper() for valor in fila)
        lista_proveedores.insert("", tk.END, values=fila_mayus)
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

# Funcion para ver la ventana de edicion, nuevos y eliminar proveedores
def ventana_proveedores(ventana_principal):
    top = tk.Toplevel()
    top.title("Gestión de Proveedores")
    ancho = 1600
    alto = 900
    centrar_ventana(top, ancho, alto)

    # Cuando se cierra la ventana de proveedores, mostrar la ventana principal
    top.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(top, ventana_principal))
    
    frame_proveedores = ttk.LabelFrame(top, text="Gestión de Proveedores")
    frame_proveedores.pack(padx=10, pady=10, fill="both", expand=True)
    
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

    frame_botones = ttk.Frame(frame_proveedores)
    frame_botones.pack(pady=10)

    btn_agregar_proveedor = ttk.Button(frame_botones, text="Nuevo Proveedor", image=icono_agregar, style="Boton.TButton",compound=tk.LEFT, 
                            command=lambda: agregar_proveedor(lista_proveedores))
    btn_editar_proveedor = ttk.Button(frame_botones,style="Boton.TButton", text="Editar Proveedor", image=icono_editar,compound=tk.LEFT,
                            command=lambda: editar_proveedor(lista_proveedores))
    btn_eliminar_proveedor = ttk.Button(frame_botones,style="Boton.TButton", text="Eliminar Proveedor", image=icono_eliminar,compound=tk.LEFT,
                            command=lambda: eliminar_proveedor(lista_proveedores))
    
    btn_agregar_proveedor.pack(side=tk.LEFT, padx=5)
    btn_editar_proveedor.pack(side=tk.LEFT, padx=5)
    btn_eliminar_proveedor.pack(side=tk.LEFT, padx=5)

    lista_proveedores = ttk.Treeview(frame_proveedores, columns=("ID", "Nombre", "Dirección", "Celular"), show="headings")
    for col in ("ID", "Nombre", "Dirección", "Celular"):
        lista_proveedores.heading(col, text=col, anchor="center")


    lista_proveedores.column("ID",width=80, anchor="center")
    lista_proveedores.column("Nombre",width=200, anchor="center")
    lista_proveedores.column("Dirección",width=200, anchor="center")
    lista_proveedores.column("Celular",width=200, anchor="center")



    lista_proveedores.pack(fill="both", expand=True)


    
    actualizar_lista_proveedores(lista_proveedores)

    top.icono_agregar = icono_agregar
    top.icono_editar = icono_editar
    top.icono_eliminar = icono_eliminar

# Función para cerrar la ventana de proveedores y mostrar la ventana principal
def cerrar_ventana(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()  # Cierra la ventana secundaria
    ventana_principal.deiconify()  # Muestra la ventana principal