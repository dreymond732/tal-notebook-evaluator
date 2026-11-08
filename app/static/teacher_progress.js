"use strict";
(() => {
  const search = document.getElementById("filter-students");
  const roster = document.getElementById("teacher-roster");
  if (!search || !roster) return;
  const rows = Array.from(roster.querySelectorAll("tbody tr"));
  const counter = document.getElementById("filtered-count");
  const normalize = value => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("fr").trim();
  const filter = () => {
    const query = normalize(search.value);
    let shown = 0;
    for (const row of rows) {
      row.hidden = !normalize(row.dataset.student || "").includes(query);
      if (!row.hidden) shown += 1;
    }
    if (counter) counter.textContent = shown + " étudiant" + (shown === 1 ? "" : "s") + " affiché" + (shown === 1 ? "" : "s");
  };
  search.addEventListener("input", filter);
  filter();
})();
