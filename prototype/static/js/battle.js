let selectedQuestOrder = []; // Ordered list of selected quest IDs

document.getElementById("battle-quest-list").addEventListener("change", function (event) {
    if (event.target.matches("input[name='selected_quests']")) {
        const questId = event.target.value;

        if (event.target.checked) {
            // Add to the selection order if not already present
            if (!selectedQuestOrder.includes(questId)) {
                selectedQuestOrder.push(questId);
            }
        } else {
            // Remove if unchecked
            selectedQuestOrder = selectedQuestOrder.filter(id => id !== questId);
        }

        console.log("Updated Selection Order:", selectedQuestOrder);
    }
});

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

    console.log("formSelectedQuests:", formSelectedQuests);
    selectedQuestOrder.forEach((questId, index) => {
        const difficulty = formData.get(`quest_difficulty_${questId}`); 
        const description = formData.get(`quest_description_${questId}`); 
        const subject_id = formData.get(`quest_subject_id_${questId}`); 
        
        console.log("desc:", description, questId);
        const quest = {
            "id": parseInt(questId),
            "difficulty": parseInt(difficulty),
            "description": description,
            "subject_id": subject_id,
        }
        selectedQuests.push(quest);
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

        const battle_duration = parseInt(data["session_data"]["duration"]);

        if (data["session_data"]["error"]) {
            return
        }

        battleOverlay.style.display = 'flex';
        initializeBattle(data["enemies"], parseInt(data["session_data"]["duration"]));

    })
    .finally(() => {    
        selectedQuestOrder = []
    })
    .catch((error) => {
        alert('Failed to start session');
        console.error('Error:', error);
        endBattle(false)
        // Handle error (e.g., show error message)
    });

}

function getDifficultyColor(difficulty) {
    // Ensure difficulty is within expected range (1-5)
    difficulty = Math.max(1, Math.min(difficulty, 5)); 

    // Convert difficulty (1-5) to an appropriate HSL hue (Green → Red)
    const hue = 120 - ((difficulty - 1) / 4) * 120;

    return `hsl(${hue}, 70%, 50%)`; 
}

function updateHealthBar(healthPercentage, difficulty) {
    const difficultyColor = getDifficultyColor(difficulty);
    attackButton.style.background = `linear-gradient(90deg, 
        ${difficultyColor}33 ${healthPercentage}%, 
        rgba(44, 62, 80, 0.9) ${healthPercentage}%)`;
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