# 🗄️ BASE DE DATOS NOVA STYLE

## 📋 Descripción General

Base de datos SQLite completa para el e-commerce Nova Style, diseñada para manejar productos, usuarios, pedidos, carrito de compras y más.

---

## 📊 Diagrama de Tablas

```
┌─────────────────┐
│   CATEGORÍAS    │
├─────────────────┤
│ id_categoria PK │
│ nombre          │
│ descripcion     │
│ imagen_url      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐       ┌──────────────────┐
│   PRODUCTOS     │───────│ PRODUCTO_IMAGENES│
├─────────────────┤  1:N  ├──────────────────┤
│ id_producto PK  │       │ id_imagen PK     │
│ nombre          │       │ id_producto FK   │
│ precio          │       │ url_imagen       │
│ id_categoria FK │       │ es_principal     │
│ genero          │       │ orden            │
│ stock           │       └──────────────────┘
└─────────────────┘
     │   │
     │   │ N:M (a través de tablas intermedias)
     │   │
     ▼   ▼
┌─────────────────┐    ┌─────────────────┐
│ PRODUCTO_TALLAS │    │ PRODUCTO_COLORES│
├─────────────────┤    ├─────────────────┤
│ id_producto FK  │    │ id_producto FK  │
│ id_talla FK     │    │ id_color FK     │
│ stock           │    │ stock           │
└─────────────────┘    └─────────────────┘
     │                      │
     ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│     TALLAS      │    │     COLORES     │
├─────────────────┤    ├─────────────────┤
│ id_talla PK     │    │ id_color PK     │
│ nombre          │    │ nombre          │
│ categoria       │    │ codigo_hex      │
└─────────────────┘    └─────────────────┘

┌─────────────────┐
│    USUARIOS     │
├─────────────────┤
│ id_usuario PK   │
│ nombre          │
│ email           │
│ password_hash   │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  DIRECCIONES    │    │    CARRITO      │    │   FAVORITOS     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id_direccion PK │    │ id_carrito PK   │    │ id_favorito PK  │
│ id_usuario FK   │    │ id_usuario FK   │    │ id_usuario FK   │
│ calle           │    │ id_producto FK  │    │ id_producto FK  │
│ ciudad          │    │ id_talla FK     │    └─────────────────┘
│ codigo_postal   │    │ id_color FK     │
└─────────────────┘    │ cantidad        │
                       └─────────────────┘

┌─────────────────┐
│    PEDIDOS      │
├─────────────────┤
│ id_pedido PK    │
│ id_usuario FK   │
│ numero_pedido   │
│ total           │
│ estado          │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│ PEDIDO_DETALLES │
├─────────────────┤
│ id_detalle PK   │
│ id_pedido FK    │
│ id_producto FK  │
│ cantidad        │
│ precio_unitario │
└─────────────────┘
```

---

## 📁 Estructura de Tablas

### 1. **categorias**
Almacena las categorías principales de productos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_categoria | INTEGER PK | ID único |
| nombre | VARCHAR(50) | Nombre de la categoría |
| descripcion | TEXT | Descripción |
| imagen_url | VARCHAR(255) | URL de imagen representativa |
| activo | BOOLEAN | Estado activo/inactivo |
| fecha_creacion | TIMESTAMP | Fecha de creación |

**Datos actuales:**
- Hombre
- Mujer
- Calzado
- Accesorios

---

### 2. **productos**
Tabla principal de productos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_producto | INTEGER PK | ID único |
| nombre | VARCHAR(100) | Nombre del producto |
| descripcion | TEXT | Descripción detallada |
| precio | DECIMAL(10,2) | Precio regular |
| precio_descuento | DECIMAL(10,2) | Precio en descuento |
| referencia | VARCHAR(50) | SKU/Referencia única |
| id_categoria | INTEGER FK | ID de categoría |
| genero | VARCHAR(20) | 'hombre', 'mujer', 'unisex' |
| stock | INTEGER | Cantidad en inventario |
| activo | BOOLEAN | Estado activo/inactivo |

**Productos actuales:** 12 productos en total

---

### 3. **producto_imagenes**
Almacena múltiples imágenes por producto.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_imagen | INTEGER PK | ID único |
| id_producto | INTEGER FK | ID del producto |
| url_imagen | VARCHAR(500) | URL de la imagen |
| es_principal | BOOLEAN | Si es la imagen principal |
| orden | INTEGER | Orden de visualización |

---

### 4. **tallas**
Catálogo de tallas disponibles.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_talla | INTEGER PK | ID único |
| nombre | VARCHAR(10) | Nombre de la talla |
| categoria | VARCHAR(20) | 'ropa', 'calzado', 'accesorio' |

**Tallas disponibles:**
- Ropa: XS, S, M, L, XL, XXL
- Calzado: 23-30 (MX)
- Accesorios: ÚNICA

---

### 5. **producto_tallas**
Relación muchos a muchos entre productos y tallas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_producto_talla | INTEGER PK | ID único |
| id_producto | INTEGER FK | ID del producto |
| id_talla | INTEGER FK | ID de la talla |
| stock | INTEGER | Stock disponible |

