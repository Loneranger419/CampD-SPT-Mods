document.addEventListener("DOMContentLoaded", function () {
    const currentVersion = "4.0.1";
    const [curMajor, curMinor, curPatch] = currentVersion.split(".").map(Number);

    // Create lists
    const allItems = Array.from(document.querySelectorAll("li"));
    const currentList = document.querySelector("#currentList");
    const potentialList = document.querySelector("#potentialList");

    // Sort alphabetically by link text
    allItems.sort((a, b) =>
        a.querySelector("a").textContent.toLowerCase()
        .localeCompare(b.querySelector("a").textContent.toLowerCase())
    );

    // Process each item
    allItems.forEach((item) => {
        const modVersion  = item.dataset.modVersion || "0.0.0";
        const modGameVersion = item.dataset.gameVersion || "0.0.0";
        const [modMajor = 0, modMinor = 0, modPatch = 0] = modGameVersion.split(".").map(Number);
        const link = item.querySelector("a");
    
        // Determine color
        let color = "red";
        if (modMajor === curMajor) {
            if (modMinor < curMinor) color = "yellow";
            else if (modMinor === curMinor && modPatch < curPatch) color = "yellow";
            else color = "green";
        }
    
        // Build indicator
        const indicator = document.createElement("span");
        indicator.className = "indicator";
        indicator.style.backgroundColor = color;
    
        // Rebuild list item
        item.innerHTML = "";
        item.appendChild(indicator);
                
        const versionSpan = document.createElement("span");
        versionSpan.className = "version";
        versionSpan.textContent = modVersion;
        item.appendChild(versionSpan);
                    
        item.appendChild(link);
        
        // Append to correct list
        if (item.dataset.current === "true") {
            currentList.appendChild(item);
        } else {
            potentialList.appendChild(item);
        }
    });
});