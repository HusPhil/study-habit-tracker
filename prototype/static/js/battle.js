 // ✅ Initialize Socket.IO

function startBattle(event) {
    
    event.preventDefault();

    const form = document.getElementById('startBattleForm');
    const formData = new FormData(form);
    const targetUrl = formData.get("target_url");
    const userId = formData.get("user_id")

    // ✅ Extract selected quests
    const battle_duration = formData.get("battle_duration");
    const formSelectedQuests = formData.getAll("selected_quests");
    const selectedQuests = []

    formSelectedQuests.forEach((questId, index) => {
        const difficulty = formData.get(`quest_difficulty_${questId}`); 
        const description = formData.get(`quest_description_${questId}`); 
        const quest = {
            "id": parseInt(questId),
            "difficulty": parseInt(difficulty),
            "description": description
        }
        selectedQuests.push(quest);
    });
    
    
    console.log("Selected Quests:", formSelectedQuests);
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
        initializeBattle(data["enemies"], parseInt(data["session_data"]["duration"]));

    })
    .catch((error) => {
        alert('Failed to start session');
        console.error('Error:', error);
        endBattle(false)
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