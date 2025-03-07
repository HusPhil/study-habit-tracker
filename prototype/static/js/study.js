
function addQuest(event) {
    event.preventDefault();
    const form = document.getElementById('addQuestModalForm');
    const formData = new FormData(form); // Gather form data

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
        form.reset();
        modalSystem.hide('addQuestModal');
    })
    .catch((error) => {
        alert('Failed to create quest');
        console.error('Error:', error);
        // Handle error (e.g., show error message)
    });
}

function closeModal() {
    const modal = document.getElementById('addQuestModal'); // Replace with your modal ID
    modal.style.display = 'none'; // Hide the modal
    // Optionally, reset the form
    document.getElementById('addQuestModalForm').reset();
}

async function updateQuestsUI(subjectId) {
    try {
        // ✅ Correctly pass subject_id as a query parameter
        const response = await fetch(`/api/subject/get_quests?subject_id=${encodeURIComponent(subjectId)}`);
        
        if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);

        const quests = await response.json();
        console.log("Loaded quests:", quests);

        const questList = document.getElementById('quest-list');
        
        // ✅ Avoid unnecessary re-rendering by using DocumentFragment
        const fragment = document.createDocumentFragment();
        
        quests.reverse().forEach(quest => {
            const li = document.createElement('li');
            li.innerHTML = `
                <input type="checkbox" id="quest-${quest.id}" ${quest.status ? 'checked' : ''}> 
                ${quest.description}
            `;
            fragment.appendChild(li);
        });

        // ✅ Replace only changed content
        questList.innerHTML = '';
        questList.appendChild(fragment);

    } catch (error) {
        console.error("Failed to load quests:", error);
        alert("Failed to load quests. Please try again.");
    }
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