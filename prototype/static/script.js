
const selectElement = document.getElementById('select-subject');
let selectedSubject = selectElement.value

selectElement.addEventListener('change', function() {
  selectedSubject = this.value; // 'this' refers to the select element
  console.log('Selected value:', selectedSubject);
  // Do something with the selected value
});

document.getElementById("session-btn").addEventListener("click", function () {
    console.log("PRESSED!")
    
    fetch("api/start_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_id: 1, subject_name: selectedSubject })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            console.log(data)
            alert("Session started: " + data["data"]["subject_name"]);
        }
    })
    .catch(error => console.error("Error:", error));
});