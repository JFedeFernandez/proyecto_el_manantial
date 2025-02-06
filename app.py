
import tkinter as tk;
import styles;
from tkinter import ttk, messagebox;
from PIL import Image, ImageTk;
from proveedores import ventana_proveedores;
from clientes import ventana_clientes;

def app():
    root = tk.Tk()
    root.title("Sistema de Gestión")
    root.geometry("400x400")
    
    styles.configurar_estilos()

    try:
        icono_clientes = ImageTk.PhotoImage(Image.open("./assets/icons/clientes.png").resize((20, 20)))
        icono_proveedores = ImageTk.PhotoImage(Image.open("./assets/icons/proveedores.png").resize((20, 20)))
        icono_productos = ImageTk.PhotoImage(Image.open("./assets/icons/productos.png").resize((20,20)))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron los archivos de iconos.")
        return

    def abrir_ventana_proveedores():
        root.withdraw()
        ventana_proveedores(root)

    def abrir_ventana_clientes():
        root.withdraw()
        ventana_clientes(root)

    btn_proveedores = ttk.Button(root, text="Gestionar Proveedores",style="Boton.TButton",image=icono_proveedores,compound=tk.LEFT, command=abrir_ventana_proveedores)
    btn_proveedores.pack(pady=20)

    btn_clientes = ttk.Button(root, text="Gestionar Clientes",style="Boton.TButton",image=icono_clientes,compound=tk.LEFT, command=abrir_ventana_clientes)
    btn_clientes.pack(pady=20)

    btn_productos = ttk.Button(root, text="Gestionar Productos",style="Boton.TButton",image=icono_productos,compound=tk.LEFT)
    btn_productos.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    app()