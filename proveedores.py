import tkinter as tk
import styles
from tkinter import ttk, messagebox
from database import conectar_bd

# Funcion agregar proveedores
def agregar_proveedor(entry_nombre, entry_telefono, entry_direccion, lista_proveedores):
    nombre = entry_nombre.get()
    celular = entry_telefono.get()
    direccion = entry_direccion.get()
    
    if not nombre:
        messagebox.showerror("Error", "El nombre es obligatorio")
        return
    
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("INSERT INTO Proveedores (nombre, direccion, celular) VALUES (?, ?, ?)",
            (nombre, direccion, celular))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    actualizar_lista_proveedores(lista_proveedores)

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
        c.execute("UPDATE Proveedores SET nombre=?, celular=?, direccion=? WHERE id_proveedor=?", 
                (nuevo_nombre, nuevo_telefono, nuevo_direccion, id_proveedor))
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
        messagebox.showerror("Error", "Selecciona un proveedor para eliminar")
        return
    
    item = lista_proveedores.item(seleccionado)
    id_proveedor = item["values"][0]

    respuesta = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al proveedor ID {id_proveedor}?")
    
    if respuesta:
        conn = conectar_bd()
        c = conn.cursor()
        c.execute("DELETE FROM Proveedores WHERE id_proveedor = ?", (id_proveedor,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
        actualizar_lista_proveedores(lista_proveedores)

# Función para actualizar la lista de proveedores
def actualizar_lista_proveedores(lista_proveedores):
    lista_proveedores.delete(*lista_proveedores.get_children())
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT * FROM Proveedores")
    for fila in c.fetchall():
        lista_proveedores.insert("", tk.END, values=fila)
    conn.close()

# Funcion para ver la ventana de edicion, nuevos y eliminar proveedores
def ventana_proveedores():
    top = tk.Toplevel()
    top.title("Gestión de Proveedores")
    top.geometry("600x400")
    
    frame_proveedores = ttk.LabelFrame(top, text="Gestión de Proveedores")
    frame_proveedores.pack(padx=10, pady=10, fill="both", expand=True)
    
    label_nombre = ttk.Label(frame_proveedores, text="Nombre:")
    entry_nombre = ttk.Entry(frame_proveedores)
    label_telefono = ttk.Label(frame_proveedores, text="Celular:")
    entry_telefono = ttk.Entry(frame_proveedores)
    label_direccion = ttk.Label(frame_proveedores, text="Dirección:")
    entry_direccion = ttk.Entry(frame_proveedores)
    
    btn_agregar = ttk.Button(frame_proveedores, style="Boton.TButton",compound=tk.LEFT, text="Agregar Proveedor", 
                            command=lambda: agregar_proveedor(entry_nombre, entry_telefono, entry_direccion, lista_proveedores))
    
    lista_proveedores = ttk.Treeview(frame_proveedores, columns=("ID", "Nombre", "Dirección", "Celular"), show="headings")
    for col in ("ID", "Nombre", "Dirección", "Celular"):
        lista_proveedores.heading(col, text=col)
    
    label_nombre.pack()
    entry_nombre.pack()
    label_telefono.pack()
    entry_telefono.pack()
    label_direccion.pack()
    entry_direccion.pack()
    btn_agregar.pack()

    btn_editar = ttk.Button(frame_proveedores,style="Boton.TButton", text="Editar Proveedor",compound=tk.LEFT, command=lambda: editar_proveedor(lista_proveedores))
    btn_editar.pack()
    btn_eliminar = ttk.Button(frame_proveedores,style="Boton.TButton", text="Eliminar Proveedor",compound=tk.LEFT, command=lambda: eliminar_proveedor(lista_proveedores))
    btn_eliminar.pack()

    btn_agregar.pack(side=tk.LEFT, padx=5)
    btn_editar.pack(side=tk.LEFT, padx=5)
    btn_eliminar.pack(side=tk.LEFT, padx=5)

    lista_proveedores.pack(fill="both", expand=True)


    
    actualizar_lista_proveedores(lista_proveedores)