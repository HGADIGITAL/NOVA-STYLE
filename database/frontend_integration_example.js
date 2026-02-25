// ================================================
// EJEMPLO DE INTEGRACIÓN CON FRONTEND
// Archivo: js/db_integration.js
// ================================================

/**
 * Módulo para conectar el frontend con la base de datos
 * Puede usar el archivo JSON o la API REST
 */

class NovaStyleAPI {
    constructor(useAPI = false) {
        this.useAPI = useAPI;
        this.apiURL = 'http://localhost:5000/api';
        this.jsonFile = 'database/catalogo.json';
        this.productos = [];
    }

    // ==================== CARGAR DATOS ====================

    async cargarProductos() {
        try {
            if (this.useAPI) {
                const response = await fetch(`${this.apiURL}/productos`);
                const data = await response.json();
                this.productos = data.data;
            } else {
                const response = await fetch(this.jsonFile);
                this.productos = await response.json();
            }
            return this.productos;
        } catch (error) {
            console.error('Error al cargar productos:', error);
            return [];
        }
    }

    // ==================== PRODUCTOS ====================

    async obtenerTodosProductos() {
        if (this.productos.length === 0) {
            await this.cargarProductos();
        }
        return this.productos;
    }

    async obtenerProductoPorId(id) {
        if (this.useAPI) {
            const response = await fetch(`${this.apiURL}/productos/${id}`);
            const data = await response.json();
            return data.data;
        } else {
            if (this.productos.length === 0) {
                await this.cargarProductos();
            }
            return this.productos.find(p => p.id_producto === id);
        }
    }

    async obtenerProductosPorCategoria(categoria) {
        if (this.useAPI) {
            const response = await fetch(`${this.apiURL}/productos/categoria/${categoria}`);
            const data = await response.json();
            return data.data;
        } else {
            if (this.productos.length === 0) {
                await this.cargarProductos();
            }
            return this.productos.filter(p => p.categoria_nombre === categoria);
        }
    }

    async buscarProductos(termino) {
        if (this.useAPI) {
            const response = await fetch(`${this.apiURL}/productos/buscar?q=${termino}`);
            const data = await response.json();
            return data.data;
        } else {
            if (this.productos.length === 0) {
                await this.cargarProductos();
            }
            return this.productos.filter(p => 
                p.nombre.toLowerCase().includes(termino.toLowerCase()) ||
                p.descripcion.toLowerCase().includes(termino.toLowerCase())
            );
        }
    }

    // ==================== CARRITO (solo con API) ====================

    async agregarAlCarrito(idUsuario, idProducto, talla = null, color = null, cantidad = 1) {
        if (!this.useAPI) {
            console.error('El carrito requiere usar la API');
            return false;
        }

        try {
            const response = await fetch(`${this.apiURL}/carrito`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id_usuario: idUsuario,
                    id_producto: idProducto,
                    id_talla: talla,
                    id_color: color,
                    cantidad: cantidad
                })
            });
            const data = await response.json();
            return data.success;
        } catch (error) {
            console.error('Error al agregar al carrito:', error);
            return false;
        }
    }

    async obtenerCarrito(idUsuario) {
        if (!this.useAPI) {
            console.error('El carrito requiere usar la API');
            return [];
        }

        try {
            const response = await fetch(`${this.apiURL}/carrito/${idUsuario}`);
            const data = await response.json();
            return data.data;
        } catch (error) {
            console.error('Error al obtener carrito:', error);
            return [];
        }
    }

    // ==================== RENDERIZADO ====================

    renderizarProducto(producto, contenedor) {
        const productoHTML = `
            <div class="producto" onclick="verDetalleProducto(${producto.id_producto})">
                <img src="${producto.imagen_principal || producto.imagenes[0].url_imagen}" 
                     alt="${producto.nombre}">
                <h3>${producto.nombre}</h3>
                <p>$${producto.precio.toFixed(2)}</p>
                <a href="#" class="boton-comprar" 
                   onclick="agregarAlCarrito(${producto.id_producto}); return false;">
                    Comprar
                </a>
            </div>
        `;
        contenedor.innerHTML += productoHTML;
    }

    renderizarCatalogo(productos, contenedorId) {
        const contenedor = document.getElementById(contenedorId);
        if (!contenedor) return;

        contenedor.innerHTML = '';
        productos.forEach(producto => {
            this.renderizarProducto(producto, contenedor);
        });
    }
}

// ================================================
// FUNCIONES GLOBALES PARA USO EN HTML
// ================================================

// Instancia global de la API
const api = new NovaStyleAPI(false); // true para usar API REST

// Cargar productos al iniciar
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Cargando catálogo...');
    await api.cargarProductos();
    console.log('Productos cargados:', api.productos.length);
});

// Función para mostrar productos de una categoría
async function mostrarCategoria(categoria) {
    const productos = await api.obtenerProductosPorCategoria(categoria);
    api.renderizarCatalogo(productos, 'catalogo');
}

// Función para buscar productos
async function buscarProductos(termino) {
    const productos = await api.buscarProductos(termino);
    api.renderizarCatalogo(productos, 'catalogo');
}

// Función para ver detalle de producto
async function verDetalleProducto(id) {
    const producto = await api.obtenerProductoPorId(id);
    
    // Aquí puedes mostrar el producto en un modal o redirigir a página de detalle
    console.log('Producto:', producto);
    
    // Ejemplo: redirigir a página de producto
    window.location.href = `html/producto.html?id=${id}`;
}

// Función para agregar al carrito
async function agregarAlCarrito(idProducto) {
    const idUsuario = 1; // ID del usuario (obtener de sesión)
    
    if (api.useAPI) {
        const success = await api.agregarAlCarrito(idUsuario, idProducto);
        if (success) {
            alert('Producto agregado al carrito');
            // Actualizar contador del carrito
            actualizarContadorCarrito();
        }
    } else {
        // Si no usamos API, usar localStorage
        let carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
        carrito.push({
            id_producto: idProducto,
            cantidad: 1,
            fecha: new Date()
        });
        localStorage.setItem('carrito', JSON.stringify(carrito));
        alert('Producto agregado al carrito');
    }
}

// Función para actualizar contador del carrito
async function actualizarContadorCarrito() {
    const idUsuario = 1;
    
    if (api.useAPI) {
        const items = await api.obtenerCarrito(idUsuario);
        document.getElementById('contador-carrito').textContent = items.length;
    } else {
        const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
        const contador = document.getElementById('contador-carrito');
        if (contador) {
            contador.textContent = carrito.length;
        }
    }
}

// ================================================
// EJEMPLO DE USO EN PÁGINA DE CATÁLOGO
// ================================================

/*
HTML EJEMPLO:

<section id="catalogo" class="catalogo">
    <!-- Los productos se cargarán aquí -->
</section>

<script>
    // Cargar productos de hombre al cargar la página
    document.addEventListener('DOMContentLoaded', async () => {
        await mostrarCategoria('Hombre');
    });
</script>
*/

// ================================================
// EJEMPLO DE USO CON BÚSQUEDA
// ================================================

/*
HTML EJEMPLO:

<input type="text" id="busqueda" placeholder="Buscar productos...">
<button onclick="realizarBusqueda()">Buscar</button>

<script>
    function realizarBusqueda() {
        const termino = document.getElementById('busqueda').value;
        buscarProductos(termino);
    }
    
    // Búsqueda en tiempo real
    document.getElementById('busqueda').addEventListener('input', (e) => {
        if (e.target.value.length > 2) {
            buscarProductos(e.target.value);
        }
    });
</script>
*/
