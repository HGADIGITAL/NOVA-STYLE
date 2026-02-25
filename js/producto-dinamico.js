let productoActual = null;
let tallaSeleccionada = null;
let colorSeleccionado = null;

// Obtener ID del producto desde la URL
function obtenerIdProducto() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id')) || 1;
}

// Cargar catálogo y mostrar producto
async function cargarProducto() {
    try {
        const response = await fetch('../database/catalogo.json');
        const catalogo = await response.json();
        const idProducto = obtenerIdProducto();
        
        productoActual = catalogo.find(p => p.id_producto === idProducto);
        
        if (!productoActual) {
            document.querySelector('.container').innerHTML = '<p>Producto no encontrado</p>';
            return;
        }
        
        mostrarProducto();
    } catch (error) {
        console.error('Error cargando catálogo:', error);
    }
}

function mostrarProducto() {
    const imagenPrincipal = productoActual.imagenes[0]?.url_imagen || '';
    
    // Mostrar imágenes
    document.getElementById('images-container').innerHTML = productoActual.imagenes
        .map(img => `<img src="${img.url_imagen}" alt="${productoActual.nombre}" onclick="cambiarImagenPrincipal(this.src)">`)
        .join('');
    
    // Mostrar detalles del producto
    const precioMostrar = productoActual.precio_descuento || productoActual.precio;
    const html = `
        <h1 class="product-title">${productoActual.nombre.toUpperCase()}</h1>
        <p class="price">MXN ${precioMostrar.toLocaleString()}</p>
        <p>${productoActual.descripcion}</p>
        <p>REF. ${productoActual.referencia}</p>
        
        ${productoActual.tallas.length > 0 ? `
            <div class="selector">
                <label>Talla:</label>
                <select id="talla-select" onchange="tallaSeleccionada = this.value">
                    <option value="">Seleccionar talla</option>
                    ${productoActual.tallas.map(t => `<option value="${t.nombre}">${t.nombre}</option>`).join('')}
                </select>
            </div>
        ` : ''}
        
        ${productoActual.colores.length > 0 ? `
            <div class="selector">
                <label>Color:</label>
                <select id="color-select" onchange="colorSeleccionado = this.value">
                    <option value="">Seleccionar color</option>
                    ${productoActual.colores.map(c => `<option value="${c.nombre}">${c.nombre}</option>`).join('')}
                </select>
            </div>
        ` : ''}
        
        <button class="button" onclick="agregarAlCarrito()">AÑADIR A LA CESTA</button>
        <div class="info-box">COMPOSICIÓN, CUIDADOS Y ORIGEN</div>
        <div class="info-box">DISPONIBILIDAD EN TIENDA</div>
        <div class="info-box">ENVÍOS Y DEVOLUCIONES</div>
        <div class="info-box free-shipping">ENVÍO A DOMICILIO - GRATIS</div>
    `;
    
    document.getElementById('product-details').innerHTML = html;
}

function cambiarImagenPrincipal(src) {
    const imagenesContainer = document.getElementById('images-container');
    const imagenes = imagenesContainer.querySelectorAll('img');
    imagenes.forEach(img => {
        if (img.src === src) {
            img.style.border = '2px solid black';
        } else {
            img.style.border = 'none';
        }
    });
}

function actualizarContadorCarrito() {
    const cantidad = carrito.obtenerCantidadItems();
    const elemento = document.getElementById('cantidad-carrito');
    if (elemento) {
        elemento.textContent = cantidad;
    }
}

function irAlCarrito() {
    window.location.href = 'carrito.html';
}

function agregarAlCarrito() {
    if (productoActual.tallas.length > 0 && !tallaSeleccionada) {
        alert('Por favor selecciona una talla');
        return;
    }
    
    const imagenPrincipal = productoActual.imagenes[0]?.url_imagen || '';
    const precio = productoActual.precio_descuento || productoActual.precio;
    
    const descripcion = `${productoActual.nombre}${tallaSeleccionada ? ` - Talla ${tallaSeleccionada}` : ''}${colorSeleccionado ? ` - ${colorSeleccionado}` : ''}`;
    
    carrito.agregarProducto(
        productoActual.id_producto,
        descripcion,
        precio,
        imagenPrincipal,
        1
    );
    
    // Mostrar preview en sidebar
    document.getElementById('cart-preview').innerHTML = `
        <img src="${imagenPrincipal}" alt="${productoActual.nombre}" style="max-width: 100%; border-radius: 4px;">
        <p>
            <strong>MXN ${precio.toLocaleString()}</strong><br>
            ${descripcion}
        </p>
    `;
    
    // Actualizar contador
    actualizarContadorCarrito();
    
    toggleSidebar();
}

function toggleSidebar() {
    document.getElementById('cart-sidebar').classList.toggle('active');
}

function toggleDropdown(sectionId) {
    const sections = document.querySelectorAll('.dropdown-section');
    sections.forEach((section) => {
        if (section.id !== sectionId) {
            section.classList.remove('active');
        }
    });
    
    const section = document.getElementById(sectionId);
    section.classList.toggle('active');
}

// Cargar producto al abrir la página
document.addEventListener('DOMContentLoaded', function() {
    cargarProducto();
    actualizarContadorCarrito(); // Mostrar contador al cargar
});