
const anuncios = {
    1: {
        nombre: "María",
        email: "maria@gmail.com",
        comuna: "Santiago",
        sector: "Beauchef 850",
        mascota: "1 Gato, 2 meses",
        fotos: ["/pictures/cat1.jpg"]
    },
    2: {
        nombre: "Carlos",
        email: "carlos@gmail.com",
        comuna: "Ñuñoa",
        sector: "Plaza Ñuñoa",
        mascota: "3 Perros, 2 meses",
        fotos: ["/pictures/dogs3.jpg", "/pictures/dog2.jpg"]
    },
    3: {
        nombre: "Ana",
        email: "ana@gmail.com",
        comuna: "Valparaíso",
        sector: "Cerro Alegre",
        mascota: "2 Gatos, 1 año",
        fotos: ["/pictures/cat2.jpg", "/pictures/cat3.jpg"]
    },
    4: { 
        nombre: "Javier",
        email: "javier@gmail.com",
        comuna: "Concepción",
        sector: "Centro",
        mascota: "1 Perro, 6 meses",
        fotos: ["/pictures/dog1.jpg"]
    },
    5: {
        nombre: "Sofía",
        email: "sofia@gmail.com",
        comuna: "La Serena",
        sector: "Av. del Mar",
        mascota: "2 Gatos, 3 meses",
        fotos: ["/pictures/cat4.jpg", "/pictures/cat5.jpg"]
    }
};

// Mostrar detalle
function mostrarDetalle(id) {
    document.getElementById("table2").hidden = true;
    document.getElementById("detalle").hidden = false;

    const anuncio = anuncios[id];
    document.getElementById("detalle-nombre").textContent = anuncio.nombre;
    document.getElementById("detalle-email").textContent = anuncio.email;
    document.getElementById("detalle-comuna").textContent = anuncio.comuna;
    document.getElementById("detalle-sector").textContent = anuncio.sector;
    document.getElementById("detalle-mascota").textContent = anuncio.mascota;

    const fotosDiv = document.getElementById("detalle-fotos");
    fotosDiv.innerHTML = "";
    anuncio.fotos.forEach((src) => {
        let img = document.createElement("img");
        img.src = src;
        img.width = 320;
        img.height = 240;
        img.style.margin = "5px";
        img.onclick = () => ampliarFoto(src);
        fotosDiv.appendChild(img);
    });
}

// Volver al listado
function volverList() {
    document.getElementById("table2").hidden = false;
    document.getElementById("detalle").hidden = true;
}

// Ampliar foto
function ampliarFoto(src) {
    const modal = document.getElementById("see-photo");
    const big = document.getElementById("bigger-photo");
    big.src = src;          
    big.width = 800;
    big.height = 600;
    modal.hidden = false;
}

function closephoto() {
    document.getElementById("see-photo").hidden = true;
}