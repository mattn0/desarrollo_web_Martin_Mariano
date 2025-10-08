

document.addEventListener("DOMContentLoaded", () => {
  const tableContainer = document.getElementById("avisos-table");
  if (!tableContainer) return;

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
            tableContainer.innerHTML = html;
            history.pushState({}, "", url.toString());
            enhancePagination(); // re-engancha los listeners nuevos
          })
          .catch(e => {
            console.error(e);
            // Fallback: navegación normal si falla AJAX
            window.location = ev.currentTarget.getAttribute("href");
          });
      });
    });
  }

  enhancePagination();
});
