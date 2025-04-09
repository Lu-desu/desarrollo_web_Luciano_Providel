window.onload = function () {
    cargarRegiones();
    setDefaultDateTime();
    document.getElementById("region").addEventListener("change", cargarComunas);
    document.getElementById("contacto").addEventListener("change", mostrarContacto);
    document.getElementById("tema").addEventListener("change", mostrarOtroTema);
    document.getElementById("agregar-foto").addEventListener("click", agregarCampoFoto);
    document.getElementById("actividadForm").addEventListener("submit", manejarEnvio);
    document.getElementById("confirmar-si").addEventListener("click", function () {
      document.getElementById("confirmacion").style.display = "none";
      document.getElementById("mensaje-final").style.display = "block";
    });
    document.getElementById("confirmar-no").addEventListener("click", function () {
      document.getElementById("confirmacion").style.display = "none";
      document.getElementById("actividadForm").style.display = "block";
    });
  };
  
  function cargarRegiones() {
    const selectRegion = document.getElementById("region");
    region_comuna.regiones.forEach(region => {
      const option = document.createElement("option");
      option.value = region.nombre;
      option.textContent = region.nombre;
      selectRegion.appendChild(option);
    });
  }
  
  function cargarComunas() {
    const regionSeleccionada = this.value;
    const selectComuna = document.getElementById("comuna");
    selectComuna.innerHTML = "<option value=''>Seleccione comuna</option>";
  
    const region = region_comuna.regiones.find(r => r.nombre === regionSeleccionada);
    if (region) {
      region.comunas.forEach(comuna => {
        const option = document.createElement("option");
        option.value = comuna.nombre;
        option.textContent = comuna.nombre;
        selectComuna.appendChild(option);
      });
    }
  }
  
  function mostrarContacto() {
    const contenedor = document.getElementById("contacto-info-container");
    contenedor.innerHTML = ""; 
  
    const seleccion = this.value;
    if (seleccion) {
      const input = document.createElement("input");
      input.type = "text";
      input.name = "contacto_id";
      input.id = "contacto_id";
      input.placeholder = `ID o URL de contacto (${seleccion})`;
      input.minLength = 4;
      input.maxLength = 50;
      input.required = false;
      contenedor.appendChild(input);
    }
  }
  
  function mostrarOtroTema() {
    const contenedor = document.getElementById("otro-tema-container");
    contenedor.innerHTML = "";
    if (this.value === "otro") {
      const input = document.createElement("input");
      input.type = "text";
      input.name = "otroTema";
      input.id = "otroTema";
      input.placeholder = "Describa el tema";
      input.minLength = 3;
      input.maxLength = 15;
      input.required = true;
      contenedor.appendChild(input);
    }
  }
  
  function agregarCampoFoto(event) {
    event.preventDefault();
    const contenedor = document.getElementById("foto-container");
    const fotosActuales = contenedor.querySelectorAll('input[type="file"]').length;
  
    if (fotosActuales < 5) {
      const input = document.createElement("input");
      input.type = "file";
      input.name = "foto";
      input.accept = "image/*";
      input.required = fotosActuales === 0; // Solo la primera es obligatoria
      contenedor.appendChild(document.createElement("br"));
      contenedor.appendChild(input);
    } else {
      alert("No se pueden agregar más de 5 fotos.");
    }
  }
  
  function setDefaultDateTime() {
    const inicio = document.getElementById("inicio");
    const termino = document.getElementById("termino");
    const ahora = new Date();
    const formato = ahora.toISOString().slice(0, 16);
    inicio.value = formato;
  
    const mas3Horas = new Date(ahora.getTime() + 3 * 60 * 60 * 1000);
    termino.value = mas3Horas.toISOString().slice(0, 16);
  }
  
  function manejarEnvio(event) {
    event.preventDefault();
  
    if (!validarFormulario()) {
      alert("Hay errores en el formulario >:(");
      return;
    }
  
    document.getElementById("actividadForm").style.display = "none";
    document.getElementById("confirmacion").style.display = "block";
  }
  
  function validarFormulario() {
    let valido = true;
  
    const region = document.getElementById("region").value;
    const comuna = document.getElementById("comuna").value;
    const nombre = document.getElementById("nombre").value;
    const email = document.getElementById("email").value;
    const celular = document.getElementById("telefono").value;
    const contacto_id = document.getElementById("contacto_id");
    const inicio = new Date(document.getElementById("inicio").value);
    const terminoInput = document.getElementById("termino");
    const termino = new Date(terminoInput.value);
    const tema = document.getElementById("tema").value;
    const otroTema = document.getElementById("otroTema");
  
    if (!region || !comuna || !nombre || !email || !inicio) {
      valido = false;
    }
  
    if (nombre.length > 200 || email.length > 100) {
      valido = false;
    }

  
    if (celular && !/^\+\d{3}\.\d{8,9}$/.test(celular)) {
      valido = false;
    }
  
    if (contacto_id && contacto_id.value && (contacto_id.value.length < 4 || contacto_id.value.length > 50)) {
      valido = false;
    }
  
    if (terminoInput.value && termino <= inicio) {
      valido = false;
    }
  
    if (!tema) {
      valido = false;
    }
  
    if (tema === "otro" && (!otroTema || otroTema.value.length < 3 || otroTema.value.length > 15)) {
      valido = false;
    }
  
    const fotos = document.querySelectorAll('input[type="file"]');
    if (fotos.length < 1 || fotos.length > 5) {
      valido = false;
    }
  
    return valido;
  }
  