---

### 6. **colores**
Catálogo de colores disponibles.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_color | INTEGER PK | ID único |
| nombre | VARCHAR(50) | Nombre del color |
| codigo_hex | VARCHAR(7) | Código hexadecimal |

**Colores disponibles:** 12 colores (Negro, Blanco, Gris, Azul, Rojo, etc.)

---

### 7. **producto_colores**
Relación muchos a muchos entre productos y colores.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_producto_color | INTEGER PK | ID único |
| id_producto | INTEGER FK | ID del producto |
| id_color | INTEGER FK | ID del color |
| stock | INTEGER | Stock disponible |

---

### 8. **usuarios**
Información de usuarios registrados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_usuario | INTEGER PK | ID único |
| nombre | VARCHAR(100) | Nombre completo |
| email | VARCHAR(100) | Email (único) |
| password_hash | VARCHAR(255) | Contraseña hasheada |
| telefono | VARCHAR(20) | Teléfono |
| fecha_registro | TIMESTAMP | Fecha de registro |
| activo | BOOLEAN | Estado activo/inactivo |

**Usuario demo:**
- Email: eddy@novastyle.com
- Password: demo123

---

### 9. **direcciones**
Direcciones de envío de usuarios.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_direccion | INTEGER PK | ID único |
| id_usuario | INTEGER FK | ID del usuario |
| nombre_completo | VARCHAR(100) | Nombre del destinatario |
| calle | VARCHAR(200) | Calle |
| numero_exterior | VARCHAR(20) | Número exterior |
| colonia | VARCHAR(100) | Colonia |
| ciudad | VARCHAR(100) | Ciudad |
| estado | VARCHAR(100) | Estado |
| codigo_postal | VARCHAR(10) | CP |
| pais | VARCHAR(50) | País (default: México) |
| es_principal | BOOLEAN | Dirección principal |

---

### 10. **carrito**
Items en el carrito de compras.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_carrito | INTEGER PK | ID único |
| id_usuario | INTEGER FK | ID del usuario |
| id_producto | INTEGER FK | ID del producto |
| id_talla | INTEGER FK | ID de talla (opcional) |
| id_color | INTEGER FK | ID de color (opcional) |
| cantidad | INTEGER | Cantidad |
| fecha_agregado | TIMESTAMP | Fecha de agregado |

---

### 11. **favoritos**
Lista de deseos de usuarios.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_favorito | INTEGER PK | ID único |
| id_usuario | INTEGER FK | ID del usuario |
| id_producto | INTEGER FK | ID del producto |
| fecha_agregado | TIMESTAMP | Fecha de agregado |

---

### 12. **pedidos**
Información de pedidos realizados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_pedido | INTEGER PK | ID único |
| id_usuario | INTEGER FK | ID del usuario |
| numero_pedido | VARCHAR(50) | Número de pedido único |
| subtotal | DECIMAL(10,2) | Subtotal |
| descuento | DECIMAL(10,2) | Descuento aplicado |
| envio | DECIMAL(10,2) | Costo de envío |
| total | DECIMAL(10,2) | Total a pagar |
| estado | VARCHAR(50) | Estado del pedido |
| metodo_pago | VARCHAR(50) | Método de pago |

**Estados de pedido:**
- pendiente
- confirmado
- enviado
- entregado
- cancelado

---

### 13. **pedido_detalles**
Detalles de productos en cada pedido.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_detalle | INTEGER PK | ID único |
| id_pedido | INTEGER FK | ID del pedido |
| id_producto | INTEGER FK | ID del producto |
| id_talla | INTEGER FK | Talla seleccionada |
| id_color | INTEGER FK | Color seleccionado |
| cantidad | INTEGER | Cantidad |
| precio_unitario | DECIMAL(10,2) | Precio al momento |
| subtotal | DECIMAL(10,2) | Subtotal del item |

---

### 14. **reviews**
Opiniones y calificaciones de productos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_review | INTEGER PK | ID único |
| id_producto | INTEGER FK | ID del producto |
| id_usuario | INTEGER FK | ID del usuario |
| calificacion | INTEGER | 1-5 estrellas |
| titulo | VARCHAR(100) | Título de la review |
| comentario | TEXT | Comentario detallado |
| verificado | BOOLEAN | Si compró el producto |

---

## 🔧 Archivos del Proyecto

### 1. `schema.sql`
Script SQL completo para crear todas las tablas e índices.

**Uso:**
```bash
sqlite3 nova_style.db < schema.sql
```

---

### 2. `init_db.py`
Script Python para inicializar la base de datos con datos de ejemplo.

**Uso:**
```bash
python3 init_db.py
```

**Funciones:**
- Crea la base de datos
- Inserta categorías
- Inserta tallas y colores
- Inserta 12 productos con imágenes
- Asigna tallas y colores a productos
- Crea usuario demo

---

### 3. `db_queries.py`
Módulo Python con clase `NovaStyleDB` para consultas.

