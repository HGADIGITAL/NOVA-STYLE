const clothingImages = [
    'https://static.bershka.net/assets/public/a410/932c/a6584c21aa24/b3dc21559ec5/01820727812-a4o/01820727812-a4o.jpg?ts=1738060899843&w=450',
    'https://static.bershka.net/assets/public/7cc1/8d43/eaf4478da252/61d5bd9464d0/05026352428-a4o/05026352428-a4o.jpg?ts=1740585592492&w=450',
    'https://static.bershka.net/assets/public/b146/5110/ab0e41e2abac/fc2bd756e5a2/08987184800-a4o/08987184800-a4o.jpg?ts=1740645179198&w=450',
    'https://static.bershka.net/assets/public/c0de/7cf3/18d742e19b05/49e38e315f84/01428109305-a4o/01428109305-a4o.jpg?ts=1737537812265&w=450',
    'https://static.bershka.net/assets/public/5aea/4fe3/20084cc3b268/d11573ec42ae/05023666809-a4o/05023666809-a4o.jpg?ts=1737557807925&w=450',
    'https://static.bershka.net/assets/public/24a9/0786/62a0492fa9b6/6013b890bfb0/07112777400-a4o/07112777400-a4o.jpg?ts=1739371656841&w=450',
    'https://static.bershka.net/assets/public/8181/d5ba/3efd4c6c957c/ff23e7928fc3/00027074500-a4o/00027074500-a4o.jpg?ts=1738247253484&w=450',
    'https://static.bershka.net/assets/public/d8cf/294d/694e4fac8998/33510ea676b4/01151008800-a4o/01151008800-a4o.jpg?ts=1738836536063&w=450',
    'https://static.bershka.net/assets/public/0413/bbde/8f6c46c18354/f84d06d9f935/11058460040-a4o/11058460040-a4o.jpg?ts=1737474790867&w=450',
    'https://static.bershka.net/assets/public/54c7/3bfc/2d3b4b799e52/cac701c323bb/11036560040-a4o/11036560040-a4o.jpg?ts=1740398720990&w=800'
];

function randomizeImages() {
    const cards = document.querySelectorAll('.card img');
    cards.forEach(img => {
        const randomIndex = Math.floor(Math.random() * clothingImages.length);
        img.src = clothingImages[randomIndex];
        img.style.opacity = 1;
    });
}

let activeSection = null;

function toggleDropdown(sectionId) {
    var section = document.getElementById(sectionId);
    if (activeSection && activeSection !== section) {
        activeSection.classList.remove("active");
    }
    section.classList.toggle("active");
    activeSection = section.classList.contains("active") ? section : null;
}
