document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });

  document.querySelectorAll(".flash-close").forEach(button => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
  });

  const date = document.getElementById("preferred-date");
  if (date) {
    const today = new Date();
    const localDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    date.min = localDate;
  }

  const search = document.getElementById("request-search");
  const filter = document.getElementById("status-filter");
  const table = document.getElementById("requests-table");
  const count = document.getElementById("visible-count");
  if (search && filter && table) {
    const rows = [...table.querySelectorAll("tbody tr[data-search]")];
    const update = () => {
      const query = search.value.trim().toLowerCase();
      const status = filter.value;
      let visible = 0;
      rows.forEach(row => {
        const match = row.dataset.search.includes(query) && (!status || row.dataset.status === status);
        row.hidden = !match;
        if (match) visible++;
      });
      if (count) count.textContent = `${visible} request(s) shown`;
    };
    search.addEventListener("input", update);
    filter.addEventListener("change", update);
  }
});
