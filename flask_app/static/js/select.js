


document.addEventListener("DOMContentLoaded", () => {
  const regionSel = document.getElementById("select-region");
  const comunaSel = document.getElementById("select-comuna");

  if (regionSel && comunaSel) {
    regionSel.addEventListener("change", () => {
      const regionId = regionSel.value;
      comunaSel.innerHTML = '<option value="">Seleccione una Comuna</option>';
      if (!regionId) return;

      fetch(`/comunas?region_id=${encodeURIComponent(regionId)}`, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
      .then(r => {
        if (!r.ok) throw new Error("No se pudieron cargar comunas");
        return r.json();
      })
      .then(data => {
        data.forEach(c => {
          const opt = document.createElement("option");
          opt.value = c.id;
          opt.textContent = c.nombre;
          comunaSel.appendChild(opt);
        });
      })
      .catch(err => {
        console.error(err);
        alert("Error cargando comunas. Intenta nuevamente.");
      });
    });
  }


  /* esto lo hace dinamico */ 
  const addBtn = document.getElementById("add-contact");
  const container = document.getElementById("contact-container");
  const tpl = document.getElementById("tpl-contact"); // requiere <template> en anuncio.html

  if (addBtn && container && tpl) {
    addBtn.addEventListener("click", () => {
      const node = tpl.content.firstElementChild.cloneNode(true);
      // Evitar IDs duplicados
      node.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
      container.appendChild(node);
    });

    container.addEventListener("change", (e) => {
      const sel = e.target.closest('select[name="contact_nombre[]"]');
      if (!sel) return;
      const row = sel.closest(".contact-row");
      const other = row.querySelector(".other-wrapper");
      if (!other) return;

      if (sel.value === "otra") {
        other.classList.remove("hidden");
      } else {
        other.classList.add("hidden");
        const inputOtro = other.querySelector('input[name="contact_otro_nombre"]');
        if (inputOtro) inputOtro.value = "";
      }
    });
  }
});
