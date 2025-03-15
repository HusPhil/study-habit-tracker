
function addQuest(event) {
    event.preventDefault();
    const form = document.getElementById('addQuestModalForm');
    const formData = new FormData(form);
    const prevSelectedId = formData.get("subject_id")
    // Send POST request
    fetch('/api/quest/create', { // Replace with your actual endpoint
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse JSON response
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log('Success:', data);
        updateQuestsUI(data.subject_id);
        updateSubjectsUI();
        selectOpponent(prevSelectedId);
        // ✅ Wait for UI updates before re-selecting subject
        waitForElementUpdate('#subject-cards', () => {
            selectOpponent(prevSelectedId);
        });
        modalSystem.hide('addQuestModal');
        form.reset();
    })
    .catch((error) => {
        alert('Failed to create quest');
        console.error('Error:', error);
        // Handle error (e.g., show error message)
    });
}

async function updateQuestsUI(subjectId) {
    try {
        const response = await fetch(`/api/subject/get_quests?subject_id=${encodeURIComponent(subjectId)}`);
        if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);

        const quests = await response.json();
        const questList = document.getElementById('quest-list');
        selectedSubjectQuests = quests;
        const fragment = document.createDocumentFragment();
                function getDifficultyColor(difficulty) {
                    // ✅ Ensure difficulty is within expected range (1-5)
                    difficulty = Math.max(1, Math.min(difficulty, 5)); 
                
                    // ✅ Convert difficulty (1-5) to an appropriate HSL hue (Green → Red)
                    const hue = 120 - ((difficulty - 1) / 4) * 120;
                
                    return `hsl(${hue}, 70%, 50%)`; // ✅ Returns color from Green (easy) to Red (hard)
                }

                quests.reverse().forEach(quest => {
                    const li = document.createElement('li');
                    li.className = 'quest-item';
                    li.style.cssText = `
                        transition: border-color 0.3s ease;
                        margin: 5px 0;
                        padding: 8px;
                        border-radius: 4px;
                        background: rgba(255, 255, 255, 0.05);
                        border-left: 4px solid ${getDifficultyColor(quest.difficulty)};
                    `;
                    li.innerHTML = `
                        <div class="quest-content">
                            <button class="quest-menu-btn" aria-label="Quest options">
                                <i class="fas fa-ellipsis-vertical"></i>
                            </button>
                            <span class="quest-text">${quest.description}</span>
                        </div>
                    `;
                    fragment.appendChild(li);
                });

        questList.innerHTML = '';
        questList.appendChild(fragment);

    } catch (error) {
        console.error("Failed to load quests:", error);
        alert("Failed to load quests. Please try again.");
    }
}

function loadBattleModalQuests() {
    const questList = document.getElementById('battle-quest-list');
    const fragment = document.createDocumentFragment();
    
    selectedSubjectQuests.forEach(quest => {
        const li = document.createElement('li');
        li.className = 'quest-item';
        li.innerHTML = `
            <div class="quest-content">
                <input type="checkbox" 
                name="selected_quests" 
                value="${quest.id}" 
                data-difficulty="${quest.difficulty}">
                <input type="hidden" name="quest_difficulty_${quest.id}" value="${quest.difficulty}">
                <input type="hidden" name="quest_description_${quest.id}" value="${quest.description}">
                <span class="quest-text">${quest.description}</span>
            </div>
        `;
        fragment.appendChild(li);
    });

    questList.innerHTML = '';
    questList.appendChild(fragment);
}

async function updateSubjectsUI() {
    try {
        // ✅ Fetch updated subject list
        const user_id = document.getElementById('current_user_id').value;
        const response = await fetch(`/api/subject/get_all_by_user_id?user_id=${encodeURIComponent(user_id)}`);
        if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);

        const subjects = await response.json();
        console.log("Updated subjects:", subjects);

        // ✅ Select the container and clear it
        const subjectCardsContainer = document.getElementById("subject-cards");
        subjectCardsContainer.innerHTML = ""; 

        // ✅ Efficiently rebuild subject cards using DocumentFragment
        const fragment = document.createDocumentFragment();

        subjects.forEach(subject => {
            // ✅ Create the main subject card div
            const subjectCard = document.createElement("div");
            subjectCard.classList.add("subject-card");
            subjectCard.dataset.subjectId = subject.id;
            subjectCard.dataset.subjectCodeName = subject.code_name;
            subjectCard.onclick = () => selectOpponent(subject.id);

            // ✅ Add subject name
            const subjectName = document.createElement("div");
            subjectName.classList.add("subject-name");
            subjectName.textContent = subject.code_name;

            // ✅ Add difficulty stars
            const difficultyStars = document.createElement("div");
            difficultyStars.classList.add("difficulty-stars");
            difficultyStars.textContent = "⭐".repeat(subject.difficulty);

            // ✅ Create stats container
            const subjectStats = document.createElement("div");
            subjectStats.classList.add("subject-stats");

            // ✅ Helper function to add a stat row
            function addStatRow(label, value) {
                const statRow = document.createElement("div");
                statRow.classList.add("stat-row");
                statRow.innerHTML = `<span class="stat-label">${label}</span> <span class="stat-value">${value}</span>`;
                subjectStats.appendChild(statRow);
            }

            // ✅ Add stats
            addStatRow("Notes", subject.notes.length);
            addStatRow("Flashcards", subject.flashcards.length);
            addStatRow("Quests", subject.quests.length);
            if (subject.last_battle) {
                addStatRow("Last Battle", subject.last_battle);
            }

            // ✅ Append all elements to subject card
            subjectCard.appendChild(subjectName);
            subjectCard.appendChild(difficultyStars);
            subjectCard.appendChild(subjectStats);

            // ✅ Append the subject card to the fragment
            fragment.appendChild(subjectCard);
        });

        // ✅ Create and add "Add Subject" button **outside the loop**
        const addSubjectCard = document.createElement("div");
        addSubjectCard.classList.add("subject-card", "add-subject-card");
        addSubjectCard.setAttribute("data-dialog-target", "addSubjectModal");

        const addIcon = document.createElement("div");
        addIcon.classList.add("add-icon");
        addIcon.innerHTML = `<i class="fas fa-scroll"></i>`;

        const addSubjectName = document.createElement("div");
        addSubjectName.classList.add("subject-name");
        addSubjectName.textContent = "New Subject";

        // ✅ Append elements to "Add Subject" button
        addSubjectCard.appendChild(addIcon);
        addSubjectCard.appendChild(addSubjectName);

        // ✅ Append the "Add Subject" button to the fragment
        fragment.appendChild(addSubjectCard);

        // ✅ Efficiently append all subject cards at once
        subjectCardsContainer.appendChild(fragment);

        modalSystem.init()

    } catch (error) {
        console.error("Failed to update subjects UI:", error);
        alert("Failed to load subjects. Please try again.");
    }
}



function waitForElementUpdate(selector, callback) {
    const targetNode = document.querySelector(selector);

    if (!targetNode) {
        console.warn(`❌ Element not found: ${selector}`);
        return;
    }

    const observer = new MutationObserver((mutationsList, observer) => {
        console.log("✅ DOM changes detected!");
        observer.disconnect(); // Stop observing once changes are detected
        callback(); // Execute the callback function
    });

    observer.observe(targetNode, { childList: true, subtree: true });
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