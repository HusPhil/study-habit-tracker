// Battle-related functionality
let selectedSubject = null;

function selectOpponent(subjectId) {
    selectedSubject = subjectId;
    document.querySelectorAll('.subject-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    updateSubjectInfo(subjectId);
}

function updateSubjectInfo(subjectId) {
    // Fetch subject info from backend
    fetch(`/api/subject/${subjectId}`)
        .then(response => response.json())
        .then(data => {
            // Update the UI with subject information
            const subjectInfo = document.getElementById('subject-info');
            if (subjectInfo) {
                subjectInfo.innerHTML = `
                    <div class="subject-ribbon">${data.name}: ${"⭐".repeat(data.difficulty)}</div>
                    <p class="text-info">Won: ${data.wins} | Lost: ${data.losses}</p>
                `;
            }
        });
}

function openBattlePopup() {
    if (!selectedSubject) {
        alert('Please select a subject first!');
        return;
    }
    document.getElementById('battle-popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('battle-popup').style.display = 'none';
}

function startBattle() {
    const selectedQuests = Array.from(document.querySelectorAll('#quest-list-select input:checked'))
        .map(input => input.value);
    
    if (selectedQuests.length === 0) {
        alert('Please select at least one quest!');
        return;
    }

    // Send battle start request to backend
    fetch('/api/battle/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            subjectId: selectedSubject,
            quests: selectedQuests
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle battle start response
        window.location.href = `/battle/${data.battleId}`;
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const battleBtn = document.querySelector('.battle-btn');
    if (battleBtn) {
        battleBtn.addEventListener('click', openBattlePopup);
    }
});