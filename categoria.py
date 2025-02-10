import tkinter as tk;
import re;
import styles;
from tkinter import ttk, messagebox;
from PIL import Image, ImageTk;
from database import conectar_bd;

def nueva_categoria():
    top_categoria = tk.Toplevel()
    top_categoria.title("Alta categoria")
    top_categoria.geometry("600x400")

    frame_productos = ttk.LabelFrame(top_categoria, text="Alta categoria")
    frame_productos.pack(padx=10,pady=10,fill="both", expand=True)

    label_nombre = ttk.Label(frame_productos, text="Nombre categoria")
    entry_nombre = ttk.Entry(frame_productos)
    label_descripcion = ttk.Label(frame_productos, text="Descripcion")
    entry_descripcion = ttk.Entry(frame_productos)

    def alta_categoria(entry_nombre, entry_descripcion):
        nombre = entry_nombre.get()
        descripcion = entry_descripcion.get()
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("INSERT INTO Categoria (nombre, descripcion) VALUES (?, ?)",
                (nombre, descripcion))
        conn.commit()
        messagebox.showinfo("Exito","Cateogria dada de alta correctamente")
        top_categoria.destroy()
        conn.close()

    btn_alta_categoria = ttk.Button(frame_productos, text="Aceptar",
                                    command=lambda: alta_categoria(entry_nombre, entry_descripcion))
    
    label_nombre.pack()
    entry_nombre.pack()
    label_descripcion.pack()
    entry_descripcion.pack()
    btn_alta_categoria.pack()

# Funcion Editar categoria
def editar_categoria(lista_categorias):
    top_editar = tk.Toplevel()
    top_editar.title("Editar Categoria")
    top_editar.geometry("300x200")

    seleccionada = lista_categorias.selection()
    if not seleccionada:
        messagebox.showerror("Error","Selecciona una categoria para editar")
        return
    
    item = lista_categorias.item(seleccionada)
    id_categoria, nombre, descripcion = item["values"]

    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_descripcion = entry_descripcion.get()
        
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("UPDATE Categoria SET nombre=?, descripcion=? WHERE id_categoria=?", 
                (nuevo_nombre, nueva_descripcion, id_categoria))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Categoria actualizada correctamente")
        top_editar.destroy()
        actualizar_lista_categorias(lista_categorias)

    tk.Label(top_editar, text="Nombre:").pack()
    entry_nombre = tk.Entry(top_editar)
    entry_nombre.insert(0, nombre)
    entry_nombre.pack()

    tk.Label(top_editar, text="Descripcion").pack()
    entry_descripcion = tk.Entry(top_editar)
    entry_descripcion.insert(0, descripcion)
    entry_descripcion.pack()

    tk.Button(top_editar, text="Guardar Cambios", command=guardar_cambios).pack()

# Eliminar categoria
def eliminar_categoria(lista_categorias):
    seleccionada = lista_categorias.selection()
    if not seleccionada:
        messagebox.showerror("Error","Selecciona una categoria para eliminar")
        return
    
    item = lista_categorias.item(seleccionada)
    id_categoria = item["values"][0]
    nombre = item["values"][1]

    top_eliminar = tk.Toplevel()
    top_eliminar.withdraw()
    
    respuesta = messagebox.askyesno("Confirmar",f"¿Seguro desea eliminar la categoria {id_categoria}-{nombre}")
    top_eliminar.destroy()

    if respuesta:
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("DELETE FROM Categoria WHERE id_categoria = ?", (id_categoria,))
        conn.commit()
        conn.close()
        
        top = tk.Toplevel()
        top.withdraw()  # Ocultar la ventana temporal
        messagebox.showinfo("Éxito", "Categoria eliminada correctamente", parent=top)
        top.destroy()  # Cerrar la ventana temporal
        actualizar_lista_categorias(lista_categorias)

# Funcion para actualizar lista de categorias
def actualizar_lista_categorias(lista_categorias):
    lista_categorias.delete(*lista_categorias.get_children())
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT * FROM Categoria")
    for fila in c.fetchall():
        fila_mayus = tuple(str(valor).upper() for valor in fila)
        lista_categorias.insert("", tk.END, values=fila_mayus)
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

def ventana_categoria(ventana_principal):
    top = tk.Toplevel()
    top.title("Gestion de Productos")
    ancho = 1600
    alto = 900
    centrar_ventana(top, ancho, alto)

    frame_categoria = ttk.LabelFrame(top, text="Gestion de Categoria")
    frame_categoria.pack(padx=10, pady=10, fill="both", expand=True)

    top.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(top, ventana_principal))

    # Traemos las imagenes para usarlas
    try:
        icono_agregar = ImageTk.PhotoImage(Image.open("./assets/icons/agregar_categoria.png").resize((20,20)))
        icono_editar = ImageTk.PhotoImage(Image.open("./assets/icons/editar_categoria.png").resize((20,20)))
        icono_eliminar =ImageTk.PhotoImage(Image.open("./assets/icons/eliminar_categoria.png").resize((20,20)))
    except FileNotFoundError:
        messagebox.showerror("Error","No se encontraron los archivos de iconos")
        return
    

    # Treaemos los estilos para los botones
    styles.configurar_estilos()

    frame_botones = ttk.Frame(frame_categoria)
    frame_botones.pack(pady=10)

    btn_agregar_categoria = ttk.Button(frame_botones, text="Nueva Categoria", style="Boton.TButton", image=icono_agregar, compound=tk.LEFT,
                                    command=lambda: nueva_categoria())
    btn_editar_categoria = ttk.Button(frame_botones, text="Editar Categoria", style="Boton.TButton", image=icono_editar, compound=tk.LEFT,
                                    command=lambda: editar_categoria(lista_categorias))
    btn_eliminar_categoria = ttk.Button(frame_botones, text="Eliminar Categoria", style="Boton.TButton", image=icono_eliminar, compound=tk.LEFT,
                                    command=lambda: eliminar_categoria(lista_categorias))
    
    btn_agregar_categoria.pack(side=tk.LEFT, padx=5)
    btn_editar_categoria.pack(side=tk.LEFT, padx=5)
    btn_eliminar_categoria.pack(side=tk.LEFT, padx=5)
    
    lista_categorias = ttk.Treeview(frame_categoria, columns=("ID", "Nombre Categoria", "Descripcion"), show="headings")
    for col in ("ID","Nombre Categoria", "Descripcion"):
        lista_categorias.heading(col, text=col, anchor="center")

    lista_categorias.column("ID", width=80, anchor="center")
    lista_categorias.column("Nombre Categoria", width=200, anchor="center")
    lista_categorias.column("Descripcion", width=200, anchor="center")

    lista_categorias.pack(fill="both", expand=True)

    actualizar_lista_categorias(lista_categorias)

    top.icono_agregar = icono_agregar
    top.icono_editar = icono_editar
    top.icono_eliminar = icono_eliminar

# Función para cerrar la ventana de proveedores y mostrar la ventana principal
def cerrar_ventana(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()  # Cierra la ventana secundaria
    ventana_principal.deiconify()  # Muestra la ventana principal