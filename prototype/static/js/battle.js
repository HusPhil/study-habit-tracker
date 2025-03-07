// Battle-related functionality
function selectOpponent(subjectId) {
    console.log("selecting opponent");
    selectedSubjectId = subjectId;
    document.querySelectorAll('.subject-card').forEach(card => {
        card.classList.remove('selected');
    });
    selectedSubjectCard = document.querySelector(`[data-subject-id="${selectedSubjectId}"]`);
    
    if(selectedSubjectCard == null) {
        console.error("Document to be selected not found!")
        return
    }
    selectedSubjectCard.classList.add('selected');
    selectedSubjectCodeName = selectedSubjectCard.getAttribute('data-subject-code-name');
    document.getElementById('opponent-title').textContent = `A battle against [${selectedSubjectCodeName}]`;

    updateQuestsUI(selectedSubjectId);

    document.getElementById('modal-indicator-subject-id').value = selectedSubjectId;
}

function checkSubjectAndAddQuest() {
    if (selectedSubjectId != null) {
        addQuest(); // Call the function to open the modal
    } else {
        alert("Please select a subject before adding a quest.");
    }
}