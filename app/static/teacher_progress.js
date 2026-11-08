"use strict";
(() => {
  // L'ouverture du portail suffit à déclencher une demande de code.
  // Le formulaire reste accessible discrètement pour une demande de renvoi.
  // Un garde côté onglet évite les boucles si le navigateur perd son cookie
  // derrière un reverse proxy mal configuré.
  const automatic = document.getElementById("teacher-code-auto-send");
  if (automatic && automatic.dataset.autoSend === "true") {
    const key = "tal_teacher_auto_code_at";
    const now = Date.now();
    let previous = 0;
    try { previous = Number(sessionStorage.getItem(key) || "0"); } catch (_) {}
    if (!previous || now - previous >= 10 * 60 * 1000) {
      try { sessionStorage.setItem(key, String(now)); } catch (_) {}
      automatic.submit();
      return;
    }
  }
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
