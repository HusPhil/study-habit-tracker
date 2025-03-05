// Battle-related functionality
let selectedSubject = null;

function selectOpponent(subjectId) {
    console.log(subjectId);
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
    const popup = document.getElementById('battle-popup');
    popup.classList.add('active');
    // Add fade-in animation
    popup.style.opacity = '0';
    popup.style.display = 'flex';
    setTimeout(() => {
        popup.style.opacity = '1';
    }, 10);
}

function closePopup() {
    const popup = document.getElementById('battle-popup');
    // Add fade-out animation
    popup.style.opacity = '0';
    setTimeout(() => {
        popup.style.display = 'none';
        popup.classList.remove('active');
    }, 300);
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
    })
    .catch(error => {
        console.error('Error starting battle:', error);
        alert('Failed to start battle. Please try again.');
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const battleBtn = document.querySelector('.battle-btn');
    if (battleBtn) {
        battleBtn.addEventListener('click', openBattlePopup);
    }

    // Close popup when clicking outside
    const popup = document.getElementById('battle-popup');
    if (popup) {
        popup.addEventListener('click', (e) => {
            if (e.target === popup) {
                closePopup();
            }
        });
    }

    // Handle escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && popup.classList.contains('active')) {
            closePopup();
        }
    });
});