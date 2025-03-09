 // ✅ Initialize Socket.IO

function startBattle(event) {
    
    event.preventDefault();

    const form = document.getElementById('startBattleForm');
    const formData = new FormData(form);
    const targetUrl = formData.get("target_url");
    const userId = formData.get("user_id")

    // console.log("Form Data:", );
    // ✅ Extract selected quests
    const battle_duration = formData.get("battle_duration");
    const selectedQuests = formData.getAll("selected_quests");

    selectedQuests.forEach((quest, index) => {
        formData.append(`selected_  quests[${index}]`, quest);
    });
    
    
    console.log("Selected Quests:", selectedQuests);
    console.log("battle_duration:" + battle_duration)

    fetch(targetUrl, { // Replace with your actual endpoint
        method: 'POST',
        headers: { "Content-Type": "application/json" }, // ✅ Tell Flask to expect JSON
        body: JSON.stringify({
                "user_id": userId,
                "subject_id": selectedSubjectId, 
                "selected_quests": selectedQuests,
                "battle_duration": battle_duration
            }),
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse JSON response
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        document.body.focus();
        console.log('Success session:', data);
        modalSystem.hide('startBattleModal');
        form.reset();


        battleOverlay.style.display = 'flex';
        initializeBattle();

    })
    .catch((error) => {
        alert('Failed to start session');
        console.error('Error:', error);
        // Handle error (e.g., show error message)
    });

}

function updateSessionTimer(data) {
    console.log("Session update:", data);
    const timerElement = document.getElementById("session-timer");
    const timeLeft = data.time_left;

    if (timerElement) {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

function handleSessionEnd(data) {
    console.log("Session ended:", data);
    alert("Session has ended!");

    // ✅ Reset session UI
    document.getElementById("session-timer").textContent = "00:00:00";
    currentSessionId = null;
}