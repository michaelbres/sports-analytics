/* ============================================================
   Sports Analytics — Core JS
   Handles: nav active state, shared utilities
   ============================================================ */

// ── Active nav link ──────────────────────────────────────
(function () {
  const path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href");
    if (href === path) link.classList.add("active");
  });
})();

// ── Shared API helper ────────────────────────────────────
const API = {
  base: "/api",

  async get(path, params = {}) {
    const url = new URL(this.base + path, window.location.origin);
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`API ${resp.status}: ${path}`);
    return resp.json();
  },
};

// ── Table builder ────────────────────────────────────────
function buildTable(tableEl, columns, rows) {
  const thead = tableEl.querySelector("thead");
  const tbody = tableEl.querySelector("tbody");

  thead.innerHTML = `<tr>
    <th class="rank">#</th>
    ${columns.map((c) => `<th data-key="${c.key}">${c.label}</th>`).join("")}
  </tr>`;

  let sortKey = columns[0].key;
  let sortAsc = false;

  function render(data) {
    tbody.innerHTML = data
      .map(
        (row, i) => `<tr>
        <td class="rank">${i + 1}</td>
        ${columns
          .map((c) => {
            const val = row[c.key];
            const display = val === null || val === undefined ? "—" : (c.fmt ? c.fmt(val) : val);
            return `<td>${display}</td>`;
          })
          .join("")}
      </tr>`
      )
      .join("");
  }

  function sort(key) {
    if (sortKey === key) sortAsc = !sortAsc;
    else { sortKey = key; sortAsc = false; }

    thead.querySelectorAll("th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.key === sortKey) th.classList.add(sortAsc ? "sort-asc" : "sort-desc");
    });

    rows.sort((a, b) => {
      const va = a[sortKey] ?? -Infinity;
      const vb = b[sortKey] ?? -Infinity;
      return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
    });
    render(rows);
  }

  thead.querySelectorAll("th[data-key]").forEach((th) => {
    th.addEventListener("click", () => sort(th.dataset.key));
  });

  sort(sortKey);
}

// ── Search filter ────────────────────────────────────────
function filterRows(rows, query, fields) {
  const q = query.toLowerCase();
  return rows.filter((r) => fields.some((f) => (r[f] || "").toLowerCase().includes(q)));
}

// ── Number formatters ────────────────────────────────────
const fmt = {
  dec1: (v) => (v == null ? "—" : Number(v).toFixed(1)),
  dec2: (v) => (v == null ? "—" : Number(v).toFixed(2)),
  dec3: (v) => (v == null ? "—" : Number(v).toFixed(3)),
  pct:  (v) => (v == null ? "—" : Number(v).toFixed(1) + "%"),
  int:  (v) => (v == null ? "—" : Math.round(v).toLocaleString()),
};

// ── Loading helper ───────────────────────────────────────
function setLoading(show) {
  const el = document.getElementById("loading");
  const content = document.getElementById("content");
  if (el) el.style.display = show ? "block" : "none";
  if (content) content.style.display = show ? "none" : "block";
}
