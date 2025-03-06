function addQuest() {
    if (!selectedSubject) {
        showError('Please select a subject first!');
        return;
    }
    
    // Remove any existing popup
    const existingPopup = document.getElementById('quest-popup');
    if (existingPopup) {
        existingPopup.remove();
    }
    
    // Create and show popup
    const popup = document.createElement('div');
    popup.className = 'popup-overlay';
    popup.id = 'quest-popup';
    popup.innerHTML = `
        <div class="quest-popup">
            <h2>Create New Quest</h2>
            <div class="quest-form">
                <div class="form-group">
                    <label for="quest-description">Quest Description</label>
                    <input type="text" id="quest-description" placeholder="Enter quest description..." autofocus>
                </div>
                <div class="form-group">
                    <label for="quest-difficulty">Difficulty</label>
                    <select id="quest-difficulty">
                        <option value="1">Easy ⭐</option>
                        <option value="2">Medium ⭐⭐</option>
                        <option value="3">Hard ⭐⭐⭐</option>
                        <option value="4">Expert ⭐⭐⭐⭐</option>
                        <option value="5">Master ⭐⭐⭐⭐⭐</option>
                    </select>
                </div>
                <div class="button-group">
                    <button onclick="closeQuestPopup()" class="cancel-btn">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                    <button onclick="createQuest()" class="create-btn">
                        <i class="fas fa-plus-circle"></i> Create Quest
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    // Add fade-in animation
    requestAnimationFrame(() => {
        popup.style.opacity = '1';
    });
    
    // Setup event listeners
    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            closeQuestPopup();
        }
    });
    
    // Focus on input after animation
    setTimeout(() => {
        const input = document.getElementById('quest-description');
        if (input) input.focus();
    }, 300);
    
    // Handle enter key
    const questInput = document.getElementById('quest-description');
    if (questInput) {
        questInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                createQuest();
            }
        });
    }
}

function closeQuestPopup() {
    const popup = document.getElementById('quest-popup');
    if (popup) {
        popup.style.opacity = '0';
        setTimeout(() => {
            popup.remove();
        }, 300);
    }
}

function createQuest() {
    const description = document.getElementById('quest-description').value.trim();
    const difficulty = parseInt(document.getElementById('quest-difficulty').value);
    
    if (!description) {
        showError('Please enter a quest description');
        return;
    }
    
    // Send quest creation request to backend
    fetch('/api/quest/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description,
            difficulty,
            subject_id: selectedSubject
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data["status"] != 200) {
            showError("Something went wrong with the server. Please try again.");
            return;
        }
        closeQuestPopup();
        updateSubjectInfo(selectedSubject); // Refresh quest list
        showSuccess('Quest created successfully!');
    })
    .catch(error => {
        console.error('Error creating quest:', error);
        showError('Failed to create quest. Please try again.');
    });
}

function addTome() {
    const input = document.getElementById('note-text-input');
    const tomeUrl = input.value.trim();
    
    if (!tomeUrl) return;

    fetch('/api/tomes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: tomeUrl })
    })
    .then(response => response.json())
    .then(tome => {
        const tomesList = document.getElementById('tomes-list');
        const li = document.createElement('li');
        li.innerHTML = `<a href="${tome.url}" target="_blank">${tome.title}</a>`;
        tomesList.appendChild(li);
        input.value = '';
    });
}

function addCrystal() {
    const input = document.getElementById('flashcard');
    const crystalUrl = input.value.trim();
    
    if (!crystalUrl) return;

    fetch('/api/crystals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: crystalUrl })
    })
    .then(response => response.json())
    .then(crystal => {
        const crystalsList = document.getElementById('crystals-list');
        const li = document.createElement('li');
        li.innerHTML = `<a href="${crystal.url}" target="_blank">${crystal.title}</a>`;
        crystalsList.appendChild(li);
        input.value = '';
    });
}

// Handle quest completion
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('quest-list').addEventListener('change', (e) => {
        if (e.target.type === 'checkbox') {
            const questId = e.target.id.replace('quest-', '');
            const completed = e.target.checked;
            
            fetch(`/api/quests/${questId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ completed })
            });
        }
    });

    // Add event listeners for the add buttons
    document.querySelectorAll('.input-group button').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.textContent.toLowerCase();
            if (action.includes('quest')) addQuest();
            else if (action.includes('tome')) addTome();
            else if (action.includes('crystal')) addCrystal();
        });
    });
});