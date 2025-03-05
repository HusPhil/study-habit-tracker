// Study zone functionality
function addQuest() {
    const input = document.getElementById('quest-text-input');
    const questText = input.value.trim();
    
    if (!questText) return;

    fetch('/api/quests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: questText })
    })
    .then(response => response.json())
    .then(quest => {
        const questList = document.getElementById('quest-list');
        const li = document.createElement('li');
        li.innerHTML = `
            <input type="checkbox" id="quest-${quest.id}">
            <span>${quest.description}</span>
        `;
        questList.appendChild(li);
        input.value = '';
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