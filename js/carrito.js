// Sistema de carrito con localStorage

class Carrito {
    constructor() {
        this.items = this.cargarCarrito();
    }

    // Cargar carrito desde localStorage
    cargarCarrito() {
        const saved = localStorage.getItem('carrito');
        return saved ? JSON.parse(saved) : [];
    }

    // Guardar carrito en localStorage
    guardarCarrito() {
        localStorage.setItem('carrito', JSON.stringify(this.items));
    }

    // Agregar producto al carrito
    agregarProducto(id, nombre, precio, imagen, cantidad = 1) {
        const existe = this.items.find(item => item.id === id);
        
        if (existe) {
            existe.cantidad += cantidad;
        } else {
            this.items.push({ id, nombre, precio, imagen, cantidad });
        }
        
        this.guardarCarrito();
        this.mostrarNotificacion(`${nombre} agregado al carrito`);
    }

    // Eliminar producto del carrito
    eliminarProducto(id) {
        this.items = this.items.filter(item => item.id !== id);
        this.guardarCarrito();
    }

    // Actualizar cantidad
    actualizarCantidad(id, cantidad) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            item.cantidad = cantidad;
            if (item.cantidad <= 0) {
                this.eliminarProducto(id);
            } else {
                this.guardarCarrito();
            }
        }
    }

    // Obtener total
    obtenerTotal() {
        return this.items.reduce((total, item) => total + (item.precio * item.cantidad), 0);
    }

    // Obtener cantidad de items
    obtenerCantidadItems() {
        return this.items.reduce((total, item) => total + item.cantidad, 0);
    }

    // Vaciar carrito
    vaciarCarrito() {
        this.items = [];
        this.guardarCarrito();
    }

    // Mostrar notificación
    mostrarNotificacion(mensaje) {
        const notif = document.createElement('div');
        notif.textContent = mensaje;
        notif.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(notif);
        
        setTimeout(() => notif.remove(), 3000);
    }
}

// Crear instancia global
const carrito = new Carrito();