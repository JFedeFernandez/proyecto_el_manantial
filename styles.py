from tkinter import ttk

def configurar_estilos():
    
    estilo = ttk.Style()

    estilo.configure("Boton.TButton", foreground="black", font=("Arial",10, "bold"), padding=10, width=20,)