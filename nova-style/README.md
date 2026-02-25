# Nova Style - E-commerce Website

## Estructura del Proyecto

```
nova-style/
│
├── index.html              # Página principal
│
├── css/                    # Archivos CSS
│   ├── index.css          # Estilos para la página principal
│   ├── catalogo.css       # Estilos compartidos para páginas de catálogo
│   ├── producto.css       # Estilos para páginas de producto individual
│   ├── iaou.css           # Estilos para la página de IA
│   └── micuenta.css       # Estilos para Mi Cuenta
│
├── js/                     # Archivos JavaScript
│   ├── index.js           # JavaScript para la página principal
│   ├── catalogo.js        # JavaScript para páginas de catálogo
│   ├── producto.js        # JavaScript para páginas de producto
│   └── iaou.js            # JavaScript para la página de IA
│
├── html/                   # Páginas HTML secundarias
│   ├── hombre.html        # Catálogo de ropa para hombre
│   ├── mujer.html         # Catálogo de ropa para mujer
│   ├── calzado.html       # Catálogo de calzado
│   ├── accesorios.html    # Catálogo de accesorios
│   ├── patang.html        # Producto: Pantalón Negro
│   ├── balle.html         # Producto: Pantalón Balloon
│   ├── colla.html         # Producto: Collar
│   ├── Zapatillaska.html  # Producto: Zapatillas
│   ├── iaou.html          # IA de Outfits (Selección Mágica)
│   └── micuenta.html      # Perfil de usuario
│
└── images/                 # Recursos multimedia
    ├── bolsa.png
    ├── devolucion.png
    ├── direcciones.png
    ├── perfil.png
    └── WhatsApp_Video_2025-03-08_at_9_37_11_PM__1_.mp4

```

## Características

### Página Principal (index.html)
- Video de fondo
- Navegación principal con dropdowns
- Grid de categorías con efectos hover
- Enlaces a todas las secciones del sitio

### Páginas de Catálogo
- **Hombre**: Ropa masculina
- **Mujer**: Ropa femenina
- **Calzado**: Zapatos, tenis, botas
- **Accesorios**: Collares, pulseras, bolsos, etc.

Todas las páginas de catálogo comparten:
- Navegación consistente
- Grid de productos con efectos hover
- Botones de compra

### Páginas de Producto Individual
Características:
- Galería de imágenes del producto
- Detalles del producto
- Sidebar de carrito (se desliza desde la derecha)
- Información de envío y devoluciones

Productos disponibles:
- Pantalón Negro (patang.html)
- Pantalón Balloon (balle.html)
- Collar (colla.html)
- Zapatillas (Zapatillaska.html)

### IA de Outfits (iaou.html)
- Generador aleatorio de combinaciones de ropa
- Interface interactiva con botón "COMBINAR"
- Muestra 5 prendas aleatorias de una colección

### Mi Cuenta (micuenta.html)
- Perfil de usuario
- Menú de opciones:
  - Mis compras
  - Devoluciones online
  - Datos personales
  - Direcciones guardadas
- Opción de e-tickets

## Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: 
  - Flexbox y Grid para layouts
  - Transiciones y animaciones
  - Efectos hover avanzados
- **JavaScript Vanilla**: 
  - Manipulación del DOM
  - Dropdowns interactivos
  - Sidebar de carrito
  - Generador aleatorio de outfits
- **Google Fonts**: 
  - Playfair Display (páginas principales y catálogo)
  - Montserrat (páginas de producto)
  - Inter (IA y Mi Cuenta)

## Funcionalidades JavaScript

### Dropdowns
```javascript
function toggleDropdown(sectionId) {
    // Abre/cierra secciones dropdown en la navegación
}
```

### Carrito Lateral
```javascript
function toggleSidebar() {
    // Muestra/oculta el sidebar del carrito
}
```

### Generador de Outfits
```javascript
function randomizeImages() {
    // Genera combinaciones aleatorias de ropa
}
```

## Estilos Compartidos

### Navbar
- Fondo semi-transparente
- Hover effect en links
- Logo central
- Responsive design

### Productos
- Cards con sombra
- Efecto de escala al hover
- Imágenes optimizadas
- Botones de compra estilizados

## Rutas Relativas

El proyecto usa rutas relativas para facilitar su despliegue:
- CSS: `../css/archivo.css`
- JS: `../js/archivo.js`
- Imágenes: `../images/archivo.ext`
- HTML: `../index.html` o `archivo.html`

## Notas de Implementación

1. **Video de fondo**: El video en index.html debe estar en formato compatible (MP4)
2. **Imágenes**: La mayoría de imágenes se cargan desde URLs externas (Bershka CDN)
3. **Iconos**: Las imágenes locales (bolsa.png, perfil.png, etc.) tienen fallback con `onerror`
4. **Navegación**: Todos los enlaces funcionan con rutas relativas

## Próximos Pasos Sugeridos

1. Implementar backend para manejo de carrito
2. Agregar autenticación de usuarios
3. Conectar con pasarela de pago
4. Implementar búsqueda de productos
5. Agregar filtros avanzados en catálogos
6. Crear sistema de reviews de productos
7. Implementar wishlist/favoritos
8. Agregar funcionalidad de comparación de productos

## Licencia

Este es un proyecto de demostración para fines educativos.
