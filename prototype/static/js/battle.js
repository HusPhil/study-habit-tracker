// Battle-related functionality
function selectOpponent(subjectId) {
    console.log("prevSelectedId", selectedSubject);

    selectedSubject = subjectId;
    document.querySelectorAll('.subject-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    
    window.dispatchEvent(new CustomEvent("subjectSelected", { "detail": {
        "subjectId": subjectId,
    } }));
}

function checkSubjectAndAddQuest() {
    if (selectedSubject != null) {
        addQuest(); // Call the function to open the modal
    } else {
        alert("Please select a subject before adding a quest.");
    }
}