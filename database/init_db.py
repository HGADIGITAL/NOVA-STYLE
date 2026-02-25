#!/usr/bin/env python3
"""
Script para crear y poblar la base de datos de Nova Style
"""

import sqlite3
import os
from datetime import datetime

# Ruta de la base de datos
DB_PATH = 'nova_style.db'

def crear_base_datos():
    """Crea la base de datos y todas las tablas"""
    print("📦 Creando base de datos...")
    
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Leer el archivo SQL del schema
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Ejecutar el script SQL
    cursor.executescript(schema_sql)
    conn.commit()
    
    print("✅ Base de datos creada exitosamente!")
    return conn

def poblar_categorias(conn):
    """Inserta las categorías principales"""
    print("\n📁 Insertando categorías...")
    
    categorias = [
        ('Hombre', 'Ropa y accesorios para hombre', 'https://static.bershka.net/assets/public/b6eb/81bb/5bc546e58706/2e3ed6262c76/03400190800-a4o/03400190800-a4o.jpg'),
        ('Mujer', 'Ropa y accesorios para mujer', 'https://static.bershka.net/assets/public/176b/be5a/09994e7f9c8b/82ff463297f7/00689187700-b/00689187700-b.jpg'),
        ('Calzado', 'Zapatos, tenis, botas y más', 'https://static.bershka.net/assets/public/338d/3d33/a2674a64ac59/e2303fb7102b/11640560040-a3o/11640560040-a3o.jpg'),
        ('Accesorios', 'Complementos y accesorios de moda', 'https://static.bershka.net/assets/public/f7b3/bb46/790542e99624/0f53731b5cac/0408316280003-p/0408316280003-p.jpg'),
    ]
    
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO categorias (nombre, descripcion, imagen_url) VALUES (?, ?, ?)',
        categorias
    )
    conn.commit()
    print(f"✅ {len(categorias)} categorías insertadas")

def poblar_tallas(conn):
    """Inserta las tallas disponibles"""
    print("\n📏 Insertando tallas...")
    
    tallas = [
        # Tallas de ropa
        ('XS', 'ropa'),
        ('S', 'ropa'),
        ('M', 'ropa'),
        ('L', 'ropa'),
        ('XL', 'ropa'),
        ('XXL', 'ropa'),
        # Tallas de calzado (MX)
        ('23', 'calzado'),
        ('24', 'calzado'),
        ('25', 'calzado'),
        ('26', 'calzado'),
        ('27', 'calzado'),
        ('28', 'calzado'),
        ('29', 'calzado'),
        ('30', 'calzado'),
        # Talla única
        ('ÚNICA', 'accesorio'),
    ]
    
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO tallas (nombre, categoria) VALUES (?, ?)',
        tallas
    )
    conn.commit()
    print(f"✅ {len(tallas)} tallas insertadas")

def poblar_colores(conn):
    """Inserta los colores disponibles"""
    print("\n🎨 Insertando colores...")
    
    colores = [
        ('Negro', '#000000'),
        ('Blanco', '#FFFFFF'),
        ('Gris', '#808080'),
        ('Azul', '#0000FF'),
        ('Rojo', '#FF0000'),
        ('Verde', '#008000'),
        ('Amarillo', '#FFFF00'),
        ('Naranja', '#FFA500'),
        ('Rosa', '#FFC0CB'),
        ('Morado', '#800080'),
        ('Beige', '#F5F5DC'),
        ('Café', '#8B4513'),
    ]
    
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO colores (nombre, codigo_hex) VALUES (?, ?)',
        colores
    )
    conn.commit()
    print(f"✅ {len(colores)} colores insertados")

