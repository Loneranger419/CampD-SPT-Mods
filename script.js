document.addEventListener("DOMContentLoaded", () => {
  const currentList = document.getElementById("currentList");
  const potentialList = document.getElementById("potentialList");

  // === Configure this to match your current SPT game version ===
  const CURRENT_GAME_VERSION = "4.0.1";

  // --- Helpers ---
  function parseVersion(v) {
    return v.split(".").map(x => parseInt(x, 10) || 0);
  }

  function getIndicatorColor(modGameVersion) {
    const mod = parseVersion(modGameVersion);
    const cur = parseVersion(CURRENT_GAME_VERSION);

    const [majM, minM, patM] = mod;
    const [majC, minC, patC] = cur;

    if (majM === majC && minM === minC && patM === patC) {
      return "#2ecc71"; // perfect match (green)
    }
    if (majM === majC && minM === minC) {
      return "#f1c40f"; // same major/minor, patch difference (yellow)
    }
    if (majM === majC && Math.abs(minM - minC) <= 1) {
      return "#f39c12"; // one minor version off (orange)
    }
    return "#e74c3c"; // major mismatch (red)
  }

  fetch("mods.json")
    .then(res => {
      if (!res.ok) throw new Error("Failed to load mods.json");
      return res.json();
    })
    .then(mods => {
      mods.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" }));

      for (const mod of mods) {
        const li = document.createElement("li");

        // --- Indicator ---
        const indicator = document.createElement("span");
        indicator.classList.add("indicator");
        indicator.style.backgroundColor = getIndicatorColor(mod.game_version);
        indicator.title = `Mod for ${mod.game_version} vs current ${CURRENT_GAME_VERSION}`;

        // --- Icon ---
        const icon = document.createElement("img");
        icon.src = mod.icon;
        icon.alt = mod.name;
        icon.width = 32;
        icon.height = 32;
        icon.style.borderRadius = "4px";

        // --- Version text ---
        const version = document.createElement("span");
        version.className = "version";
        version.textContent = mod.mod_version;

        // --- Link ---
        const link = document.createElement("a");
        link.href = mod.url;
        link.textContent = mod.name;
        link.target = "_blank";

        // --- Assemble ---
        li.append(indicator, icon, version, link);

        // --- Append to correct section ---
        (mod.current ? currentList : potentialList).appendChild(li);
      }
    })
    .catch(err => {
      console.error("Error loading mod list:", err);
      const msg = document.createElement("p");
      msg.textContent = "Failed to load mod list.";
      document.body.appendChild(msg);
    });
});