#!/usr/bin/env python3
"""
Módulo de consultas para la base de datos Nova Style
Contiene funciones útiles para interactuar con la BD
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
import json

DB_PATH = 'nova_style.db'

class NovaStyleDB:
    """Clase para manejar las operaciones de la base de datos"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        return conn
    
    # ==================== PRODUCTOS ====================
    
    def obtener_todos_productos(self) -> List[Dict]:
        """Obtiene todos los productos activos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen_principal
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.activo = 1
            ORDER BY p.fecha_creacion DESC
        ''')
        
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Dict]:
        """Obtiene un producto específico con todas sus imágenes"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Obtener datos del producto
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.id_producto = ? AND p.activo = 1
        ''', (id_producto,))
        
        producto = cursor.fetchone()
        
        if not producto:
            conn.close()
            return None
        
        producto = dict(producto)
        
        # Obtener imágenes
        cursor.execute('''
            SELECT url_imagen, es_principal, orden
            FROM producto_imagenes
            WHERE id_producto = ?
            ORDER BY orden
        ''', (id_producto,))
        
        producto['imagenes'] = [dict(row) for row in cursor.fetchall()]
        
        # Obtener tallas disponibles
        cursor.execute('''
            SELECT t.id_talla, t.nombre, pt.stock
            FROM producto_tallas pt
            JOIN tallas t ON pt.id_talla = t.id_talla
            WHERE pt.id_producto = ? AND pt.stock > 0
        ''', (id_producto,))
        
        producto['tallas'] = [dict(row) for row in cursor.fetchall()]
        
        # Obtener colores disponibles
        cursor.execute('''
            SELECT c.id_color, c.nombre, c.codigo_hex, pc.stock
            FROM producto_colores pc
            JOIN colores c ON pc.id_color = c.id_color
            WHERE pc.id_producto = ? AND pc.stock > 0
        ''', (id_producto,))
        
        producto['colores'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return producto
    
    def obtener_productos_por_categoria(self, nombre_categoria: str) -> List[Dict]:
        """Obtiene productos de una categoría específica"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen_principal
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE c.nombre = ? AND p.activo = 1
            ORDER BY p.fecha_creacion DESC
        ''', (nombre_categoria,))
        
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos
    
    def obtener_productos_por_genero(self, genero: str) -> List[Dict]:
        """Obtiene productos por género (hombre, mujer, unisex)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen_principal
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.genero = ? AND p.activo = 1
            ORDER BY p.fecha_creacion DESC
        ''', (genero,))
        
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos
    
    def buscar_productos(self, termino: str) -> List[Dict]:
        """Busca productos por nombre o descripción"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen_principal
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE (p.nombre LIKE ? OR p.descripcion LIKE ?) AND p.activo = 1
            ORDER BY p.fecha_creacion DESC
        ''', (f'%{termino}%', f'%{termino}%'))
        
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos
    
    # ==================== CATEGORÍAS ====================
    
    def obtener_categorias(self) -> List[Dict]:
        """Obtiene todas las categorías activas"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, 
                   COUNT(p.id_producto) as total_productos
            FROM categorias c
            LEFT JOIN productos p ON c.id_categoria = p.id_categoria AND p.activo = 1
            WHERE c.activo = 1
            GROUP BY c.id_categoria
        ''')
        
        categorias = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return categorias
    
    # ==================== CARRITO ====================
    
    def agregar_al_carrito(self, id_usuario: int, id_producto: int, 
                          id_talla: Optional[int] = None, 
                          id_color: Optional[int] = None, 
                          cantidad: int = 1) -> bool:
        """Agrega un producto al carrito"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya existe en el carrito
            cursor.execute('''
                SELECT id_carrito, cantidad 
                FROM carrito 
                WHERE id_usuario = ? AND id_producto = ? 
                AND (id_talla = ? OR (id_talla IS NULL AND ? IS NULL))
                AND (id_color = ? OR (id_color IS NULL AND ? IS NULL))
            ''', (id_usuario, id_producto, id_talla, id_talla, id_color, id_color))
            
            item_existente = cursor.fetchone()
            
            if item_existente:
                # Actualizar cantidad
                nueva_cantidad = item_existente[1] + cantidad
                cursor.execute('''
                    UPDATE carrito 
                    SET cantidad = ? 
                    WHERE id_carrito = ?
                ''', (nueva_cantidad, item_existente[0]))
            else:
                # Insertar nuevo item
                cursor.execute('''
                    INSERT INTO carrito 
                    (id_usuario, id_producto, id_talla, id_color, cantidad)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id_usuario, id_producto, id_talla, id_color, cantidad))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar al carrito: {e}")
            conn.close()
            return False
    
    def obtener_carrito(self, id_usuario: int) -> List[Dict]:
        """Obtiene el carrito de un usuario"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id_carrito, c.cantidad, c.fecha_agregado,
                   p.id_producto, p.nombre, p.precio, p.referencia,
                   t.nombre as talla,
                   col.nombre as color,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen
            FROM carrito c
            JOIN productos p ON c.id_producto = p.id_producto
            LEFT JOIN tallas t ON c.id_talla = t.id_talla
            LEFT JOIN colores col ON c.id_color = col.id_color
            WHERE c.id_usuario = ?
            ORDER BY c.fecha_agregado DESC
        ''', (id_usuario,))
        
        items = [dict(row) for row in cursor.fetchall()]
        
        # Calcular subtotal para cada item
        for item in items:
            item['subtotal'] = item['precio'] * item['cantidad']
        
        conn.close()
        return items
    
    def eliminar_del_carrito(self, id_carrito: int) -> bool:
        """Elimina un item del carrito"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM carrito WHERE id_carrito = ?', (id_carrito,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def vaciar_carrito(self, id_usuario: int) -> bool:
        """Vacía el carrito de un usuario"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM carrito WHERE id_usuario = ?', (id_usuario,))
        conn.commit()
        conn.close()
        return True
    
    # ==================== FAVORITOS ====================
    
    def agregar_a_favoritos(self, id_usuario: int, id_producto: int) -> bool:
        """Agrega un producto a favoritos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO favoritos (id_usuario, id_producto)
                VALUES (?, ?)
            ''', (id_usuario, id_producto))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Ya existe en favoritos
            conn.close()
            return False
    
    def obtener_favoritos(self, id_usuario: int) -> List[Dict]:
        """Obtiene los favoritos de un usuario"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.id_favorito, f.fecha_agregado,
                   p.id_producto, p.nombre, p.precio, p.referencia,
                   (SELECT url_imagen FROM producto_imagenes 
                    WHERE id_producto = p.id_producto AND es_principal = 1 
                    LIMIT 1) as imagen
            FROM favoritos f
            JOIN productos p ON f.id_producto = p.id_producto
            WHERE f.id_usuario = ? AND p.activo = 1
            ORDER BY f.fecha_agregado DESC
        ''', (id_usuario,))
        
        favoritos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return favoritos
    
    def eliminar_de_favoritos(self, id_usuario: int, id_producto: int) -> bool:
        """Elimina un producto de favoritos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM favoritos 
            WHERE id_usuario = ? AND id_producto = ?
        ''', (id_usuario, id_producto))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    # ==================== UTILIDADES ====================
    
    def exportar_catalogo_json(self, archivo: str = 'catalogo.json'):
        """Exporta el catálogo completo a JSON"""
        productos = self.obtener_todos_productos()
        
        # Obtener detalles completos de cada producto
        catalogo_completo = []
        for prod in productos:
            producto_completo = self.obtener_producto_por_id(prod['id_producto'])
            if producto_completo:
                catalogo_completo.append(producto_completo)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(catalogo_completo, f, ensure_ascii=False, indent=2)
        
        return len(catalogo_completo)
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas generales de la base de datos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de productos
        cursor.execute('SELECT COUNT(*) FROM productos WHERE activo = 1')
        stats['total_productos'] = cursor.fetchone()[0]
        
        # Total de categorías
        cursor.execute('SELECT COUNT(*) FROM categorias WHERE activo = 1')
        stats['total_categorias'] = cursor.fetchone()[0]
        
        # Total de usuarios
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE activo = 1')
        stats['total_usuarios'] = cursor.fetchone()[0]
        
        # Producto más caro
        cursor.execute('SELECT nombre, precio FROM productos WHERE activo = 1 ORDER BY precio DESC LIMIT 1')
        producto_caro = cursor.fetchone()
        if producto_caro:
            stats['producto_mas_caro'] = {
                'nombre': producto_caro[0],
                'precio': producto_caro[1]
            }
        
        # Producto más barato
        cursor.execute('SELECT nombre, precio FROM productos WHERE activo = 1 ORDER BY precio ASC LIMIT 1')
        producto_barato = cursor.fetchone()
        if producto_barato:
            stats['producto_mas_barato'] = {
                'nombre': producto_barato[0],
                'precio': producto_barato[1]
            }
        
        # Precio promedio
        cursor.execute('SELECT AVG(precio) FROM productos WHERE activo = 1')
        stats['precio_promedio'] = round(cursor.fetchone()[0], 2)
        
        conn.close()
        return stats


# Funciones de ejemplo para probar
def ejemplo_uso():
    """Ejemplos de uso de la base de datos"""
    db = NovaStyleDB()
    
    print("=" * 60)
    print("EJEMPLOS DE USO DE LA BASE DE DATOS")
    print("=" * 60)
    
    # 1. Obtener todos los productos
    print("\n1. Todos los productos:")
    productos = db.obtener_todos_productos()
    for p in productos[:3]:  # Solo primeros 3
        print(f"   - {p['nombre']}: ${p['precio']}")
    
    # 2. Obtener productos de una categoría
    print("\n2. Productos de Hombre:")
    productos_hombre = db.obtener_productos_por_categoria('Hombre')
    for p in productos_hombre:
        print(f"   - {p['nombre']}: ${p['precio']}")
    
    # 3. Buscar productos
    print("\n3. Buscar 'pantalón':")
    resultados = db.buscar_productos('pantalón')
    for p in resultados:
        print(f"   - {p['nombre']}: ${p['precio']}")
    
    # 4. Obtener estadísticas
    print("\n4. Estadísticas:")
    stats = db.obtener_estadisticas()
    for key, value in stats.items():
        print(f"   - {key}: {value}")
    
    # 5. Exportar catálogo
    print("\n5. Exportando catálogo a JSON...")
    total = db.exportar_catalogo_json()
    print(f"   ✅ {total} productos exportados a catalogo.json")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    ejemplo_uso()
