document.addEventListener("DOMContentLoaded", () => {

  const tableContainer = document.getElementById("avisos-table");
  function enhancePagination() {
    document.querySelectorAll(".btn-page").forEach(btn => {
      btn.addEventListener("click", (ev) => {
        ev.preventDefault();
        const page = ev.currentTarget.getAttribute("data-page");
        if (!page) return;

        const url = new URL(window.location.href);
        url.searchParams.set("page", page);

        fetch(url.toString(), { headers: { "X-Requested-With": "XMLHttpRequest" } })
          .then(r => {
            if (!r.ok) throw new Error("Error al cargar avisos");
            return r.text();
          })
          .then(html => {
            if (tableContainer) {
              tableContainer.innerHTML = html;
              history.pushState({}, "", url.toString());
              enhancePagination(); // reenganchar listeners
            } else {
              window.location = url.toString();
            }
          })
          .catch(e => {
            console.error(e);
            window.location = ev.currentTarget.getAttribute("href");
          });
      });
    });
  }
  if (tableContainer) enhancePagination();


  const secComentarios = document.getElementById("comentarios");
  if (secComentarios) {
    const avisoId = secComentarios.getAttribute("data-aviso-id");
    const lista = document.getElementById("comentarios-lista");
    const form = document.getElementById("form-comentario");
    const btnAdd = document.getElementById("btn-agregar-com");
    const errBox = document.getElementById("comentario-errores");
    const inpNombre = document.getElementById("nombre-com");
    const inpTexto = document.getElementById("texto-com");

    const escapeHtml = (s) =>
      (s || "").replace(/[&<>\"']/g, (ch) => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[ch]));

    const renderComentarios = (items) => {
      if (!lista) return;
      if (!items || !items.length) {
        lista.innerHTML = "<p><em>No hay comentarios</em></p>";
        return;
      }
      const frag = document.createDocumentFragment();
      items.forEach(c => {
        const div = document.createElement("div");
        div.className = "comentario-item";
        div.innerHTML = `
          <div class="comentario-meta">${escapeHtml(c.fecha)} — <strong>${escapeHtml(c.nombre)}</strong></div>
          <div class="comentario-texto">${escapeHtml(c.texto)}</div>
        `;
        frag.appendChild(div);
      });
      lista.innerHTML = "";
      lista.appendChild(frag);
    };

    const cargarComentarios = () => {
      fetch(`/api/avisos/${avisoId}/comentarios`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(r => {
          if (!r.ok) throw new Error("No se pudieron cargar los comentarios");
          return r.json();
        })
        .then(renderComentarios)
        .catch(e => console.error(e));
    };

    const validar = () => {
      const errors = [];
      const nombre = (inpNombre.value || "").trim();
      const texto  = (inpTexto.value || "").trim();
      if (nombre.length < 3 || nombre.length > 80) errors.push("El nombre debe tener entre 3 y 80 caracteres.");
      if (texto.length < 5 || texto.length > 300) errors.push("El comentario debe tener entre 5 y 300 caracteres.");
      return { ok: errors.length === 0, errors, data: { nombre, texto } };
    };

    if (btnAdd) {
      //prevenimos el mismo error que con los contactos en la tarea 2
      btnAdd.replaceWith(btnAdd.cloneNode(true));
      const newBtn = document.getElementById("btn-agregar-com");
      newBtn.addEventListener("click", () => {
        const v = validar();
        if (!v.ok) {
          errBox.innerHTML = v.errors.map(e => `<div>• ${e}</div>`).join("");
          errBox.hidden = false;
          return;
        }
        errBox.hidden = true;

        fetch(`/api/avisos/${avisoId}/comentarios`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
          },
          body: JSON.stringify(v.data)
        })
        .then(async r => {
          if (!r.ok) {
            const j = await r.json().catch(() => ({}));
            const errs = (j && j.errors) ? j.errors : ["Error al enviar comentario."];
            throw new Error(errs.join("\n"));
          }
          return r.json();
        })
        .then(() => {
          form.reset();
          cargarComentarios();
        })
        .catch(e => {
          errBox.textContent = e.message || "Error al enviar comentario.";
          errBox.hidden = false;
        });
      });
    }

    // Carga inicial de comentarios
    cargarComentarios();
  }


  const elDia = document.getElementById("chart-dia");
  const elTipo = document.getElementById("chart-tipo");
  const elMes = document.getElementById("chart-mes");

  if (elDia || elTipo || elMes) {
    if (!window.Highcharts) {
      console.error("Highcharts no está cargado. Revisa el <script> en estadisticas.html");
      return;
    }
    const fetchJSON = (url) =>
      fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(r => {
          if (!r.ok) throw new Error("Error consultando " + url);
          return r.json();
        });

    // (1) Línea: avisos por día (últimos 30)
    if (elDia) {
      fetchJSON("/api/stats/por_dia?days=30")
        .then(data => {
          Highcharts.chart(elDia, {
            chart: { type: 'line' },
            title: { text: '' },
            xAxis: { categories: data.map(x => x.dia), title: { text: 'Día' } },
            yAxis: { title: { text: 'Avisos' }, allowDecimals: false },
            series: [{ name: 'Avisos', data: data.map(x => x.total) }]
          });
        })
        .catch(console.error);
    }

    // (2) Torta: total por tipo
    if (elTipo) {
      fetchJSON("/api/stats/por_tipo")
        .then(data => {
          Highcharts.chart(elTipo, {
            chart: { type: 'pie' },
            title: { text: '' },
            series: [{ name: 'Avisos', data: data.map(x => ({ name: x.tipo, y: x.total })) }]
          });
        })
        .catch(console.error);
    }

    // (3) Barras: por mes (gatos vs perros) — usa tu endpoint por_mes_tipo
    if (elMes) {
      const year = new Date().getFullYear();
      fetchJSON(`/api/stats/por_mes_tipo?year=${year}`)
        .then(data => {
          Highcharts.chart(elMes, {
            chart: { type: 'column' },
            title: { text: '' },
            xAxis: { categories: data.map(x => x.mes), title: { text: 'Mes' } },
            yAxis: { title: { text: 'Avisos' }, allowDecimals: false },
            plotOptions: { column: { pointPadding: 0.1, borderWidth: 0 } },
            series: [
              { name: 'Gato', data: data.map(x => x.gato) },
              { name: 'Perro', data: data.map(x => x.perro) }
            ]
          });
        })
        .catch(console.error);
    }
  }
});