**Métodos principales:**

#### Productos
- `obtener_todos_productos()` - Lista todos los productos
- `obtener_producto_por_id(id)` - Detalles de un producto
- `obtener_productos_por_categoria(nombre)` - Productos por categoría
- `obtener_productos_por_genero(genero)` - Productos por género
- `buscar_productos(termino)` - Búsqueda de productos

#### Carrito
- `agregar_al_carrito(id_usuario, id_producto, ...)` - Agregar al carrito
- `obtener_carrito(id_usuario)` - Ver carrito
- `eliminar_del_carrito(id_carrito)` - Eliminar item
- `vaciar_carrito(id_usuario)` - Vaciar carrito

#### Favoritos
- `agregar_a_favoritos(id_usuario, id_producto)` - Agregar a favoritos
- `obtener_favoritos(id_usuario)` - Ver favoritos
- `eliminar_de_favoritos(id_usuario, id_producto)` - Eliminar favorito

#### Utilidades
- `exportar_catalogo_json()` - Exporta catálogo a JSON
- `obtener_estadisticas()` - Estadísticas generales

**Ejemplo de uso:**
```python
from db_queries import NovaStyleDB

db = NovaStyleDB()

# Obtener todos los productos
productos = db.obtener_todos_productos()

# Buscar productos
resultados = db.buscar_productos('pantalón')

# Agregar al carrito
db.agregar_al_carrito(
    id_usuario=1,
    id_producto=1,
    id_talla=3,  # M
    id_color=1,  # Negro
    cantidad=2
)
```

---

### 4. `api.py`
API REST con Flask para acceder a la base de datos.

**Endpoints disponibles:**

#### Productos
- `GET /api/productos` - Todos los productos
- `GET /api/productos/<id>` - Producto específico
- `GET /api/productos/categoria/<nombre>` - Por categoría
- `GET /api/productos/genero/<genero>` - Por género
- `GET /api/productos/buscar?q=<termino>` - Búsqueda

#### Categorías
- `GET /api/categorias` - Todas las categorías

#### Carrito
- `GET /api/carrito/<id_usuario>` - Ver carrito
- `POST /api/carrito` - Agregar al carrito
- `DELETE /api/carrito/<id_carrito>` - Eliminar item

#### Favoritos
- `GET /api/favoritos/<id_usuario>` - Ver favoritos
- `POST /api/favoritos` - Agregar favorito
- `DELETE /api/favoritos/<id_usuario>/<id_producto>` - Eliminar

#### Estadísticas
- `GET /api/estadisticas` - Estadísticas generales

**Iniciar servidor:**
```bash
pip install flask flask-cors
python3 api.py
```

Servidor en: `http://localhost:5000`

---

## 📈 Estadísticas Actuales

- **Productos:** 12
- **Categorías:** 4
- **Imágenes:** 19
- **Tallas:** 15
- **Colores:** 12
- **Usuarios:** 1 (demo)

**Precios:**
- Más caro: Vestido Elegante ($1,599)
- Más barato: Pulsera Elegante ($299)
- Promedio: $978.25

---

## 🚀 Instrucciones de Uso

### Instalación Inicial

1. **Crear la base de datos:**
```bash
cd database
python3 init_db.py
```

2. **Probar consultas:**
```bash
python3 db_queries.py
```

3. **Iniciar API (opcional):**
```bash
pip install flask flask-cors
python3 api.py
```

### Integración con el Frontend

El archivo `catalogo.json` generado puede usarse directamente en JavaScript:

```javascript
// Cargar productos
fetch('database/catalogo.json')
    .then(response => response.json())
    .then(productos => {
        // Mostrar productos
        productos.forEach(producto => {
            console.log(producto.nombre, producto.precio);
        });
    });
```

O usando la API:

```javascript
// Obtener productos
fetch('http://localhost:5000/api/productos')
    .then(response => response.json())
    .then(data => {
        console.log(data.data); // Array de productos
    });
```

---

## 🔒 Seguridad

**IMPORTANTE:** En producción:

1. ✅ Usar contraseñas hasheadas (bcrypt)
2. ✅ Implementar autenticación JWT
3. ✅ Validar todos los inputs
4. ✅ Usar HTTPS
5. ✅ Implementar rate limiting
6. ✅ Sanitizar consultas SQL

---

## 📝 Notas

- Base de datos SQLite (fácil de usar, sin instalación)
- Perfecta para desarrollo y testing
- Para producción, considerar PostgreSQL o MySQL
- Todos los precios en MXN (pesos mexicanos)

---

## 🎯 Próximos Pasos

1. Implementar sistema de autenticación
2. Agregar más productos
3. Crear sistema de procesamiento de pedidos
4. Implementar notificaciones por email
5. Agregar panel de administración
6. Integrar pasarela de pagos
7. Sistema de inventario en tiempo real
8. Analytics y reportes

---

**Creado por:** Nova Style Team  
**Fecha:** Febrero 2026  
**Versión:** 1.0
