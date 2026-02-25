function toggleSidebar() {
    document.getElementById('cart-sidebar').classList.toggle('active');
}

function toggleDropdown(sectionId) {
    // Cierra todas las secciones primero
    const sections = document.querySelectorAll('.dropdown-section');
    sections.forEach((section) => {
        if (section.id !== sectionId) {
            section.classList.remove('active');
        }
    });

    // Ahora abre la sección que se ha clicado
    const section = document.getElementById(sectionId);
    section.classList.toggle('active');
}
