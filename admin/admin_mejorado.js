// Configuración de la API
const API_URL = 'http://127.0.0.1:5000/api';

// Variable global para modo edición
let modoEdicion = false;
let idProductoEdicion = null;

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Panel de administración inicializado');
    verificarConexionAPI();
    cargarCategorias();
    cargarProductos();
    cargarEstadisticas();
});

// ============================================
// VERIFICACIÓN DE CONEXIÓN
// ============================================

async function verificarConexionAPI() {
    try {
        const respuesta = await fetch(`${API_URL}/health`);
        const data = await respuesta.json();
        
        if (data.status === 'ok') {
            mostrarAlerta('Conexión con la base de datos establecida ✅', 'success');
            console.log('✅ API conectada:', data);
        }
    } catch (error) {
        mostrarAlerta('⚠️ No se pudo conectar con el servidor. Asegúrate de ejecutar: python3 database/api_mejorada.py', 'error');
        console.error('❌ Error de conexión:', error);
    }
}

// ============================================
// GESTIÓN DE TABS
// ============================================

function cambiarTab(tabName) {
    // Ocultar todos los tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remover clase active de todos los botones
    document.querySelectorAll('.tab').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Activar el tab seleccionado
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Cargar datos según el tab
    if (tabName === 'categorias') {
        cargarCategoriasTabla();
    } else if (tabName === 'estadisticas') {
        cargarEstadisticas();
    }
}

// ============================================
// ALERTAS
// ============================================

function mostrarAlerta(mensaje, tipo = 'info') {
    const container = document.getElementById('alertContainer');
    const alerta = document.createElement('div');
    alerta.className = `alert alert-${tipo}`;
    alerta.textContent = mensaje;
    
    container.innerHTML = '';
    container.appendChild(alerta);
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        alerta.remove();
    }, 5000);
}

// ============================================
// PRODUCTOS
// ============================================

async function cargarProductos() {
    const tabla = document.getElementById('cuerpo-tabla');
    
    try {
        const respuesta = await fetch(`${API_URL}/productos`);
        const productos = await respuesta.json();
        
        tabla.innerHTML = '';
        
        if (productos.length === 0) {
            tabla.innerHTML = '<tr><td colspan="8" style="text-align:center;">No hay productos en el inventario.</td></tr>';
            return;
        }
        
        productos.forEach(p => {
            const fila = document.createElement('tr');
            const estadoBadge = p.activo 
                ? '<span class="status-badge status-activo">Activo</span>'
                : '<span class="status-badge status-inactivo">Inactivo</span>';
            
            const precioMostrar = p.precio_descuento 
                ? `<s style="color: #95a5a6;">$${p.precio}</s> <span style="color: #e74c3c; font-weight: bold;">$${p.precio_descuento}</span>`
                : `$${p.precio}`;
            
            fila.innerHTML = `
                <td>${p.id_producto}</td>
                <td><strong>${p.nombre}</strong></td>
                <td>${p.categoria_nombre || 'Sin categoría'}</td>
                <td>${precioMostrar}</td>
                <td>${p.stock > 0 ? p.stock : '<span style="color: #e74c3c;">Sin stock</span>'}</td>
                <td><code>${p.referencia}</code></td>
                <td>${estadoBadge}</td>
                <td>
                    <button class="btn-edit btn-small" onclick="prepararEdicion(${p.id_producto})">✏️ Editar</button>
                    <button class="btn-delete btn-small" onclick="eliminarProducto(${p.id_producto})">🗑️</button>
                </td>
            `;
            tabla.appendChild(fila);
        });
        
    } catch (error) {
        console.error('Error al cargar productos:', error);
        tabla.innerHTML = '<tr><td colspan="8" style="text-align:center; color: #e74c3c;">Error al cargar productos</td></tr>';
    }
}

