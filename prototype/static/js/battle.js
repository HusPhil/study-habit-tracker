


function startBattle(event) {
    
    event.preventDefault();

    const form = document.getElementById('startBattleForm');
    const formData = new FormData(form);
    const target_url = formData.get("target_url");

    // console.log("Form Data:", );
    // ✅ Extract selected quests
    const battle_duration = formData.get("battle_duration");
    const selectedQuests = formData.getAll("selected_quests");

    selectedQuests.forEach((quest, index) => {
        formData.append(`selected_  quests[${index}]`, quest);
    });
    
    
    console.log("Selected Quests:", selectedQuests);
    console.log("battle_duration:" + battle_duration)

    fetch(target_url, { // Replace with your actual endpoint
        method: 'POST',
        headers: { "Content-Type": "application/json" }, // ✅ Tell Flask to expect JSON
        body: JSON.stringify({
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
        console.log('Success session:', data);
        modalSystem.hide('startBattleModal');
        form.reset();
    })
    .catch((error) => {
        alert('Failed to start session');
        console.error('Error:', error);
        // Handle error (e.g., show error message)
    });

}