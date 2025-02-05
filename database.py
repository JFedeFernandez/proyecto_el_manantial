import sqlite3

def conectar_bd():
    conn = sqlite3.connect("manantial.db")
    return conn

def crear_tablas():
    conn = conectar_bd()
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS Clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT,
        celular INTEGER,
        direccion TEXT
    );
    
    CREATE TABLE IF NOT EXISTS Proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        celular INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        id_proveedor INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        precio_venta REAL NOT NULL,
        precio_compra REAL NOT NULL,
        stock INTEGER NOT NULL,
        descuento INTEGER,

        FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Compra (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_proveedor INTEGER NOT NULL,
        fecha_compra DATE NOT NULL,
        total REAL NOT NULL,
                
        FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON DELETE CASCADE
    );
                
    CREATE TABLE IF NOT EXISTS Venta (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        fecha_venta DATE NOT NULL,
        total REAL NOT NULL,
                
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
    );
                
    CREATE TABLE IF NOT EXISTS Detalle_compra(
        id_detalle_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_compra INTEGER NOT NULL,
        id_producto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
                
        FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
        FOREIGN KEY (id_producto) REFERENCES Productos(id_productos) ON DELETE CASCADE
    );
                
    CREATE TABLE IF NOT EXISTS Detalle_venta(
        id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER NOT NULL,
        id_producto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        descuento_aplicado INTEGER NOT NULL,
                
        FOREIGN KEY (id_venta) REFERENCES Venta(id_venta) ON DELETE CASCADE, 
        FOREIGN KEY (id_producto) REFERENCES Productos(id_productos) ON DELETE CASCADE
    );
''');
    conn.commit();
    conn.close();

crear_tablas()