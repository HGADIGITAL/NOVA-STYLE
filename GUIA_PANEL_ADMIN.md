# 🛠️ GUÍA DE INSTALACIÓN Y USO - PANEL DE ADMINISTRADOR NOVA STYLE

## 📋 CONTENIDO
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Iniciar el Sistema](#iniciar-el-sistema)
4. [Uso del Panel](#uso-del-panel)
5. [Solución de Problemas](#solución-de-problemas)

---

## ✅ REQUISITOS PREVIOS

### Software necesario:
- **Python 3.8+** (para el servidor API)
- **Navegador web moderno** (Chrome, Firefox, Edge, Safari)

### Verificar instalación de Python:
```bash
python3 --version
# o
python --version
```

---

## 🚀 INSTALACIÓN

### Paso 1: Instalar dependencias de Python

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
# Navegar a la carpeta database
cd database

# Instalar Flask y Flask-CORS
pip install flask flask-cors

# O si estás en Mac/Linux:
pip3 install flask flask-cors

# O usando el archivo requirements.txt:
pip install -r requirements.txt
```

### Paso 2: Verificar la base de datos

La base de datos `nova_style.db` ya debería existir en la carpeta `database/`. Si no existe, créala ejecutando:

```bash
python3 init_db.py
```

---

## 🎯 INICIAR EL SISTEMA

### IMPORTANTE: Siempre sigue estos pasos en orden

### 1️⃣ Iniciar el servidor API (OBLIGATORIO)

**En una terminal, ejecuta:**

```bash
# Asegúrate de estar en la carpeta database
cd database

# Iniciar el servidor API mejorado
python3 api_mejorada.py
```

**Deberías ver algo como esto:**
```
============================================================
🚀 API NOVA STYLE - PANEL DE ADMINISTRADOR
============================================================
📍 Servidor: http://127.0.0.1:5000
💾 Base de datos: /ruta/database/nova_style.db
============================================================

📋 Endpoints disponibles:
   GET    /api/health
   GET    /api/productos
   ...
============================================================

✅ Presiona Ctrl+C para detener el servidor

 * Running on http://127.0.0.1:5000
```

**⚠️ MANTÉN ESTA TERMINAL ABIERTA mientras uses el panel de administrador**

---

### 2️⃣ Abrir el Panel de Administrador

**Opción A - Panel Mejorado (Recomendado):**
1. Abre tu navegador
2. Navega a: `admin/admin_mejorado.html`
3. O arrastra el archivo `admin_mejorado.html` al navegador

**Opción B - Panel Original:**
1. Abre: `admin/admin.html`

---

## 📖 USO DEL PANEL

### Panel de Administrador Mejorado

El panel tiene 3 secciones principales:

#### 1. 📦 PRODUCTOS
**Agregar un producto:**
1. Completa los campos del formulario:
   - ✅ **Nombre** (requerido): "Camisa Polo"
   - ✅ **Precio** (requerido): 599.00
   - **Precio con Descuento** (opcional): 499.00
   - ✅ **Stock** (requerido): 50
   - ✅ **Referencia** (requerido): "NS-001"
   - ✅ **Categoría** (requerido): Selecciona de la lista
   - ✅ **Género** (requerido): Hombre/Mujer/Unisex
   - **Descripción** (opcional): Detalles del producto
   - **URL de Imagen** (opcional): https://ejemplo.com/imagen.jpg
   - **Estado**: Activo/Inactivo

2. Haz clic en **"💾 Guardar Producto"**
3. ¡El producto aparecerá en la tabla!

**Editar un producto:**
1. En la tabla de inventario, haz clic en **"✏️ Editar"**
2. El formulario se llenará con los datos del producto
3. Modifica lo que necesites
4. Haz clic en **"💾 Actualizar Producto"**
5. O **"❌ Cancelar"** para cancelar la edición

**Eliminar un producto:**
1. Haz clic en **"🗑️"** en la tabla
2. Confirma la eliminación
3. ⚠️ Esta acción no se puede deshacer

**Atajo de teclado:**
- `Ctrl + S`: Guardar producto rápidamente

---

#### 2. 📁 CATEGORÍAS
**Agregar una categoría:**
1. Ingresa el nombre: "Deportivo"
2. (Opcional) Agrega una descripción
3. (Opcional) URL de imagen representativa
4. Haz clic en **"💾 Guardar Categoría"**

**Ver categorías:**
- La tabla muestra todas las categorías
- Puedes ver cuántos productos tiene cada una

---

#### 3. 📊 ESTADÍSTICAS
**Información en tiempo real:**
- **Total Productos**: Productos activos en inventario
- **Sin Stock**: Productos con stock = 0
- **Categorías**: Total de categorías activas
- **Valor Inventario**: Suma del precio × stock de todos los productos
- **Agregados (7 días)**: Productos creados en la última semana

**Productos por Categoría:**
- Tabla que muestra la distribución de productos

**Actualizar datos:**
- Haz clic en **"🔄 Actualizar"** en el header

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se pudo conectar con el servidor"

**Problema:** El servidor API no está corriendo

**Solución:**
1. Abre una terminal
2. Ve a la carpeta `database`
3. Ejecuta: `python3 api_mejorada.py`
4. Recarga la página del panel

---

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

**Problema:** Flask no está instalado

**Solución:**
```bash
pip install flask flask-cors
# o
pip3 install flask flask-cors
```

---

### ❌ Los productos no aparecen en la tabla

**Problema:** Puede que no haya productos en la base de datos

**Solución:**
1. Ve al tab "Estadísticas"
2. Si dice "Total Productos: 0", agrega productos desde el tab "Productos"
3. Si hay productos pero no aparecen:
   - Verifica que el servidor API esté corriendo
   - Abre la consola del navegador (F12) y busca errores
   - Recarga la página (F5)

---

### ❌ Error al guardar producto: "Campos requeridos"

**Problema:** Faltan campos obligatorios

**Solución:**
Asegúrate de completar todos los campos marcados con **\***:
- Nombre
- Precio
- Stock
- Referencia
- Categoría
- Género

---

### ❌ Error de CORS

**Problema:** Restricciones de seguridad del navegador

**Solución:**
1. Verifica que el API esté corriendo en `http://127.0.0.1:5000`
2. El API ya tiene `flask-cors` configurado
3. Si persiste, asegúrate de que `flask-cors` esté instalado:
   ```bash
   pip install flask-cors
   ```

---

### ❌ La base de datos está vacía

**Problema:** No se inicializó la base de datos

**Solución:**
```bash
cd database
python3 init_db.py
```

Esto creará la base de datos con datos de ejemplo.

---

## 🎨 COMPARACIÓN DE VERSIONES

### Panel Original (`admin.html`)
✅ Funciones básicas CRUD
✅ Interfaz simple
❌ Solo maneja campos básicos (nombre, precio, stock, referencia)
❌ Sin categorías ni imágenes
❌ Sin estadísticas

### Panel Mejorado (`admin_mejorado.html`)
✅ **CRUD completo** con todos los campos
✅ **Gestión de categorías**
✅ **Estadísticas en tiempo real**
✅ **Interfaz con tabs**
✅ **Sistema de alertas**
✅ **Soporte para descuentos**
✅ **Gestión de imágenes**
✅ **Estados activo/inactivo**
✅ **Atajo de teclado (Ctrl+S)**

**Recomendación:** Usa el panel mejorado para mayor funcionalidad.

---

## 📝 FLUJO DE TRABAJO TÍPICO

### Configuración Inicial (Una sola vez):
1. ✅ Instalar Python 3
2. ✅ Instalar Flask: `pip install flask flask-cors`
3. ✅ Inicializar BD: `python3 init_db.py` (si no existe)

### Uso Diario:
1. **Iniciar servidor:**
   ```bash
   cd database
   python3 api_mejorada.py
   ```
   *(Dejar corriendo)*

2. **Abrir panel:**
   - Navegador → `admin/admin_mejorado.html`

3. **Trabajar:**
   - Agregar/editar/eliminar productos
   - Gestionar categorías
   - Ver estadísticas

4. **Al terminar:**
   - `Ctrl + C` en la terminal del servidor
   - Cerrar navegador

---

## 🔄 SINCRONIZACIÓN CON EL SITIO WEB

Los cambios que hagas en el panel de administrador se reflejarán **automáticamente** en:
- La base de datos (`nova_style.db`)
- Cualquier consulta a la API
- El sitio web (si está configurado para usar la API)

### Para que el sitio web use los datos:

**Opción 1 - Usar la API (Recomendado):**
```javascript
// En tus archivos JavaScript del sitio
fetch('http://127.0.0.1:5000/api/productos')
    .then(response => response.json())
    .then(productos => {
        // Mostrar productos
        console.log(productos);
    });
```

**Opción 2 - Exportar JSON:**
```bash
cd database
python3 db_queries.py
```
Esto generará `catalogo.json` que puedes usar en el sitio.

---

## 🆘 AYUDA ADICIONAL

### Logs y Debugging

**Ver logs del servidor:**
- La terminal donde corre `api_mejorada.py` muestra todas las peticiones
- Los errores aparecen ahí

**Ver logs del navegador:**
- Presiona `F12` → Consola
- Busca errores en rojo

**Verificar conexión manualmente:**
- Abre: `http://127.0.0.1:5000/api/health`
- Deberías ver: `{"status": "ok", ...}`

---

## 📞 CONTACTO Y SOPORTE

Si encuentras algún problema:
1. Revisa esta guía de solución de problemas
2. Verifica que el servidor esté corriendo
3. Revisa la consola del navegador (F12)
4. Verifica los logs del servidor en la terminal

---

## ✨ CARACTERÍSTICAS ADICIONALES

### API Endpoints Disponibles:

```
GET    /api/health                    - Estado del servidor
GET    /api/productos                 - Todos los productos
GET    /api/productos/<id>            - Producto específico
POST   /api/productos                 - Crear producto
PUT    /api/productos/<id>            - Actualizar producto
DELETE /api/productos/<id>            - Eliminar producto
GET    /api/categorias                - Todas las categorías
POST   /api/categorias                - Crear categoría
GET    /api/tallas                    - Todas las tallas
GET    /api/colores                   - Todos los colores
GET    /api/estadisticas              - Estadísticas generales
```

Puedes usar estos endpoints en tu propio código para crear funcionalidades personalizadas.

---

**¡Listo! 🎉 Tu panel de administrador está completamente funcional.**

**Recuerda:**
1. Siempre iniciar el servidor API primero
2. Mantener la terminal del servidor abierta
3. Usar el panel mejorado para más funcionalidades

---

**Versión:** 2.0  
**Fecha:** Febrero 2026  
**Nova Style Team**
