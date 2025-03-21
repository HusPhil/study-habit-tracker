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
        // updateQuestsUI(data.subject_id);
        // updateSubjectsUI();
        selectOpponent(prevSelectedId);
        // Wait for UI updates before re-selecting subject
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
        console.log(response)

        const quests = await response.json();
        const questList = document.getElementById('quest-list');
        selectedSubjectQuests = quests;
        const fragment = document.createDocumentFragment();
                function getDifficultyColor(difficulty) {
                    // Ensure difficulty is within expected range (1-5)
                    difficulty = Math.max(1, Math.min(difficulty, 5)); 
                
                    // Convert difficulty (1-5) to an appropriate HSL hue (Green → Red)
                    const hue = 120 - ((difficulty - 1) / 4) * 120;
                
                    return `hsl(${hue}, 70%, 50%)`; // Returns color from Green (easy) to Red (hard)
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

async function updateFlashcardsUI(subjectId) {
    try {
        const response = await fetch(`/api/subject/get_flashcards?subject_id=${encodeURIComponent(subjectId)}`);
        const flashcards = await response.json();
        console.log("Updated flashcards:", flashcards);
        const flashcardList = document.getElementById('flashcard-list');
        flashcardList.style.listStyle = 'none';
        flashcardList.style.padding = '0';
        const fragment = document.createDocumentFragment();

        flashcards.reverse().forEach(flashcard => {
            const li = document.createElement('li');
            li.className = 'flashcard-item';
            li.style.cssText = `
                transition: all 0.3s ease;
                margin: 10px 0;
                padding: 15px;
                border-radius: 8px;
                background: rgba(44, 62, 80, 0.9);
                border: 2px solid #34495e;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                color: #ecf0f1;
                font-family: 'MedievalSharp', cursive;
            `;

            li.innerHTML = `
                <div class="flashcard-content">
                    <button class="flashcard-menu-btn" aria-label="Flashcard options" style="
                        background: none;
                        border: none;
                        color: #3498db;
                        cursor: pointer;
                        float: right;
                        padding: 5px;
                    ">
                        <i class="fas fa-ellipsis-vertical"></i>
                    </button>
                    <span class="flashcard-text">${flashcard.description}</span>
                    ${flashcard.link ? `<div class="flashcard-link" style="
                        margin-top: 8px;
                        font-size: 0.9em;
                        color: #3498db;
                    "><i class="fas fa-link"></i> Study Resource</div>` : ''}
                </div>
            `;

            if (flashcard.link) {
                li.addEventListener('click', (e) => {
                    if (!e.target.closest('.flashcard-menu-btn')) {
                        window.open(flashcard.link, '_blank');
                    }
                });

                li.addEventListener('mouseenter', () => {
                    li.style.transform = 'translateY(-2px)';
                    li.style.borderColor = '#3498db';
                    li.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)';
                });

                li.addEventListener('mouseleave', () => {
                    li.style.transform = 'translateY(0)';
                    li.style.borderColor = '#34495e';
                    li.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';
                });
            }

            fragment.appendChild(li);
        });

        flashcardList.innerHTML = '';
        flashcardList.appendChild(fragment);

    } catch (error) {
        console.error("Failed to load flashcards:", error);
        alert("Failed to load flashcards. Please try again.");
    }
}

async function updateNotesUI(subjectId) {
    try {
        const response = await fetch(`/api/subject/get_notes?subject_id=${encodeURIComponent(subjectId)}`);
        const notes = await response.json();
        console.log("Updated notes:", notes);
        
        const notesList = document.getElementById('note-list');
        notesList.style.listStyle = 'none';
        notesList.style.padding = '0';
        const fragment = document.createDocumentFragment();

        notes.reverse().forEach(note => {
            const li = document.createElement('li');
            li.className = 'note-item';
            li.style.cssText = `
                transition: all 0.3s ease;
                margin: 10px 0;
                padding: 15px;
                border-radius: 8px;
                background: rgba(44, 62, 80, 0.9);
                border: 2px solid #34495e;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                color: #ecf0f1;
                font-family: 'MedievalSharp', cursive;
            `;

            li.innerHTML = `
                <div class="note-content">
                    <button class="note-menu-btn" aria-label="Note options" style="
                        background: none;
                        border: none;
                        color: #3498db;
                        cursor: pointer;
                        float: right;
                        padding: 5px;
                    ">
                        <i class="fas fa-ellipsis-vertical"></i>
                    </button>
                    <span class="note-text">${note.description}</span>
                    ${note.link ? `<div class="note-link" style="
                        margin-top: 8px;
                        font-size: 0.9em;
                        color: #3498db;
                    "><i class="fas fa-link"></i> Study Resource</div>` : ''}
                </div>
            `;

            if (note.link) {
                li.addEventListener('click', (e) => {
                    if (!e.target.closest('.note-menu-btn')) {
                        window.open(note.link, '_blank');
                    }
                });

                li.addEventListener('mouseenter', () => {
                    li.style.transform = 'translateY(-2px)';
                    li.style.borderColor = '#3498db';
                    li.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)';
                });

                li.addEventListener('mouseleave', () => {
                    li.style.transform = 'translateY(0)';
                    li.style.borderColor = '#34495e';
                    li.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';
                });
            }

            fragment.appendChild(li);
        });

        notesList.innerHTML = '';
        notesList.appendChild(fragment);

    } catch (error) {
        console.error("Failed to load notes:", error);
        alert("Failed to load notes. Please try again.");
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
        // Get user ID safely
        const userInput = document.getElementById('current_user_id');
        if (!userInput) throw new Error("User ID input field not found");

        const user_id = userInput.value.trim();
        if (!user_id) throw new Error("User ID is missing");

        // Fetch updated subject list
        const response = await fetch(`/api/subject/get_all_by_user_id?user_id=${encodeURIComponent(user_id)}`);
        if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);

        const subjects = await response.json();
        console.log("Updated subjects:", subjects);

        console.log(subjects[0])

        // Select the container and clear it
        const subjectCardsContainer = document.getElementById("subject-cards");
        if (!subjectCardsContainer) throw new Error("Subject cards container not found");

        subjectCardsContainer.innerHTML = ""; // Clear existing subjects

        // Efficiently rebuild subject cards using DocumentFragment
        const fragment = document.createDocumentFragment();

        subjects.forEach(subject => {
            // Create the main subject card div
            const subjectCard = document.createElement("div");
            subjectCard.classList.add("subject-card");
            subjectCard.dataset.subjectId = subject.id;
            subjectCard.dataset.subjectCodeName = subject.code_name;
            subjectCard.onclick = () => selectOpponent(subject.id);

            // Add subject name
            const subjectName = document.createElement("div");
            subjectName.classList.add("subject-name");
            subjectName.textContent = subject.code_name;

            // Add difficulty stars
            const difficultyStars = document.createElement("div");
            difficultyStars.classList.add("difficulty-stars");
            difficultyStars.textContent = "★".repeat(subject.difficulty); // ✅ Corrected star rendering

            // Create stats container
            const subjectStats = document.createElement("div");
            subjectStats.classList.add("subject-stats");

            // Helper function to add a stat row
            function addStatRow(label, value) {
                const statRow = document.createElement("div");
                statRow.classList.add("stat-row");
                statRow.innerHTML = `<span class="stat-label">${label}</span> <span class="stat-value">${value}</span>`;
                subjectStats.appendChild(statRow);
            }

            // Add stats

            addStatRow("Notes", subject.notes?.length || 0);
            addStatRow("Flashcards", subject.flashcards?.length || 0);
            addStatRow("Quests", subject.quests?.length || 0);
            if (subject.last_battle) {
                addStatRow("Last Battle", subject.last_battle);
            }

            // Append all elements to subject card
            subjectCard.appendChild(subjectName);
            subjectCard.appendChild(difficultyStars);
            subjectCard.appendChild(subjectStats);

            // Append the subject card to the fragment
            fragment.appendChild(subjectCard);
        });

        // Create and add "Add Subject" button **outside the loop**
        const addSubjectCard = document.createElement("div");
        addSubjectCard.classList.add("subject-card", "add-subject-card");
        addSubjectCard.setAttribute("data-dialog-target", "addSubjectModal");

        const addIcon = document.createElement("div");
        addIcon.classList.add("add-icon");
        addIcon.innerHTML = `<i class="fas fa-scroll"></i>`;

        const addSubjectName = document.createElement("div");
        addSubjectName.classList.add("subject-name");
        addSubjectName.textContent = "New Subject";

        // Append elements to "Add Subject" button
        addSubjectCard.appendChild(addIcon);
        addSubjectCard.appendChild(addSubjectName);

        // Append the "Add Subject" button to the fragment
        fragment.appendChild(addSubjectCard);

        // Efficiently append all subject cards at once
        subjectCardsContainer.appendChild(fragment);

        // Ensure modalSystem exists before calling it
        if (typeof modalSystem !== "undefined" && modalSystem.init) {
            modalSystem.init();
        } else {
            console.warn("modalSystem is not available");
        }

    } catch (error) {
        console.error("Failed to update subjects UI:", error);
        alert(error.message || "Failed to load subjects. Please try again.");
    }
}




function waitForElementUpdate(selector, callback) {
    const targetNode = document.querySelector(selector);

    if (!targetNode) {
        console.warn(` Element not found: ${selector}`);
        return;
    }

    const observer = new MutationObserver((mutationsList, observer) => {
        console.log(" DOM changes detected!");
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