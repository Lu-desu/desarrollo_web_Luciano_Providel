const actividades = [
    {
      inicio: "2025-03-28 12:00",
      termino: "2025-03-28 14:00",
      comuna: "Santiago",
      sector: "Beauchef 850, pajarera",
      tema: "juegos",
      nombre: "Torneo de Pokemon TCG",
      organizador: "Club Pokémon UChile",
      fotos: ["pokemon.jpg"]
    },
    {
      inicio: "2025-03-29 19:00",
      termino: "2025-03-29 21:00",
      comuna: "Santiago",
      sector: "Tienda OOPS!",
      tema: "juegos",
      nombre: "Torneo Digimon",
      organizador: "Tienda OOPS!",
      fotos: ["digimon.jpg"]
    },
    {
      inicio: "2025-03-30 19:00",
      termino: "2025-03-30 21:00",
      comuna: "Santiago",
      sector: "Parque O’Higgins",
      tema: "feria",
      nombre: "Feria Friki",
      organizador: "Comunidad Geek",
      fotos: ["feria.jpg"]
    },
    {
      inicio: "2025-04-01 10:00",
      termino: "2025-04-01 13:00",
      comuna: "Providencia",
      sector: "Tienda Tea&Coffe Games",
      tema: "juegos",
      nombre: "Escuelita Digimon",
      organizador: "Tea&Coffe Games",
      fotos: ["terrier.jpeg"]
    },
    {
      inicio: "2025-04-04 16:30",
      termino: "2025-04-04 22:00",
      comuna: "Santiago",
      sector: "Beauchef 850, patio",
      tema: "baile",
      nombre: "Carrete owo",
      organizador: "Estudiantes de Beauchef",
      fotos: ["carrete.jpg"]
    }
  ];

  const tabla = document.querySelector("#tabla-actividades tbody");
  const detalle = document.getElementById("detalle");
  const info = document.getElementById("info");
  const fotosDiv = document.getElementById("fotos");
  const modal = document.getElementById("modal");
  const imgAmpliada = document.getElementById("imagen-ampliada");
  
  actividades.forEach((act, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${act.inicio}</td>
      <td>${act.termino}</td>
      <td>${act.comuna}</td>
      <td>${act.sector}</td>
      <td>${act.tema}</td>
      <td>${act.nombre}</td>
      <td>${act.organizador}</td>
      <td>${act.fotos.length}</td>
    `;
    tr.addEventListener("click", () => mostrarDetalle(i));
    tabla.appendChild(tr);
  });
  
  function mostrarDetalle(i) {
    const act = actividades[i];
    document.querySelector("table").style.display = "none";
    detalle.style.display = "block";
  
    info.innerHTML = `
      <strong>Nombre:</strong> ${act.nombre}<br>
      <strong>Inicio:</strong> ${act.inicio}<br>
      <strong>Término:</strong> ${act.termino}<br>
      <strong>Comuna:</strong> ${act.comuna}<br>
      <strong>Sector:</strong> ${act.sector}<br>
      <strong>Tema:</strong> ${act.tema}<br>
      <strong>Organizador:</strong> ${act.organizador}<br>
      <strong>Total Fotos:</strong> ${act.fotos.length}<br>
    `;
  
    fotosDiv.innerHTML = "";
    act.fotos.forEach(foto => {
      const img = document.createElement("img");
      img.src = `imagenes/${foto}`;
      img.className = "foto-mini";
      img.addEventListener("click", () => {
        imgAmpliada.src = `imagenes/${foto}`;
        modal.style.display = "flex";
      });
      fotosDiv.appendChild(img);
    });
  }
  
  function volverListado() {
    detalle.style.display = "none";
    document.querySelector("table").style.display = "table";
  }
  
  function cerrarModal() {
    modal.style.display = "none";
  }
  