async function guardarProducto() {
    // Validar campos requeridos
    const campos = {
        nombre: document.getElementById('nombre').value.trim(),
        precio: document.getElementById('precio').value,
        stock: document.getElementById('stock').value,
        referencia: document.getElementById('referencia').value.trim(),
        id_categoria: document.getElementById('categoria').value,
        genero: document.getElementById('genero').value
    };
    
    if (!campos.nombre || !campos.precio || !campos.referencia || !campos.id_categoria) {
        mostrarAlerta('❌ Por favor completa todos los campos requeridos (*)', 'error');
        return;
    }
    
    // Preparar datos del producto
    const nuevoProducto = {
        nombre: campos.nombre,
        descripcion: document.getElementById('descripcion').value.trim(),
        precio: parseFloat(campos.precio),
        precio_descuento: document.getElementById('precio_descuento').value 
            ? parseFloat(document.getElementById('precio_descuento').value) 
            : null,
        stock: parseInt(campos.stock) || 0,
        referencia: campos.referencia,
        id_categoria: parseInt(campos.id_categoria),
        genero: campos.genero,
        activo: parseInt(document.getElementById('activo').value)
    };
    
    // Agregar imagen si existe
    const imagenUrl = document.getElementById('imagen_url').value.trim();
    if (imagenUrl) {
        nuevoProducto.imagenes = [imagenUrl];
    }
    
    try {
        let respuesta;
        
        if (modoEdicion) {
            // Actualizar producto existente
            respuesta = await fetch(`${API_URL}/productos/${idProductoEdicion}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(nuevoProducto)
            });
        } else {
            // Crear nuevo producto
            respuesta = await fetch(`${API_URL}/productos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(nuevoProducto)
            });
        }
        
        if (respuesta.ok) {
            const mensaje = modoEdicion 
                ? '✅ Producto actualizado exitosamente' 
                : '✅ Producto creado exitosamente';
            mostrarAlerta(mensaje, 'success');
            
            limpiarFormulario();
            cancelarEdicion();
            cargarProductos();
            cargarEstadisticas();
        } else {
            const error = await respuesta.json();
            mostrarAlerta(`❌ Error: ${error.error}`, 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('❌ Error de conexión con el servidor', 'error');
    }
}

async function prepararEdicion(id) {
    try {
        const respuesta = await fetch(`${API_URL}/productos/${id}`);
        const producto = await respuesta.json();
        
        // Llenar el formulario
        document.getElementById('nombre').value = producto.nombre;
        document.getElementById('descripcion').value = producto.descripcion || '';
        document.getElementById('precio').value = producto.precio;
        document.getElementById('precio_descuento').value = producto.precio_descuento || '';
        document.getElementById('stock').value = producto.stock;
        document.getElementById('referencia').value = producto.referencia;
        document.getElementById('categoria').value = producto.id_categoria || '';
        document.getElementById('genero').value = producto.genero;
        document.getElementById('activo').value = producto.activo ? 1 : 0;
        
        // Cargar imagen principal si existe
        if (producto.imagenes && producto.imagenes.length > 0) {
            const imagenPrincipal = producto.imagenes.find(img => img.es_principal) || producto.imagenes[0];
            document.getElementById('imagen_url').value = imagenPrincipal.url_imagen;
        }
        
        // Cambiar a modo edición
        modoEdicion = true;
        idProductoEdicion = id;
        
        // Actualizar UI
        document.getElementById('form-titulo').textContent = '✏️ Editar Producto';
        document.getElementById('btn-guardar').textContent = '💾 Actualizar Producto';
        document.getElementById('btn-guardar').style.backgroundColor = '#f39c12';
        document.getElementById('btn-cancelar').style.display = 'inline-block';
        
        // Scroll al formulario
        document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
        
        mostrarAlerta('📝 Modo edición activado', 'info');
        
    } catch (error) {
        console.error('Error al cargar producto:', error);
        mostrarAlerta('❌ Error al cargar los datos del producto', 'error');
    }
}

function cancelarEdicion() {
    modoEdicion = false;
    idProductoEdicion = null;
    
    document.getElementById('form-titulo').textContent = '➕ Agregar Nuevo Producto';
    document.getElementById('btn-guardar').textContent = '💾 Guardar Producto';
    document.getElementById('btn-guardar').style.backgroundColor = '#27ae60';
    document.getElementById('btn-cancelar').style.display = 'none';
    
    limpiarFormulario();
}

async function eliminarProducto(id) {
    if (!confirm('⚠️ ¿Estás seguro de eliminar este producto? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        const respuesta = await fetch(`${API_URL}/productos/${id}`, {
            method: 'DELETE'
        });
        
        if (respuesta.ok) {
            mostrarAlerta('✅ Producto eliminado exitosamente', 'success');
            cargarProductos();
            cargarEstadisticas();
        } else {
            mostrarAlerta('❌ Error al eliminar el producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('❌ Error de conexión', 'error');
    }
}

function limpiarFormulario() {
    document.getElementById('nombre').value = '';
    document.getElementById('descripcion').value = '';
    document.getElementById('precio').value = '';
    document.getElementById('precio_descuento').value = '';
    document.getElementById('stock').value = '';
    document.getElementById('referencia').value = '';
    document.getElementById('categoria').value = '';
    document.getElementById('genero').value = 'unisex';
    document.getElementById('activo').value = '1';
    document.getElementById('imagen_url').value = '';
}

// ============================================
// CATEGORÍAS
// ============================================

async function cargarCategorias() {
    const select = document.getElementById('categoria');
    
    try {
        const respuesta = await fetch(`${API_URL}/categorias`);
        const categorias = await respuesta.json();
        
        select.innerHTML = '<option value="">Seleccionar categoría...</option>';
        
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id_categoria;
            option.textContent = cat.nombre;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error al cargar categorías:', error);
    }
}

async function cargarCategoriasTabla() {
    const tabla = document.getElementById('tabla-categorias');
    
    try {
        const respuesta = await fetch(`${API_URL}/categorias`);
        const categorias = await respuesta.json();
        
        // También necesitamos los productos para contar
        const respProductos = await fetch(`${API_URL}/productos`);
        const productos = await respProductos.json();
        
        tabla.innerHTML = '';
        
        categorias.forEach(cat => {
            const cantidadProductos = productos.filter(p => p.id_categoria === cat.id_categoria).length;
            
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${cat.id_categoria}</td>
                <td><strong>${cat.nombre}</strong></td>
                <td>${cat.descripcion || 'Sin descripción'}</td>
                <td>${cantidadProductos} productos</td>
            `;
            tabla.appendChild(fila);
        });
        
    } catch (error) {
        console.error('Error:', error);
        tabla.innerHTML = '<tr><td colspan="4" style="text-align:center; color: #e74c3c;">Error al cargar categorías</td></tr>';
    }
}

async function agregarCategoria() {
    const nombre = document.getElementById('cat-nombre').value.trim();
    const descripcion = document.getElementById('cat-descripcion').value.trim();
    const imagen = document.getElementById('cat-imagen').value.trim();
    
    if (!nombre) {
        mostrarAlerta('❌ El nombre de la categoría es requerido', 'error');
        return;
    }
    
    try {
        const respuesta = await fetch(`${API_URL}/categorias`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre,
                descripcion,
                imagen_url: imagen
            })
        });
        
        if (respuesta.ok) {
            mostrarAlerta('✅ Categoría creada exitosamente', 'success');
            document.getElementById('cat-nombre').value = '';
            document.getElementById('cat-descripcion').value = '';
            document.getElementById('cat-imagen').value = '';
            cargarCategorias();
            cargarCategoriasTabla();
        } else {
            const error = await respuesta.json();
            mostrarAlerta(`❌ Error: ${error.error}`, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('❌ Error de conexión', 'error');
    }
}

// ============================================
// ESTADÍSTICAS
// ============================================

async function cargarEstadisticas() {
    try {
        const respuesta = await fetch(`${API_URL}/estadisticas`);
        const stats = await respuesta.json();
        
        // Actualizar tarjetas de estadísticas
        document.getElementById('stat-total').textContent = stats.total_productos;
        document.getElementById('stat-sin-stock').textContent = stats.productos_sin_stock;
        document.getElementById('stat-categorias').textContent = stats.total_categorias;
        document.getElementById('stat-valor').textContent = `$${stats.valor_inventario.toLocaleString('es-MX')}`;
        document.getElementById('stat-recientes').textContent = stats.productos_recientes;
        
        // Actualizar tabla de productos por categoría
        const tabla = document.getElementById('tabla-stats-categorias');
        tabla.innerHTML = '';
        
        if (stats.por_categoria && stats.por_categoria.length > 0) {
            stats.por_categoria.forEach(cat => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td><strong>${cat.nombre}</strong></td>
                    <td>${cat.total} productos</td>
                `;
                tabla.appendChild(fila);
            });
        } else {
            tabla.innerHTML = '<tr><td colspan="2" style="text-align:center;">No hay datos disponibles</td></tr>';
        }
        
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

// ============================================
// UTILIDADES
// ============================================

// Auto-guardar al presionar Ctrl+S
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        guardarProducto();
    }
});

// Log de inicialización
console.log('%c🛍️ Nova Style Admin Panel', 'color: #27ae60; font-size: 20px; font-weight: bold;');
console.log('%cAPI URL:', 'font-weight: bold;', API_URL);
