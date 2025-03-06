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

function getStatusClass(status) {
    switch(status) {
        case 0: return 'not-started';
        case 1: return 'in-progress';
        case 2: return 'completed';
        default: return 'not-started';
    }
}

function getStatusIcon(status) {
    switch(status) {
        case 0: return '<i class="fas fa-circle"></i>';
        case 1: return '<i class="fas fa-spinner fa-spin"></i>';
        case 2: return '<i class="fas fa-check-circle"></i>';
        default: return '<i class="fas fa-circle"></i>';
    }
}

function updateSubjectInfo(subjectId) {
    fetch(`/api/get_subject?subject_id=${subjectId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const subjectInfo = document.getElementById('subject-info');
            const questList = document.getElementById('quest-list');
            
            if (subjectInfo) {
                subjectInfo.innerHTML = `
                    <div class="subject-ribbon">${data.subject.name}: ${"⭐".repeat(data.subject.difficulty)}</div>
                    <p class="text-info">Won: ${data.subject.wins} | Lost: ${data.subject.losses}</p>
                `;
            }
            
            if (questList) {
                // Clear existing quests
                questList.innerHTML = '';
                
                // Add each quest to the list
                data.subject.quests.forEach(quest => {
                    const li = document.createElement('li');
                    li.className = `quest-item ${getStatusClass(quest.status)}`;
                    
                    const description = document.createElement('div');
                    description.className = 'quest-description';
                    description.textContent = quest.description;
                    
                    const difficulty = document.createElement('div');
                    difficulty.className = 'quest-difficulty';
                    difficulty.innerHTML = `<i class="fas fa-star"></i> ${quest.difficulty}`;
                    
                    const statusBtn = document.createElement('button');
                    statusBtn.className = 'status-btn';
                    statusBtn.innerHTML = getStatusIcon(quest.status);
                    statusBtn.onclick = () => toggleQuestStatus(quest.id, quest.status);
                    statusBtn.title = 'Toggle Status';
                    
                    const actionsDiv = document.createElement('div');
                    actionsDiv.className = 'quest-actions';
                    
                    const editBtn = document.createElement('button');
                    editBtn.className = 'edit-btn';
                    editBtn.innerHTML = '<i class="fas fa-edit"></i>';
                    editBtn.onclick = () => editQuest(quest.id);
                    editBtn.title = 'Edit Quest';
                    
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'delete-btn';
                    deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
                    deleteBtn.onclick = () => deleteQuest(quest.id);
                    deleteBtn.title = 'Delete Quest';
                    
                    actionsDiv.appendChild(statusBtn);
                    actionsDiv.appendChild(editBtn);
                    actionsDiv.appendChild(deleteBtn);
                    
                    li.appendChild(description);
                    li.appendChild(difficulty);
                    li.appendChild(actionsDiv);
                    questList.appendChild(li);
                });
                
                // Update quest count
                updateQuestCount();
            }
        })
        .catch(error => {
            console.error('Error fetching subject:', error);
            showError('Failed to load quests. Please try again.');
        });
}

function toggleQuestStatus(questId, currentStatus) {
    // Cycle through status: 0 -> 1 -> 2 -> 0
    const newStatus = (currentStatus + 1) % 3;
    
    fetch(`/api/quest/update_status/${questId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        updateSubjectInfo(selectedSubject);
        showSuccess('Quest status updated!');
    })
    .catch(error => {
        console.error('Error updating quest status:', error);
        showError('Failed to update quest status. Please try again.');
    });
}

function updateQuestCount() {
    const questList = document.getElementById('quest-list');
    const questCount = document.querySelector('.quest-count');
    const emptyState = document.getElementById('empty-quest-list');
    
    if (questCount && questList) {
        const activeQuests = questList.children.length;
        questCount.textContent = `${activeQuests} Active`;
        
        // Show/hide empty state
        if (emptyState) {
            emptyState.style.display = activeQuests === 0 ? 'flex' : 'none';
        }
    }
}

function editQuest(questId) {
    // TODO: Implement quest editing
    showError('Quest editing coming soon!');
}

function deleteQuest(questId) {
    if (confirm('Are you sure you want to delete this quest?')) {
        fetch(`/api/quest/delete/${questId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            updateSubjectInfo(selectedSubject);
            showSuccess('Quest deleted successfully!');
        })
        .catch(error => {
            console.error('Error deleting quest:', error);
            showError('Failed to delete quest. Please try again.');
        });
    }
}

function toggleQuest(questId, completed) {
    // TODO: Implement quest completion API call
    console.log(`Quest ${questId} ${completed ? 'completed' : 'uncompleted'}`);
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

function updateSubjectCards() {
    fetch('/api/subjects')
        .then(response => response.json())
        .then(data => {
            const subjectCards = document.getElementById('subject-cards');
            if (!subjectCards) return;
            
            subjectCards.innerHTML = '';
            
            data.subjects.forEach(subject => {
                const card = document.createElement('div');
                card.className = 'subject-card';
                card.onclick = () => selectOpponent(subject.id);
                
                card.innerHTML = `
                    <div class="subject-name">${subject.name}</div>
                    <div class="difficulty-stars">${"⭐".repeat(subject.difficulty)}</div>
                    <div class="subject-stats">
                        <div class="stat-row">
                            <span class="stat-label">Notes</span>
                            <span class="stat-value">${subject.notes.length}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Flashcards</span>
                            <span class="stat-value">${subject.flashcards.length}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Quests</span>
                            <span class="stat-value">${subject.quests.length}</span>
                        </div>
                        ${subject.last_battle ? `
                        <div class="stat-row">
                            <span class="stat-label">Last Battle</span>
                            <span class="stat-value">${new Date(subject.last_battle).toLocaleDateString()}</span>
                        </div>
                        ` : ''}
                    </div>
                `;
                
                subjectCards.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error updating subject cards:', error);
            showError('Failed to update subject cards');
        });
}

// Error and Success Messages
function showError(message) {
    // TODO: Implement error toast notification
    alert(message);
}

function showSuccess(message) {
    // TODO: Implement success toast notification
    console.log(message);
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

// Add event listener for quest creation success
window.addEventListener('questCreated', () => {
    updateSubjectCards();
});