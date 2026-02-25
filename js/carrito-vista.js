// Mostrar carrito en la página

function mostrarCarrito() {
    const container = document.getElementById('carrito-items-container');
    
    if (!container) return;
    
    console.log('Carrito items:', carrito.items); // Para debug
    
    if (carrito.items.length === 0) {
        container.innerHTML = `
            <div class="carrito-vacio">
                <h2>Tu carrito está vacío</h2>
                <p>¿Qué esperas? ¡Empieza a comprar!</p>
            </div>
        `;
        actualizarTotales();
        return;
    }

    container.innerHTML = carrito.items.map(item => `
        <div class="item-carrito">
            <img src="${item.imagen}" alt="${item.nombre}" class="item-imagen" onerror="this.src='https://via.placeholder.com/120x150?text=Sin+imagen'">
            <div class="item-info">
                <div class="item-nombre">${item.nombre}</div>
                <div class="item-descripcion">${item.descripcion || 'Sin descripción'}</div>
                <div class="item-precio">MXN ${parseInt(item.precio).toLocaleString()}</div>
                <div class="item-acciones">
                    <div class="cantidad-control">
                        <button onclick="actualizarCantidad(${item.id}, ${item.cantidad - 1})">−</button>
                        <input type="number" value="${item.cantidad}" readonly>
                        <button onclick="actualizarCantidad(${item.id}, ${item.cantidad + 1})">+</button>
                    </div>
                    <button class="btn-eliminar" onclick="eliminarDelCarrito(${item.id})">Eliminar</button>
                </div>
            </div>
            <div style="text-align: right; min-width: 100px;">
                <strong>MXN ${parseInt(item.precio * item.cantidad).toLocaleString()}</strong>
            </div>
        </div>
    `).join('');

    actualizarTotales();
}

function actualizarCantidad(id, cantidad) {
    if (cantidad <= 0) {
        eliminarDelCarrito(id);
    } else {
        carrito.actualizarCantidad(id, cantidad);
        mostrarCarrito();
    }
}

function eliminarDelCarrito(id) {
    carrito.eliminarProducto(id);
    mostrarCarrito();
}

function actualizarTotales() {
    const subtotal = carrito.obtenerTotal();
    const envio = subtotal >= 500 ? 0 : 100;
    const total = subtotal + envio;
    
    const subtotalElement = document.getElementById('subtotal');
    const envioElement = document.getElementById('envio');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) subtotalElement.textContent = `MXN ${parseInt(subtotal).toLocaleString()}`;
    if (envioElement) envioElement.textContent = envio === 0 ? 'GRATIS' : `MXN ${envio}`;
    if (totalElement) totalElement.textContent = `MXN ${parseInt(total).toLocaleString()}`;
}

function vaciarCarrito() {
    if (confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
        carrito.vaciarCarrito();
        mostrarCarrito();
    }
}

function finalizarCompra() {
    if (carrito.items.length === 0) {
        alert('Tu carrito está vacío');
        return;
    }
    
    const total = carrito.obtenerTotal();
    const confirmar = confirm(`¿Confirmar compra por MXN ${parseInt(total).toLocaleString()}?`);
    
    if (confirmar) {
        alert('¡Compra realizada exitosamente! Gracias por tu compra.');
        carrito.vaciarCarrito();
        mostrarCarrito();
        setTimeout(() => location.href = 'index.html', 1000);
    }
}

// Mostrar carrito al cargar la página
window.addEventListener('load', mostrarCarrito);
document.addEventListener('DOMContentLoaded', mostrarCarrito);