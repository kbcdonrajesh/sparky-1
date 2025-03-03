// Add Talent
function addTalent() {
    let name = document.getElementById("name").value;
    let skill = document.getElementById("skill").value;
    let workLink = document.getElementById("workLink").value;
    let workImage = document.getElementById("workImage").files[0];

    if (!name || !skill) {
        alert("Please enter your name and talent!");
        return;
    }

    let formData = new FormData();
    formData.append("name", name);
    formData.append("skill", skill);
    formData.append("workLink", workLink);
    if (workImage) formData.append("workImage", workImage);

    fetch("/add_talent", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert("Talent Added!");
        loadTalents(); // Refresh talent list
    });
}

// Load Talents and Showcase Work
function loadTalents() {
    fetch("/get_talents")
    .then(response => response.json())
    .then(talents => {
        let talentContainer = document.getElementById("talents");
        talentContainer.innerHTML = "";

        talents.forEach(talent => {
            let div = document.createElement("div");
            div.className = "talent";

            div.innerHTML = `
                <h3>${talent.name} - ${talent.skill}</h3>
                ${talent.workLink ? `<p>🔗 <a href="${talent.workLink}" target="_blank">View Work</a></p>` : ""}
                ${talent.workImage ? `<img src="${talent.workImage}" width="200">` : ""}
            `;

            talentContainer.appendChild(div);
        });
    });
}
// Add Talent
function addTalent() {
    let name = document.getElementById("name").value;
    let skill = document.getElementById("skill").value;
    let workLink = document.getElementById("workLink").value;
    let workImage = document.getElementById("workImage").files[0];

    if (!name || !skill) {
        alert("Please enter your name and talent!");
        return;
    }

    let formData = new FormData();
    formData.append("name", name);
    formData.append("skill", skill);
    formData.append("workLink", workLink);
    if (workImage) formData.append("workImage", workImage);

    fetch("/add_talent", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert("Talent Added!");
        loadTalents(); // Refresh talent list
    });
}

// Load Talents and Showcase Work
function loadTalents() {
    fetch("/get_talents")
    .then(response => response.json())
    .then(talents => {
        let talentContainer = document.getElementById("talents");
        talentContainer.innerHTML = "";

        talents.forEach(talent => {
            let div = document.createElement("div");
            div.className = "talent";

            div.innerHTML = `
                <h3>${talent.name} - ${talent.skill}</h3>
                ${talent.workLink ? `<p>🔗 <a href="${talent.workLink}" target="_blank">View Work</a></p>` : ""}
                ${talent.workImage ? `<img src="${talent.workImage}" width="200">` : ""}
            `;

            talentContainer.appendChild(div);
        });
    });
}
