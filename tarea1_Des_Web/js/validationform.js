
function showErrors(errors) {
    const box = document.getElementById("val-box");
    const list = document.getElementById("val-list");
    if (!box || !list) return;
    list.innerHTML = "";
    errors.forEach(msg => {
        const li = document.createElement("li");
        li.textContent = msg;
        list.appendChild(li);
    });
    box.hidden = errors.length === 0;
    document.getElementById("val-msg").textContent = errors.length ? "Corrige los siguientes campos:" : "";
}

const validarForm1 = () => {
    let errores = [];

    const region = document.getElementById("select-region").value;
    const comuna = document.getElementById("select-comuna").value;
    const sector = document.getElementById("text-sector").value;

    if (!region) {
        errores.push("Debe seleccionar una región");
    }
    if (!comuna) {
        errores.push("Debe seleccionar una comuna");
    }
    if (sector.length > 100) {
        errores.push("El sector no puede tener más de 100 caracteres");
    }

    return errores;
}

const validarForm2 = () => {
    let errores = [];

    const nombre = document.getElementById("name-user").value.trim();
    const email = document.getElementById("email-user").value.trim();
    const telefono = document.getElementById("tel-user").value.trim();
    const contacto = document.getElementById("user-connection").value;

    if (nombre.length < 3 || nombre.length > 200) {
        errores.push("El nombre debe tener entre 3 y 200 caracteres");
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 100) {
    errores.push("El email no es válido o supera 100 caracteres");
    }

    if (telefono && !/^\+\d{3}\.\d{8,9}$/.test(telefono)) {
        errores.push("El teléfono debe tener formato +NNN.NNNNNNNN");
    }

    if (!contacto) {
        errores.push("Debe seleccionar un medio de contacto");
    }

    return errores;

}

const validarForm3 = () => {
    let errores = [];

    const tipo = document.getElementById("animal-type").value;
    const cantidad = document.getElementById("animal-quantity").value;
    const edad = document.getElementById("animal-age").value;
    const unidadEdad = document.getElementById("age-type").value;
    const fechaEntrega = document.getElementById("delibery-date").value;
    const descripcion = document.getElementById("animal-description").value;

    if (!tipo) {
        errores.push("Debe seleccionar el tipo de animal");
    }

    if (!cantidad || cantidad < 1) {
        errores.push("La cantidad debe ser al menos 1");
    }

    if (!edad || edad < 1) {
        errores.push("La edad debe ser al menos 1");
    }

    if (!unidadEdad) {
        errores.push("Debe seleccionar la unidad de edad");
    }

    if (!fechaEntrega) {
        errores.push("Debe indicar una fecha de entrega");
    } else {
        let fecha = new Date(fechaEntrega);
        let ahora = new Date();
        if (fecha < ahora) {
            errores.push("La fecha de entrega debe ser futura");
        }
    }

    if (descripcion.length > 200) {
        errores.push("La descripción no puede superar 200 caracteres");
    }

    return errores;
}

window.addEventListener("load", () => {
    const btn = document.getElementById("send-button");
    if (!btn) return;

    const confirmModal = document.getElementById("confirm-modal");
    const sentBox = document.getElementById("sent-box");
    const confirmYes = document.getElementById("confirm-yes");
    const confirmNo = document.getElementById("confirm-no");

    btn.addEventListener("click", (e) => {
        e.preventDefault();
        const errs = [...validarForm1(), ...validarForm2(), ...validarForm3()];
        if (errs.length) {
            showErrors(errs);
            document.getElementById("val-box").scrollIntoView({ behavior: "smooth" });
            return;
        }
        // sin errores
        if (confirmModal) confirmModal.hidden = false;
    });

    if (confirmNo) {
        confirmNo.addEventListener("click", () => {
        if (confirmModal) confirmModal.hidden = true;
        // volver al formulario (no limpiar nada)
        });
    }
    if (confirmYes) {
        confirmYes.addEventListener("click", () => {
        if (confirmModal) confirmModal.hidden = true;
        // mostrar mensaje enviado
        if (sentBox) sentBox.hidden = false;
        });
    }
});