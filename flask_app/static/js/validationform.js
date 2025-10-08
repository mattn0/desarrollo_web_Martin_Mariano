

// Validación del formulario de anuncio (cliente) alineada con el servidor
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-anuncio");
  if (!form) return;

  const PHONE_REGEX = /^\+\d{3}\.\d{8,9}$/; // +NNN.NNNNNNNN

  form.addEventListener("submit", (e) => {
    const errors = [];

    const required = [
      ["region", "Debes seleccionar una región."],
      ["commune", "Debes seleccionar una comuna."],
      ["sector", "Debes indicar el sector."],
      ["name-user", "Debes ingresar tu nombre."],
      ["email-user", "Debes ingresar tu email."],
      ["pet-type", "Debes seleccionar el tipo de mascota."],
      ["amount", "Debes indicar la cantidad."],
      ["age", "Debes indicar la edad."],
      ["age-type", "Debes indicar Años/Meses."],
      ["delibery-date", "Debes ingresar una fecha de entrega."],
    ];

    required.forEach(([id, msg]) => {
      const el = form.querySelector(`[name="${id}"]`) || form.querySelector(`#${id}`);
      if (!el || !el.value) errors.push(msg);
    });

    const email = form.querySelector('[name="email-user"]')?.value || "";
    if (email && !email.includes("@")) errors.push("Email no tiene formato válido.");

    const tel = form.querySelector('[name="tel-user"]')?.value?.trim() || "";
    if (tel && !PHONE_REGEX.test(tel)) errors.push("Celular debe tener formato +NNN.NNNNNNNN.");

    const desc = form.querySelector('[name="description"]')?.value || "";
    if (desc.length > 500) errors.push("Descripción no debe exceder 500 caracteres.");

    if (errors.length) {
      e.preventDefault();
      alert(errors.join("\n"));
    }
  });
});
