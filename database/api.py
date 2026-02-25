from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Configuración de ruta automática para la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nova_style.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. VER PRODUCTOS
@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        productos = conn.execute('SELECT * FROM productos').fetchall()
        conn.close()
        return jsonify([dict(p) for p in productos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. AGREGAR PRODUCTO
@app.route('/api/productos', methods=['POST'])
def add_producto():
    try:
        data = request.get_json()
        conn = get_db_connection()
        conn.execute('INSERT INTO productos (nombre, precio, stock, referencia) VALUES (?, ?, ?, ?)',
                     (data['nombre'], data['precio'], data['stock'], data['referencia']))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "exito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. EDITAR PRODUCTO (Esta es la que te faltaba)
@app.route('/api/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, precio = ?, stock = ?, referencia = ? 
            WHERE id_producto = ?
        ''', (data['nombre'], data['precio'], data['stock'], data['referencia'], id))
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Producto no encontrado"}), 404
            
        return jsonify({"mensaje": "actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. ELIMINAR PRODUCTO
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id_producto = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor Nova Style funcionando con CRUD completo")
    app.run(debug=True, port=5000)