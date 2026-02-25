from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de ruta automática para la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nova_style.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================
# ENDPOINTS DE PRODUCTOS
# ============================================

# 1. OBTENER TODOS LOS PRODUCTOS
@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        productos = conn.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            ORDER BY p.fecha_creacion DESC
        ''').fetchall()
        conn.close()
        return jsonify([dict(p) for p in productos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. OBTENER PRODUCTO POR ID (con detalles completos)
@app.route('/api/productos/<int:id>', methods=['GET'])
def get_producto(id):
    try:
        conn = get_db_connection()
        
        # Obtener producto básico
        producto = conn.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.id_producto = ?
        ''', (id,)).fetchone()
        
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Obtener imágenes
        imagenes = conn.execute('''
            SELECT * FROM producto_imagenes 
            WHERE id_producto = ?
            ORDER BY es_principal DESC, orden
        ''', (id,)).fetchall()
        
        # Obtener tallas
        tallas = conn.execute('''
            SELECT t.*, pt.stock
            FROM producto_tallas pt
            JOIN tallas t ON pt.id_talla = t.id_talla
            WHERE pt.id_producto = ?
        ''', (id,)).fetchall()
        
        # Obtener colores
        colores = conn.execute('''
            SELECT c.*, pc.stock
            FROM producto_colores pc
            JOIN colores c ON pc.id_color = c.id_color
            WHERE pc.id_producto = ?
        ''', (id,)).fetchall()
        
        conn.close()
        
        producto_dict = dict(producto)
        producto_dict['imagenes'] = [dict(img) for img in imagenes]
        producto_dict['tallas'] = [dict(t) for t in tallas]
        producto_dict['colores'] = [dict(c) for c in colores]
        
        return jsonify(producto_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. CREAR PRODUCTO
@app.route('/api/productos', methods=['POST'])
def add_producto():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insertar producto
        cursor.execute('''
            INSERT INTO productos 
            (nombre, descripcion, precio, precio_descuento, referencia, 
             id_categoria, genero, stock, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('nombre'),
            data.get('descripcion', ''),
            data.get('precio'),
            data.get('precio_descuento'),
            data.get('referencia'),
            data.get('id_categoria'),
            data.get('genero', 'unisex'),
            data.get('stock', 0),
            data.get('activo', 1)
        ))
        
        producto_id = cursor.lastrowid
        
        # Insertar imágenes si las hay
        if 'imagenes' in data and data['imagenes']:
            for idx, img_url in enumerate(data['imagenes']):
                cursor.execute('''
                    INSERT INTO producto_imagenes 
                    (id_producto, url_imagen, es_principal, orden)
                    VALUES (?, ?, ?, ?)
                ''', (producto_id, img_url, 1 if idx == 0 else 0, idx))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "mensaje": "Producto creado exitosamente",
            "id_producto": producto_id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. ACTUALIZAR PRODUCTO
@app.route('/api/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, 
                descripcion = ?,
                precio = ?, 
                precio_descuento = ?,
                stock = ?, 
                referencia = ?,
                id_categoria = ?,
                genero = ?,
                activo = ?,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_producto = ?
        ''', (
            data.get('nombre'),
            data.get('descripcion', ''),
            data.get('precio'),
            data.get('precio_descuento'),
            data.get('stock'),
            data.get('referencia'),
            data.get('id_categoria'),
            data.get('genero', 'unisex'),
            data.get('activo', 1),
            id
        ))
        
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Producto no encontrado"}), 404
            
        return jsonify({"mensaje": "Producto actualizado"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. ELIMINAR PRODUCTO
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id_producto = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# ENDPOINTS DE CATEGORÍAS
# ============================================

@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    try:
        conn = get_db_connection()
        categorias = conn.execute('SELECT * FROM categorias WHERE activo = 1').fetchall()
        conn.close()
        return jsonify([dict(c) for c in categorias])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categorias', methods=['POST'])
def add_categoria():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO categorias (nombre, descripcion, imagen_url)
            VALUES (?, ?, ?)
        ''', (data['nombre'], data.get('descripcion', ''), data.get('imagen_url', '')))
        
        conn.commit()
        categoria_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "mensaje": "Categoría creada",
            "id_categoria": categoria_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# ENDPOINTS DE IMÁGENES DE PRODUCTOS
# ============================================

@app.route('/api/productos/<int:id_producto>/imagenes', methods=['POST'])
def add_imagen_producto(id_producto):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener el orden máximo actual
        max_orden = cursor.execute('''
            SELECT MAX(orden) FROM producto_imagenes WHERE id_producto = ?
        ''', (id_producto,)).fetchone()[0]
        
        nuevo_orden = (max_orden or -1) + 1
        
        cursor.execute('''
            INSERT INTO producto_imagenes 
            (id_producto, url_imagen, es_principal, orden)
            VALUES (?, ?, ?, ?)
        ''', (
            id_producto,
            data['url_imagen'],
            data.get('es_principal', 0),
            nuevo_orden
        ))
        
        conn.commit()
        imagen_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "mensaje": "Imagen agregada",
            "id_imagen": imagen_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/imagenes/<int:id>', methods=['DELETE'])
def eliminar_imagen(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM producto_imagenes WHERE id_imagen = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Imagen eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# ENDPOINTS DE TALLAS Y COLORES
# ============================================

@app.route('/api/tallas', methods=['GET'])
def get_tallas():
    try:
        conn = get_db_connection()
        tallas = conn.execute('SELECT * FROM tallas ORDER BY nombre').fetchall()
        conn.close()
        return jsonify([dict(t) for t in tallas])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/colores', methods=['GET'])
def get_colores():
    try:
        conn = get_db_connection()
        colores = conn.execute('SELECT * FROM colores ORDER BY nombre').fetchall()
        conn.close()
        return jsonify([dict(c) for c in colores])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# ENDPOINTS DE ESTADÍSTICAS
# ============================================

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    try:
        conn = get_db_connection()
        
        stats = {
            'total_productos': conn.execute('SELECT COUNT(*) FROM productos WHERE activo = 1').fetchone()[0],
            'productos_sin_stock': conn.execute('SELECT COUNT(*) FROM productos WHERE stock = 0 AND activo = 1').fetchone()[0],
            'total_categorias': conn.execute('SELECT COUNT(*) FROM categorias WHERE activo = 1').fetchone()[0],
            'valor_inventario': conn.execute('SELECT SUM(precio * stock) FROM productos WHERE activo = 1').fetchone()[0] or 0,
            'productos_recientes': conn.execute('''
                SELECT COUNT(*) FROM productos 
                WHERE DATE(fecha_creacion) >= DATE('now', '-7 days')
            ''').fetchone()[0]
        }
        
        # Productos por categoría
        productos_por_categoria = conn.execute('''
            SELECT c.nombre, COUNT(p.id_producto) as total
            FROM categorias c
            LEFT JOIN productos p ON c.id_categoria = p.id_categoria AND p.activo = 1
            WHERE c.activo = 1
            GROUP BY c.id_categoria
        ''').fetchall()
        
        stats['por_categoria'] = [dict(row) for row in productos_por_categoria]
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "mensaje": "API Nova Style funcionando correctamente",
        "database": DB_PATH,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 API NOVA STYLE - PANEL DE ADMINISTRADOR")
    print("=" * 60)
    print(f"📍 Servidor: http://127.0.0.1:5000")
    print(f"💾 Base de datos: {DB_PATH}")
    print("=" * 60)
    print("\n📋 Endpoints disponibles:")
    print("   GET    /api/health")
    print("   GET    /api/productos")
    print("   GET    /api/productos/<id>")
    print("   POST   /api/productos")
    print("   PUT    /api/productos/<id>")
    print("   DELETE /api/productos/<id>")
    print("   GET    /api/categorias")
    print("   POST   /api/categorias")
    print("   GET    /api/tallas")
    print("   GET    /api/colores")
    print("   GET    /api/estadisticas")
    print("=" * 60)
    print("\n✅ Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')
