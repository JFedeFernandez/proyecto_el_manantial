import tkinter as tk;
import re;
import styles;
from tkinter import ttk, messagebox;
from PIL import Image, ImageTk;
from database import conectar_bd;

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

# Funcion nuevo producto
def nuevo_producto(lista_productos):
    top_producto = tk.Toplevel()
    top_producto.title("Alta producto")
    top_producto.geometry("600x400")

    frame_productos = ttk.LabelFrame(top_producto, text="Alta proveedor")
    frame_productos.pack(padx=10,pady=10,fill="both", expand=True)

    # Creamos labels y entrys
    label_marca = ttk.Label(frame_productos, text="Marca del Producto")
    entry_marca = ttk.Entry(frame_productos)
    label_descripcion = ttk.Label(frame_productos, text="Descripcion")
    entry_descripcion = ttk.Entry(frame_productos)
    label_precio_venta = ttk.Label(frame_productos, text="Precio de Venta")
    entry_precio_venta = ttk.Entry(frame_productos)
    label_precio_compra = ttk.Label(frame_productos, text="Precio de Compra")
    entry_precio_compra = ttk.Entry(frame_productos)
    label_stock = ttk.Label(frame_productos, text="Cantidad a comprar")
    entry_stock = ttk.Entry(frame_productos)
    label_descuento = ttk.Label(frame_productos, text="Descuento %")
    entry_descuento = ttk.Entry(frame_productos)

    label_proveedor = ttk.Label(frame_productos, text="Proveedor")
    combo_proveedor = ttk.Combobox(frame_productos)

    label_categoria = ttk.Label(frame_productos, text="Categoria")
    combo_categoria = ttk.Combobox(frame_productos)


    # Obtener los IDs y nombres de las categorias desde la base de datos
    def obtener_categorias():
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("SELECT id_categoria, nombre FROM Categoria")
        categorias = c.fetchall()
        conn.close()

        #Formatear los datos como "ID - Nombre"
        return [f"{categoria[0]} - {categoria[1]}" for categoria in categorias]

    # Obtener los IDs y nombres de los proveedores desde la base de datos
    def obtener_proveedores():
        conn = conectar_bd()  # Cambia 'tu_base_de_datos.db' por el nombre de tu base de datos
        c = conn.cursor()
        c.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedores = c.fetchall()
        conn.close()

        # Formatear los datos como "ID - Nombre"
        return [f"{proveedor[0]} - {proveedor[1]}" for proveedor in proveedores]

    # Insertar los nombres de los proveedores en el Combobox
    combo_proveedor['values'] = obtener_proveedores()
    combo_categoria['values'] = obtener_categorias()

    # Alta del producto
    def alta_producto(entry_marca,entry_descripcion,entry_precio_compra,entry_precio_venta,entry_stock,entry_descuento,entry_proveedor,entry_categoria):

        marca = entry_marca.get()
        descripcion = entry_descripcion.get()
        precio_compra = float(entry_precio_compra.get())
        precio_venta = float(entry_precio_venta.get())
        stock = int(entry_stock.get())
        descuento = int(entry_descuento.get())
        proveedor_seleccionado = entry_proveedor.get()
        id_proveedor = proveedor_seleccionado.split(" - ")[0]
        categoria_seleccionada = entry_categoria.get()
        id_categoria = categoria_seleccionada.split(" - ")[0]

        if not validar_labels(marca):
            messagebox.showerror("Error","Nombre incorrecto: solo puede ingresar letras A-Z a-z")
            return
        
        if not marca:
            messagebox.showerror("Error","Nombre obligatorio")
            return
        
        
        if not precio_compra:
            messagebox.showerror("Error","Precio de compra obligatorio")
            return
        
        
        if not precio_venta:
            messagebox.showerror("Error","Precio de venta obligatorio")
            return
        
        if not stock > 0:
            messagebox.showerror("Error","Cantidad: Debe ingresar un numero mayor a 0")
            return
        
        if not stock:
            messagebox.showerror("Error","Cantidad obligatoria")
            return
        
        if not (descuento > 0 and descuento <= 100):
            messagebox.showerror("Error","Descuento: Debe ingresar un numero entre 0 y 100")
            return
        
        if not descuento:
            messagebox.showerror("Error","Descuento obligatorio")
            return
        
        if not id_proveedor: 
            messagebox.showerror("Error","Proveedor: debe seleccionar un proveedor")
            return
        
        if not id_categoria:
            messagebox.showerror("Error","Categoria: debe seleccionar un proveedor")
            return
        
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("INSERT INTO Productos (id_proveedor, id_categoria, marca, descripcion, precio_venta, precio_compra, stock, descuento) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (id_proveedor, id_categoria, marca, descripcion, precio_venta, precio_compra, stock, descuento))
        conn.commit()
        messagebox.showinfo("Exito","Proveedor dado de alta correctamente")
        actualizar_lista_productos(lista_productos)
        top_producto.destroy()
        conn.close()

    btn_alta_producto = ttk.Button(frame_productos, text="Aceptar",
                                    command=lambda: alta_producto(entry_marca,entry_descripcion,entry_precio_compra,entry_precio_venta,entry_stock,entry_descuento,combo_proveedor,combo_categoria))
    
    label_marca.pack()
    entry_marca.pack()
    label_descripcion.pack()
    entry_descripcion.pack()
    label_precio_compra.pack()
    entry_precio_compra.pack()
    label_precio_venta.pack()
    entry_precio_venta.pack()
    label_stock.pack()
    entry_stock.pack()
    label_descuento.pack()
    entry_descuento.pack()
    label_proveedor.pack()
    combo_proveedor.pack()
    label_categoria.pack()
    combo_categoria.pack()

    btn_alta_producto.pack()

# Funcion editar producto
def editar_producto(lista_productos):
    seleccionado = lista_productos.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Selecciona un proveedor para editar")
        return
    
    item = lista_productos.item(seleccionado)
    id_producto, proveedor, categoria, marca, descripcion, precio_venta, precio_compra, stock, descuento = item["values"]

    # Obtener los IDs y nombres de los proveedores desde la base de datos
    def obtener_proveedores():
        conn = conectar_bd()  # Cambia 'tu_base_de_datos.db' por el nombre de tu base de datos
        c = conn.cursor()
        c.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedores = c.fetchall()
        conn.close()

        # Formatear los datos como "ID - Nombre"
        return [f"{proveedor[0]} - {proveedor[1].upper()}" for proveedor in proveedores]


    # Obtener los IDs y nombres de los proveedores desde la base de datos
    def obtener_categorias():
        conn = conectar_bd()  # Cambia 'tu_base_de_datos.db' por el nombre de tu base de datos
        c = conn.cursor()
        c.execute("SELECT id_categoria, nombre FROM Categoria")
        categorias = c.fetchall()
        conn.close()

        # Formatear los datos como "ID - Nombre"
        return [f"{categoria[0]} - {categoria[1].upper()}" for categoria in categorias]
    
    # Funcion guardar cambios 
    def guardar_cambios():
        marca = entry_marca.get()
        descripcion = entry_descripcion.get()
        precio_venta = entry_precio_venta.get()
        precio_compra = entry_precio_compra.get()
        stock = entry_stock.get()
        descuento = entry_descuento.get()
        proveedor_seleccionado = combo_proveedores.get()
        id_proveedor = proveedor_seleccionado.split(" - ")[0]
        categoria_seleccionada = combo_categorias.get()
        id_categoria = categoria_seleccionada.split(" - ")[0]

        conn = conectar_bd()
        c = conn.cursor()
        c.execute("UPDATE Productos SET id_proveedor=?, id_categoria=?, marca=?, descripcion=?, precio_venta=?, precio_compra=?, stock=?, descuento=? WHERE id_producto=?", 
                (id_proveedor, id_categoria, marca, descripcion, precio_venta, precio_compra, stock, descuento, id_producto))
        conn.commit()
        conn.close()

        messagebox.showinfo("Exito","Producto actualizado correctamente")
        top_editar.destroy()
        actualizar_lista_productos(lista_productos)
    

    # Interfaz de usuario
    top_editar = tk.Toplevel()
    top_editar.title("Editar Producto")
    top_editar.geometry("600x350")

    frame_editar = ttk.LabelFrame(top_editar, text="Editar Producto")
    frame_editar.pack(padx=10, pady=10, fill="both", expand=True)

    ttk.Label(frame_editar, text="Marca Producto")
    entry_marca = ttk.Entry(frame_editar)
    entry_marca.insert(0,marca)
    entry_marca.pack()

    ttk.Label(frame_editar, text="Descripcion")
    entry_descripcion = ttk.Entry(frame_editar)
    entry_descripcion.insert(0,descripcion)
    entry_descripcion.pack()

    ttk.Label(frame_editar, text="Precio Venta")
    entry_precio_venta = ttk.Entry(frame_editar)
    entry_precio_venta.insert(0,precio_venta)
    entry_precio_venta.pack()

    ttk.Label(frame_editar, text="Precio Compra")
    entry_precio_compra = ttk.Entry(frame_editar)
    entry_precio_compra.insert(0,precio_compra)
    entry_precio_compra.pack()

    ttk.Label(frame_editar, text="Cantidad")
    entry_stock = ttk.Entry(frame_editar)
    entry_stock.insert(0,stock)
    entry_stock.pack()

    ttk.Label(frame_editar, text="Descuento")
    entry_descuento = ttk.Entry(frame_editar)
    entry_descuento.insert(0,descuento)
    entry_descuento.pack()

    ttk.Label(frame_editar, text="Proveedores")
    combo_proveedores = ttk.Combobox(frame_editar)
    combo_proveedores['values'] = obtener_proveedores()
    combo_proveedores.set(proveedor)
    combo_proveedores.pack()

    ttk.Label(frame_editar, text="Categorias")
    combo_categorias = ttk.Combobox(frame_editar)
    combo_categorias['values'] = obtener_categorias()
    combo_categorias.set(categoria)
    combo_categorias.pack()

    ttk.Button(frame_editar, text="Guardar Cambios", command=lambda: guardar_cambios()).pack()

# Funcion para eliminar un producto de la lista 
def eliminar_producto(lista_productos):
    seleccionado = lista_productos.selection()
    if not seleccionado:
        # Asegurar que el messagebox esté en primer plano
        top = tk.Toplevel()
        top.withdraw()  # Ocultar la ventana temporal
        messagebox.showerror("Error", "Selecciona un proveedor para eliminar", parent=top)
        top.destroy()  # Cerrar la ventana temporal
        return
    
    item = lista_productos.item(seleccionado)
    id_producto = item["values"][0]
    marca = item["values"][3]
    descripcion = item["values"][4]

    top_eliminar = tk.Toplevel()
    top_eliminar.withdraw()
    respuesta = messagebox.askyesno("Confirmar",f"¿Seguro que desea eliminar el producto {id_producto} - {marca} - {descripcion}", parent=top_eliminar)
    top_eliminar.destroy()

    if respuesta :
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("DELETE FROM Productos WHERE id_producto = ?", (id_producto,))
        conn.commit()
        conn.close()

        top = tk.Toplevel()
        top.withdraw()
        messagebox.showinfo("Exito","Producto eliminado correctamente", parent=top)
        top.destroy()
        actualizar_lista_productos(lista_productos)

# Función para actualizar la lista de proveedores
def actualizar_lista_productos(lista_productos):
    lista_productos.delete(*lista_productos.get_children())
    conn = conectar_bd()
    c = conn.cursor()
    consulta = """
    SELECT p.id_producto, pr.id_proveedor || ' - ' || pr.nombre as proveedor,c.id_categoria || ' - ' || c.nombre as categoria, p.marca, p.descripcion, p.precio_venta, p.precio_compra, p.stock, p.descuento
    FROM Productos p
    JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor
    JOIN Categoria c ON p.id_categoria = c.id_categoria
    """
    c.execute(consulta)
    for fila in c.fetchall():
        fila_mayus = tuple(str(valor).upper() for valor in fila)
        lista_productos.insert("", tk.END, values=fila_mayus)
    conn.close()

def ventana_productos(ventana_principal):
    top = tk.Toplevel()
    top.title("Gestion de Productos")
    top.geometry("1266x600")

    frame_productos = ttk.LabelFrame(top, text="Gestion de Productos")
    frame_productos.pack(padx=10, pady=10, fill="both", expand=True)

    top.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(top, ventana_principal))

    # Traemos las imagenes para usarlas
    try:
        icono_agregar = ImageTk.PhotoImage(Image.open("./assets/icons/add_product.png").resize((20, 20)))
        icono_editar = ImageTk.PhotoImage(Image.open("./assets/icons/edit_product.png").resize((20, 20)))
        icono_eliminar = ImageTk.PhotoImage(Image.open("./assets/icons/delete_product.png").resize((20, 20)))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron los archivos de iconos.")
        return
    
    # Traemos los estilos para los botones
    styles.configurar_estilos()


    frame_botones = ttk.Frame(frame_productos)
    frame_botones.pack(pady=10)

    btn_agregar_producto = ttk.Button(frame_botones, text="Nuevo producto", image=icono_agregar, compound=tk.LEFT, style="Boton.TButton",
                                    command=lambda: nuevo_producto(lista_productos))
    btn_editar_producto = ttk.Button(frame_botones, text="Editar producto", image=icono_editar, compound=tk.LEFT, style="Boton.TButton",
                                    command=lambda: editar_producto(lista_productos))
    btn_eliminar_producto = ttk.Button(frame_botones, text="Eliminar producto", image=icono_eliminar, compound=tk.LEFT, style="Boton.TButton",
                                    command=lambda: eliminar_producto(lista_productos))

    btn_agregar_producto.pack(side=tk.LEFT, padx=5)
    btn_editar_producto.pack(side=tk.LEFT, padx=5)
    btn_eliminar_producto.pack(side=tk.LEFT, padx=5)

    lista_productos = ttk.Treeview(frame_productos, columns=("ID Producto", "Proveedor", "Categoria", "Marca del Producto", "Descripcion", "Precio de venta", "Precio de compra", "Stock", "Descuento"), show="headings")
    for col in ("ID Producto", "Proveedor","Categoria", "Marca del Producto", "Descripcion", "Precio de venta", "Precio de compra", "Stock", "Descuento"):
        lista_productos.heading(col, text=col, anchor="center")

    for col in ("ID Producto", "Proveedor", "Categoria", "Marca del Producto", "Descripcion", "Precio de venta", "Precio de compra", "Stock", "Descuento"):
        lista_productos.column(col, anchor="center")

    lista_productos.pack(fill="both", expand=True)

    actualizar_lista_productos(lista_productos)

    top.icono_agregar = icono_agregar
    top.icono_editar = icono_editar
    top.icono_eliminar = icono_eliminar


# Función para cerrar la ventana de proveedores y mostrar la ventana principal
def cerrar_ventana(ventana_secundaria, ventana_principal):
    ventana_secundaria.destroy()  # Cierra la ventana secundaria
    ventana_principal.deiconify()  # Muestra la ventana principal