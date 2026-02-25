document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
});

// 1. FUNCIÓN PARA MOSTRAR LOS PRODUCTOS EN LA TABLA
async function cargarProductos() {
    const tabla = document.getElementById('cuerpo-tabla');
    try {
        const respuesta = await fetch('http://127.0.0.1:5000/api/productos');
        const productos = await respuesta.json();

        tabla.innerHTML = ''; // Limpiar tabla antes de llenar

        if (productos.length === 0) {
            tabla.innerHTML = '<tr><td colspan="6" style="text-align:center;">No hay productos en el inventario.</td></tr>';
            return;
        }

        productos.forEach(p => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${p.id_producto}</td>
                <td>${p.nombre}</td>
                <td>$${p.precio}</td>
                <td>${p.stock}</td>
                <td>${p.referencia}</td>
                <td>
                    <button class="btn-edit" onclick="prepararEdicion(${p.id_producto}, '${p.nombre}', ${p.precio}, ${p.stock}, '${p.referencia}')">✏️ Editar</button>
                    <button class="btn-delete" onclick="eliminarProducto(${p.id_producto})">🗑️ Borrar</button>
                </td>
            `;
            tabla.appendChild(fila);
        });
    } catch (error) {
        console.error("Error al cargar:", error);
    }
}

// 2. FUNCIÓN PARA AGREGAR UN NUEVO PRODUCTO
async function agregarProducto() {
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const stock = document.getElementById('stock').value;
    const referencia = document.getElementById('referencia').value;

    if (!nombre || !precio || !stock || !referencia) {
        alert("Héctor, completa todos los campos para continuar.");
        return;
    }

    const nuevoP = { nombre, precio, stock, referencia };

    try {
        const respuesta = await fetch('http://127.0.0.1:5000/api/productos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevoP)
        });

        if (respuesta.ok) {
            alert("¡Producto guardado!");
            limpiarFormulario();
            cargarProductos();
        }
    } catch (error) {
        alert("Error de conexión con el servidor.");
    }
}

// 3. FUNCIÓN PARA ELIMINAR UN PRODUCTO
async function eliminarProducto(id) {
    if (confirm("¿Estás seguro de que quieres eliminar este producto de Nova Style?")) {
        try {
            const respuesta = await fetch(`http://127.0.0.1:5000/api/productos/${id}`, {
                method: 'DELETE'
            });

            if (respuesta.ok) {
                cargarProductos(); // Refrescar tabla
            }
        } catch (error) {
            alert("No se pudo eliminar el producto.");
        }
    }
}

// 4. PREPARAR EL FORMULARIO PARA EDITAR
function prepararEdicion(id, nombre, precio, stock, referencia) {
    // Subimos los datos al formulario
    document.getElementById('nombre').value = nombre;
    document.getElementById('precio').value = precio;
    document.getElementById('stock').value = stock;
    document.getElementById('referencia').value = referencia;

    // Cambiamos el botón principal para que sea de "Actualizar"
    const btnContainer = document.querySelector('.form-container');
    const btnOriginal = btnContainer.querySelector('.btn-principal');
    
    btnOriginal.innerText = "💾 ACTUALIZAR PRODUCTO";
    btnOriginal.style.backgroundColor = "#ffc107"; // Color naranja para distinguir
    btnOriginal.onclick = () => ejecutarActualizacion(id);
}

// 5. EJECUTAR LA ACTUALIZACIÓN EN LA BASE DE DATOS
async function ejecutarActualizacion(id) {
    const datosEditados = {
        nombre: document.getElementById('nombre').value,
        precio: document.getElementById('precio').value,
        stock: document.getElementById('stock').value,
        referencia: document.getElementById('referencia').value
    };

    try {
        const respuesta = await fetch(`http://127.0.0.1:5000/api/productos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datosEditados)
        });

        if (respuesta.ok) {
            alert("Producto actualizado correctamente.");
            resetearBoton();
            limpiarFormulario();
            cargarProductos();
        }
    } catch (error) {
        alert("Error al actualizar.");
    }
}

// FUNCIONES DE APOYO (Limpieza)
function limpiarFormulario() {
    document.getElementById('nombre').value = '';
    document.getElementById('precio').value = '';
    document.getElementById('stock').value = '';
    document.getElementById('referencia').value = '';
}

function resetearBoton() {
    const btn = document.querySelector('.btn-principal');
    btn.innerText = "Guardar en Inventario";
    btn.style.backgroundColor = "#27ae60"; // Volver al verde original
    btn.onclick = agregarProducto;
}