document.getElementById("studyForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let subject = document.getElementById("subject").value;
    let duration = document.getElementById("duration").value;
    let notes = document.getElementById("notes").value;

    console.log("what is happening?")

    fetch("/add_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, duration, notes })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("points").innerText = data.points;
        document.getElementById("level").innerText = data.level;
        document.getElementById("badges").innerText = data.badges.join(", ") || "None";
    });
});
