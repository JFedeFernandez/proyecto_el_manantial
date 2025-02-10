
import tkinter as tk;
import styles;
from tkinter import ttk, messagebox;
from PIL import Image, ImageTk;
from proveedores import ventana_proveedores;
from clientes import ventana_clientes;
from productos import ventana_productos;
from categoria import ventana_categoria;

def centrar_ventana(root, ancho, alto):

    # Obtenemos las dimensiones de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    # Calculamos las coordenadas x e y para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    # Establecemos la geometría de la ventana
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

def app():
    root = tk.Tk()
    root.title("Sistema de Gestión")
    ancho_ventana = 400
    alto_ventana = 400
    centrar_ventana(root, ancho_ventana, alto_ventana)
    
    styles.configurar_estilos()

    try:
        icono_clientes = ImageTk.PhotoImage(Image.open("./assets/icons/clientes.png").resize((20,20)))
        icono_proveedores = ImageTk.PhotoImage(Image.open("./assets/icons/proveedores.png").resize((20,20)))
        icono_productos = ImageTk.PhotoImage(Image.open("./assets/icons/productos.png").resize((20,20)))
        icono_categorias = ImageTk.PhotoImage(Image.open("./assets/icons/categoria.png").resize((20,20)))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron los archivos de iconos.")
        return

    def abrir_ventana_proveedores():
        root.withdraw()
        ventana_proveedores(root)

    def abrir_ventana_clientes():
        root.withdraw()
        ventana_clientes(root)

    def abrir_ventana_productos():
        root.withdraw()
        ventana_productos(root)

    def abrir_ventana_categoria():
        root.withdraw()
        ventana_categoria(root)

    btn_proveedores = ttk.Button(root, text="Gestionar Proveedores",style="Boton.TButton",image=icono_proveedores,compound=tk.LEFT,
                            command=abrir_ventana_proveedores)
    btn_proveedores.pack(pady=20)

    btn_clientes = ttk.Button(root, text="Gestionar Clientes",style="Boton.TButton",image=icono_clientes,compound=tk.LEFT,
                            command=abrir_ventana_clientes)
    btn_clientes.pack(pady=20)

    btn_productos = ttk.Button(root, text="Gestionar Productos",style="Boton.TButton",image=icono_productos,compound=tk.LEFT,
                            command=abrir_ventana_productos)
    btn_productos.pack(pady=20)

    btn_categoria = ttk.Button(root, text="Gestionar Categoria",style="Boton.TButton",image=icono_categorias,compound=tk.LEFT,
                            command=abrir_ventana_categoria)
    btn_categoria.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    app()