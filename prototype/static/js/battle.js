// Battle-related functionality
function selectOpponent(subjectId) {
    console.log("prevSelectedId", selectedSubjectId);

    selectedSubjectId = subjectId;
    document.querySelectorAll('.subject-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    selectedSubjectCodeName = event.currentTarget.getAttribute('data-subject-code-name');
    
    console.log("selectedSubjectCodeName", selectedSubjectCodeName);
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