def poblar_productos(conn):
    """Inserta los productos del catálogo"""
    print("\n👕 Insertando productos...")
    
    cursor = conn.cursor()
    
    # Obtener IDs de categorías
    cursor.execute("SELECT id_categoria, nombre FROM categorias")
    categorias_dict = {nombre: id_cat for id_cat, nombre in cursor.fetchall()}
    
    productos = [
        # HOMBRE
        {
            'nombre': 'Pantalón Negro Ajustado',
            'descripcion': 'Pantalón negro ajustado de corte moderno, perfecto para ocasiones formales o casuales.',
            'precio': 850.00,
            'referencia': 'H-PANT-001',
            'categoria': 'Hombre',
            'genero': 'hombre',
            'stock': 50,
            'imagenes': [
                'https://static.bershka.net/assets/public/56ea/21cc/be5e42998afb/ce4a40be9a71/00413710800-p/00413710800-p.jpg',
                'https://static.bershka.net/assets/public/39f0/af17/e11a4aa88ee4/17d9608625a0/00413710800-a1t/00413710800-a1t.jpg',
                'https://static.bershka.net/assets/public/b90f/7547/0c0e4246b110/6a077dc88a6e/00413710800-a2d/00413710800-a2d.jpg',
            ]
        },
        {
            'nombre': 'Chaqueta Elegante',
            'descripcion': 'Chaqueta elegante para hombre, ideal para el trabajo o eventos especiales.',
            'precio': 1299.00,
            'referencia': 'H-CHAQ-001',
            'categoria': 'Hombre',
            'genero': 'hombre',
            'stock': 30,
            'imagenes': [
                'https://static.bershka.net/assets/public/2366/9389/4ce049cfa00c/2ba3e1cba64e/01579718200-p/01579718200-p.jpg',
            ]
        },
        {
            'nombre': 'Camisa Casual',
            'descripcion': 'Camisa casual de manga larga, perfecta para el día a día.',
            'precio': 599.00,
            'referencia': 'H-CAM-001',
            'categoria': 'Hombre',
            'genero': 'hombre',
            'stock': 45,
            'imagenes': [
                'https://static.bershka.net/assets/public/25cb/a4b8/36754be8aae7/b49a3af0fb7c/01575677800-p/01575677800-p.jpg',
            ]
        },
        
        # MUJER
        {
            'nombre': 'Pantalón Balloon Parachute',
            'descripcion': 'Pantalón balloon parachute técnico, diseño moderno y cómodo.',
            'precio': 1299.00,
            'referencia': 'M-PANT-001',
            'categoria': 'Mujer',
            'genero': 'mujer',
            'stock': 40,
            'imagenes': [
                'https://static.bershka.net/assets/public/9835/6f81/5dc84dd8a88f/b37d4912847b/00110741505-p/00110741505-p.jpg',
                'https://static.bershka.net/assets/public/129e/7bb7/fe644ddbb1af/82824880cfd7/00110741505-a2d/00110741505-a2d.jpg',
                'https://static.bershka.net/assets/public/b179/99d4/cfd440d58f4f/cd89de9786d4/00110741505-a3o/00110741505-a3o.jpg',
            ]
        },
        {
            'nombre': 'Vestido Elegante',
            'descripcion': 'Vestido elegante para ocasiones especiales.',
            'precio': 1599.00,
            'referencia': 'M-VEST-001',
            'categoria': 'Mujer',
            'genero': 'mujer',
            'stock': 25,
            'imagenes': [
                'https://static.bershka.net/assets/public/9cc9/40ae/da744853a5ef/9e09d012246f/00650693700-p/00650693700-p.jpg',
            ]
        },
        {
            'nombre': 'Conjunto Casual',
            'descripcion': 'Conjunto casual de dos piezas, perfecto para el día a día.',
            'precio': 899.00,
            'referencia': 'M-CONJ-001',
            'categoria': 'Mujer',
            'genero': 'mujer',
            'stock': 35,
            'imagenes': [
                'https://static.bershka.net/assets/public/1184/ce74/4a68423d8d87/fb4693472564/03575028401-p/03575028401-p.jpg',
            ]
        },
        
        # CALZADO
        {
            'nombre': 'Zapatillas Deportivas',
            'descripcion': 'Zapatillas deportivas cómodas y modernas, ideales para entrenar o uso casual.',
            'precio': 1199.00,
            'referencia': 'C-ZAP-001',
            'categoria': 'Calzado',
            'genero': 'unisex',
            'stock': 60,
            'imagenes': [
                'https://static.bershka.net/assets/public/161f/883d/43c7405598e9/3a6cc114453f/12485560100-a4o/12485560100-a4o.jpg',
                'https://static.bershka.net/assets/public/39f3/6415/4a8945229766/67a6470f2078/12485560100-a2d/12485560100-a2d.jpg',
                'https://static.bershka.net/assets/public/1107/3e63/59034df18908/1198cc2069a7/12485560100-a1t/12485560100-a1t.jpg',
            ]
        },
        {
            'nombre': 'Tenis Casual',
            'descripcion': 'Tenis casual para uso diario.',
            'precio': 899.00,
            'referencia': 'C-TEN-001',
            'categoria': 'Calzado',
            'genero': 'unisex',
            'stock': 55,
            'imagenes': [
                'https://static.bershka.net/assets/public/72f1/e8a4/0dc449318052/367be42493b6/12616460040-a4o/12616460040-a4o.jpg',
            ]
        },
        {
            'nombre': 'Botas',
            'descripcion': 'Botas elegantes de piel sintética.',
            'precio': 1499.00,
            'referencia': 'C-BOT-001',
            'categoria': 'Calzado',
            'genero': 'unisex',
            'stock': 30,
            'imagenes': [
                'https://static.bershka.net/assets/public/7b1d/d56a/0cc746808398/5defe9c3f153/12478560001-01-a3o/12478560001-01-a3o.jpg',
            ]
        },
        
        # ACCESORIOS
        {
            'nombre': 'Collar Moderno',
            'descripcion': 'Collar moderno con diseño minimalista.',
            'precio': 399.00,
            'referencia': 'A-COLL-001',
            'categoria': 'Accesorios',
            'genero': 'unisex',
            'stock': 100,
            'imagenes': [
                'https://static.bershka.net/assets/public/4ef2/0a7a/009049d3b53d/b7ce2c1db279/04466023302-p/04466023302-p.jpg',
                'https://static.bershka.net/assets/public/c513/183f/9db64fbf8a6c/f9787ded3149/04466023302-a4o/04466023302-a4o.jpg',
            ]
        },
        {
            'nombre': 'Pulsera Elegante',
            'descripcion': 'Pulsera elegante de acero inoxidable.',
            'precio': 299.00,
            'referencia': 'A-PULS-001',
            'categoria': 'Accesorios',
            'genero': 'unisex',
            'stock': 80,
            'imagenes': [
                'https://static.bershka.net/assets/public/8e12/56a9/a34441a7a578/ea834e0d46c0/04469769302-a7o/04469769302-a7o.jpg',
            ]
        },
        {
            'nombre': 'Bolso',
            'descripcion': 'Bolso versátil para uso diario.',
            'precio': 899.00,
            'referencia': 'A-BOLS-001',
            'categoria': 'Accesorios',
            'genero': 'unisex',
            'stock': 40,
            'imagenes': [
                'https://static.bershka.net/assets/public/b215/9855/c9bb44fa909d/e440f9c7dfcf/04120668742-p/04120668742-p.jpg',
            ]
        },
    ]
    
    productos_insertados = 0
    
    for prod in productos:
        # Insertar producto
        cursor.execute('''
            INSERT INTO productos 
            (nombre, descripcion, precio, referencia, id_categoria, genero, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            prod['nombre'],
            prod['descripcion'],
            prod['precio'],
            prod['referencia'],
            categorias_dict[prod['categoria']],
            prod['genero'],
            prod['stock']
        ))
        
        id_producto = cursor.lastrowid
        
        # Insertar imágenes
        for idx, url in enumerate(prod['imagenes']):
            cursor.execute('''
                INSERT INTO producto_imagenes 
                (id_producto, url_imagen, es_principal, orden)
                VALUES (?, ?, ?, ?)
            ''', (id_producto, url, 1 if idx == 0 else 0, idx))
        
        productos_insertados += 1
    
    conn.commit()
    print(f"✅ {productos_insertados} productos insertados")

def poblar_producto_tallas(conn):
    """Asigna tallas a los productos"""
    print("\n📏 Asignando tallas a productos...")
    
    cursor = conn.cursor()
    
    # Obtener productos de ropa (Hombre y Mujer)
    cursor.execute('''
        SELECT p.id_producto 
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE c.nombre IN ('Hombre', 'Mujer')
    ''')
    productos_ropa = [row[0] for row in cursor.fetchall()]
    
    # Obtener productos de calzado
    cursor.execute('''
        SELECT p.id_producto 
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE c.nombre = 'Calzado'
    ''')
    productos_calzado = [row[0] for row in cursor.fetchall()]
    
    # Obtener productos de accesorios
    cursor.execute('''
        SELECT p.id_producto 
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE c.nombre = 'Accesorios'
    ''')
    productos_accesorios = [row[0] for row in cursor.fetchall()]
    
    # Obtener IDs de tallas
    cursor.execute("SELECT id_talla, nombre, categoria FROM tallas")
    tallas_ropa = [row[0] for row in cursor.fetchall() if row[2] == 'ropa']
    tallas_calzado = [row[0] for row in cursor.fetchall() if row[2] == 'calzado']
    tallas_accesorios = [row[0] for row in cursor.fetchall() if row[2] == 'accesorio']
    
    asignaciones = 0
    
    # Asignar tallas de ropa
    for id_producto in productos_ropa:
        for id_talla in tallas_ropa:
            cursor.execute('''
                INSERT INTO producto_tallas (id_producto, id_talla, stock)
                VALUES (?, ?, ?)
            ''', (id_producto, id_talla, 10))
            asignaciones += 1
    
    # Asignar tallas de calzado
    for id_producto in productos_calzado:
        for id_talla in tallas_calzado:
            cursor.execute('''
                INSERT INTO producto_tallas (id_producto, id_talla, stock)
                VALUES (?, ?, ?)
            ''', (id_producto, id_talla, 8))
            asignaciones += 1
    
    # Asignar talla única a accesorios
    for id_producto in productos_accesorios:
        for id_talla in tallas_accesorios:
            cursor.execute('''
                INSERT INTO producto_tallas (id_producto, id_talla, stock)
                VALUES (?, ?, ?)
            ''', (id_producto, id_talla, 50))
            asignaciones += 1
    
    conn.commit()
    print(f"✅ {asignaciones} tallas asignadas a productos")

def poblar_producto_colores(conn):
    """Asigna colores a los productos"""
    print("\n🎨 Asignando colores a productos...")
    
    cursor = conn.cursor()
    
    # Obtener todos los productos
    cursor.execute("SELECT id_producto FROM productos")
    productos = [row[0] for row in cursor.fetchall()]
    
    # Obtener algunos colores populares
    cursor.execute("SELECT id_color FROM colores WHERE nombre IN ('Negro', 'Blanco', 'Gris', 'Azul', 'Beige')")
    colores = [row[0] for row in cursor.fetchall()]
    
    asignaciones = 0
    
    # Asignar 2-3 colores a cada producto
    for id_producto in productos:
        for id_color in colores[:3]:  # Asignar los primeros 3 colores
            cursor.execute('''
                INSERT INTO producto_colores (id_producto, id_color, stock)
                VALUES (?, ?, ?)
            ''', (id_producto, id_color, 15))
            asignaciones += 1
    
    conn.commit()
    print(f"✅ {asignaciones} colores asignados a productos")

def crear_usuario_demo(conn):
    """Crea un usuario de demostración"""
    print("\n👤 Creando usuario de demostración...")
    
    cursor = conn.cursor()
    
    # Usuario demo (password: demo123)
    cursor.execute('''
        INSERT INTO usuarios (nombre, email, password_hash, telefono)
        VALUES (?, ?, ?, ?)
    ''', ('Eddy Demo', 'eddy@novastyle.com', 'demo123hash', '3331234567'))
    
    id_usuario = cursor.lastrowid
    
    # Dirección demo
    cursor.execute('''
        INSERT INTO direcciones 
        (id_usuario, nombre_completo, calle, numero_exterior, colonia, ciudad, estado, codigo_postal, telefono, es_principal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        id_usuario,
        'Eddy Demo',
        'Av. Principal',
        '123',
        'Centro',
        'Tepic',
        'Nayarit',
        '63000',
        '3331234567',
        1
    ))
    
    conn.commit()
    print("✅ Usuario demo creado (email: eddy@novastyle.com)")

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 INICIALIZADOR DE BASE DE DATOS - NOVA STYLE")
    print("=" * 60)
    
    # Crear base de datos
    conn = crear_base_datos()
    
    # Poblar tablas
    poblar_categorias(conn)
    poblar_tallas(conn)
    poblar_colores(conn)
    poblar_productos(conn)
    poblar_producto_tallas(conn)
    poblar_producto_colores(conn)
    crear_usuario_demo(conn)
    
    # Mostrar estadísticas
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM categorias")
    print(f"Categorías: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    print(f"Productos: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM producto_imagenes")
    print(f"Imágenes: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM tallas")
    print(f"Tallas: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM colores")
    print(f"Colores: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    print(f"Usuarios: {cursor.fetchone()[0]}")
    
    print("=" * 60)
    print("✅ Base de datos inicializada correctamente!")
    print(f"📁 Archivo: {DB_PATH}")
    print("=" * 60)
    
    # Cerrar conexión
    conn.close()

if __name__ == "__main__":
    main()
