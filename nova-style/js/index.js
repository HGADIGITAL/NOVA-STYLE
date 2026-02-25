let activeSection = null;

function toggleDropdown(sectionId) {
    var section = document.getElementById(sectionId);
    if (activeSection && activeSection !== section) {
        activeSection.classList.remove("active");
    }
    section.classList.toggle("active");
    activeSection = section.classList.contains("active") ? section : null;
}
