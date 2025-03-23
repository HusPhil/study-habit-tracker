let monsters;
let tasks;

document.addEventListener('DOMContentLoaded', () => {
    // Battle elements
    const battleOverlay = document.getElementById('battleOverlay');
    const showBattleBtn = document.getElementById('showBattleBtn');
    const currentEnemy = document.getElementById('currentEnemy');
    const enemyQueue = document.getElementById('enemyQueue');
    const attackButton = document.getElementById('attack-button');

    const observer = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            if (mutation.attributeName === "style") {
                const newDisplay = window.getComputedStyle(battleOverlay).display;
                if (newDisplay === 'none') {
                    stopBattleTimer();
                }       
            }
        }
    });
    
    // Observe only `style` attribute changes
    observer.observe(battleOverlay, { attributes: true, attributeFilter: ["style"] });


    // Game state
    let enemies = [];
    let currentEnemyIndex = 0;
    let isAnimating = false;
    let battleActive = false;

    // Show/Hide battle overlay
    showBattleBtn?.addEventListener('click', () => {
        battleOverlay.style.display = 'flex';
        
        initializeBattle();
    });

    // Close battle when clicking outside
    battleOverlay.addEventListener('click', (e) => {
        e.preventDefault();
    });

    




    let battleTimerInterval = null;

    function startBattleTimer(durationMinutes, timerElement) {
        let duration = durationMinutes * 60;
        let minutes = Math.floor(duration / 60);
        let seconds = duration % 60;
    
        function updateTimer() {
            minutes = Math.floor(duration / 60);    
            seconds = duration % 60;
            timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            duration--;
            if (duration < 0) {
                endBattle();
                stopBattleTimer();
            }
        }    
    
        updateTimer();
        battleTimerInterval = setInterval(updateTimer, 1000);
    }
    
    function stopBattleTimer() {
        if (battleTimerInterval) {
            clearInterval(battleTimerInterval);
            battleTimerInterval = null;
        }
    }

    function initializeBattle(generatedMonsters, battle_duration) {

        monsters = generatedMonsters;
        // get a task from shuffle list
        
        
        attackButton.focus();
        shrinkText(attackButton, attackButton);

        const battleTimer = document.getElementById('battleTimer');
        console.log("battle_duration", battle_duration)

        startBattleTimer(battle_duration, battleTimer);


        resetBattle();
        battleActive = true;
        
        // Set player sprite
        const playerSprite = document.querySelector('.player-character .character-sprite');
        if (playerSprite) {
            playerSprite.style.backgroundImage = "url('/static/assets/images/avatar_icons/players/con1.png')";
        }

        // Generate 3-5 enemies
        const totalEnemies = generatedMonsters.length;
        enemies = []
        for (let i = 0; i < totalEnemies; i++) {
            const enemy = generatedMonsters[i];
            console.log(enemy)
            enemies.push({
                name: enemy.name,
                image: enemy.file_name,
                health: enemy.health,
                maxHealth: enemy.health,
                description: enemy.description
            });
        }

        console.log('Enemies:', enemies);   


        // Create queue indicators
        enemies.forEach((enemy, index) => {
            const indicator = document.createElement('div');
            indicator.className = 'queue-indicator';
            indicator.title = enemy.name;
            enemyQueue.appendChild(indicator);
        });

        showCurrentEnemy();
    }
    

    function shrinkText(container, textElement) {
        let fontSize = 20; // Start with a reasonable default
        textElement.style.fontSize = fontSize + "px";
        console.log(`Initial font size: ${fontSize}px`);
    
        // Create a temporary element for measurement
        const tempElement = document.createElement('div');
        tempElement.style.position = 'absolute';
        tempElement.style.visibility = 'hidden';
        tempElement.style.whiteSpace = 'nowrap';
        tempElement.style.fontSize = fontSize + "px";
        tempElement.textContent = textElement.textContent;
        document.body.appendChild(tempElement);
    
        // Reduce font size if text overflows container
        while ((tempElement.offsetHeight > container.clientHeight || tempElement.offsetWidth > container.clientWidth) && fontSize > 10) {
            fontSize--;
            tempElement.style.fontSize = fontSize + "px";
            textElement.style.fontSize = fontSize + "px";
            console.log(`Adjusted font size: ${fontSize}px, offsetHeight: ${tempElement.offsetHeight}, containerHeight: ${container.clientHeight}, offsetWidth: ${tempElement.offsetWidth}, containerWidth: ${container.clientWidth}`);
        }
    
        // Remove the temporary element
        document.body.removeChild(tempElement);
    
        if (fontSize <= 10) {
            console.warn('Minimum font size reached, text may still overflow.');
        }
    }

    function getDifficultyColor(maxHealth) {
        // Map maxHealth to 1-5 difficulty scale
        const difficulty = maxHealth; // maxHealth should already be 1-5

        // Convert difficulty (1-5) to an appropriate HSL hue (Green → Red)
        // const hue = 120 - ((difficulty - 1) / 4) * 120;

        // Use project's theme colors based on difficulty
        switch(difficulty) {
            case 1: return '#2ecc71'; // Easiest - Success green
            case 2: return '#87D37C'; // Easy-medium - Light green
            case 3: return '#3498db'; // Medium - Interactive blue
            case 4: return '#E87E04'; // Medium-hard - Orange
            case 5: return '#e74c3c'; // Hardest - Accent red
            default: return '#2ecc71'; // Default to success green
        }
    }

    function showCurrentEnemy() {
        if (!enemies[currentEnemyIndex]) return;

        const enemy = enemies[currentEnemyIndex];
        console.log('Current enemy:', enemy);
        const enemySprite = currentEnemy.querySelector('.character-sprite');

        const enemyName = document.querySelector('.enemy-stats .stat-name');
        if (enemyName) {
            enemyName.textContent = enemy.name;
        }

        attackButton.textContent = enemy.description
        shrinkText(attackButton, attackButton);

        if(enemySprite) {
            enemySprite.style.backgroundImage = `url('/static/assets/images/avatar_icons/monsta/${enemy.image}')`;
        }   

        const healthPercentage = (enemy.health / enemy.maxHealth) * 100;
        const difficultyColor = getDifficultyColor(enemy.maxHealth);
        attackButton.style.background = `linear-gradient(90deg, 
            ${difficultyColor}33 ${healthPercentage}%, 
            rgba(44, 62, 80, 0.9) ${healthPercentage}%)`;

        currentEnemy.addEventListener('click', () => {
            if (!isAnimating && battleActive) {
                performAttack();
            }
        });
        
        attackButton.addEventListener('click', () => {
            if (!isAnimating && battleActive) {
                performAttack();
            }
        });
    }

    function performAttack() {
        if (!enemies[currentEnemyIndex]) return;

        isAnimating = true;
        const enemy = enemies[currentEnemyIndex];
        const taskText = attackButton.querySelector('.task-text');
        
        // Player attack animation
        const playerChar = document.querySelector('.player-character');
        playerChar.classList.add('attacking-right');
        
        setTimeout(() => {
            // Enemy takes damage
            enemy.health--;
            
            // Update task text with new health
            if (taskText) {
                taskText.innerHTML = `<span class="enemy-name">${enemy.name}</span> (${enemy.health}/${enemy.maxHealth} HP)`;
                shrinkText(attackButton, taskText); // Shrink text after updating
            }

            // Update health bar in button
            const healthPercentage = (enemy.health / enemy.maxHealth) * 100;
            const difficultyColor = getDifficultyColor(enemy.maxHealth);
            attackButton.style.background = `linear-gradient(90deg, 
                ${difficultyColor}33 ${healthPercentage}%, 
                rgba(44, 62, 80, 0.9) ${healthPercentage}%
            )`;

            // Enemy hit animation
            const enemyChar = currentEnemy;
            enemyChar.classList.add('hit');
            
            setTimeout(() => {
                playerChar.classList.remove('attacking-right');
                enemyChar.classList.remove('hit');
                
                if (enemy.health <= 0) {
                    defeatCurrentEnemy();
                } else {
                    enemyCounterAttack();
                }
            }, 300);
        }, 200);
    }

    function enemyCounterAttack() {
        const enemyChar = currentEnemy;
        enemyChar.classList.add('attacking-left');
        
        setTimeout(() => {
            const playerChar = document.querySelector('.player-character');
            playerChar.classList.add('hit');
            
            setTimeout(() => {
                enemyChar.classList.remove('attacking-left');
                playerChar.classList.remove('hit');
                isAnimating = false;
            }, 300);
        }, 200);
    }

    function defeatCurrentEnemy() {
        const indicators = enemyQueue.children;

        // indicators[currentEnemyIndex].classList.add('defeated');
        indicators[currentEnemyIndex].classList.add('active');

        currentEnemy.classList.add('defeated');

        setTimeout(() => {
            currentEnemyIndex++;
            
            if (currentEnemyIndex < enemies.length) {
                if (indicators[currentEnemyIndex]) {
                    // indicators[currentEnemyIndex].classList.add('active');
                }
                currentEnemy.classList.remove('defeated');
                showCurrentEnemy();
                isAnimating = false;
            } else {
                setTimeout(() => {
                    endBattle();
                }, 500);
            }
        }, 1000);
    }

    function resetBattle() {
        // tasks.sort(() => Math.random() - 0.5);
        enemyQueue.innerHTML = '';
        currentEnemy.classList.remove('hit', 'defeated', 'attacking-left');

        const playerName = document.querySelector('.player-stats .stat-name');
        const playerUsername = document.getElementById('current_username').value;

        console.log(playerUsername, playerName)

        if (playerName) {
            playerName.textContent = playerUsername;
        }
        
        const enemyName = document.querySelector('.enemy-stats .stat-name');
        if (enemyName) {
            enemyName.textContent = "enemy";
        }

        const taskText = attackButton.querySelector('.task-text');
        
        if (taskText) {
            taskText.textContent = 'Start Battle';
        }

        attackButton.style.background = 'rgba(44, 62, 80, 0.9)';
        
        const playerChar = document.querySelector('.player-character');
        if (playerChar) {
            playerChar.classList.remove('attacking-right', 'hit');
        }
        
        enemies = [];
        currentEnemyIndex = 0;
        isAnimating = false;
    }

    function endBattle() {
        remainingEnemies = enemies.length - currentEnemyIndex;
        
        if (remainingEnemies === 0) {
            alert('Victory! All enemies defeated!');
        }

        battleActive = false;
        battleOverlay.style.display = 'none';
        resetBattle();


        fetch(`/api/stop_session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "remaining_enemies": remainingEnemies, "total_enemies": enemies.length })
        })
        .then(response => response.json())  // Convert response to JSON
        .then(async data => {
            console.log("Message:", data.message);  // Extract message
            console.log("Player Stats:", data.player_stats);  // Extract player stats

            // Example: Access specific player stats
            console.log("Player Email:", data.player_stats.email);
            console.log("Player XP:", data.player_stats.exp);
            console.log("Player Level:", data.player_stats.level);
            console.log("Player Title:", data.player_stats.title);
            console.log("Player Badge:", data.default_badge);

            updatePlayerStatsUI(data.player_stats)
            console.log(data.subject_id, typeof data.subject_id)
            await selectOpponent(data.subject_id)

        })
    }   

    function updatePlayerStatsUI({ exp, level, title, username }) {
        const playerTitle = document.getElementById('player-title');
        const playerName = document.getElementById('player-name');
        const playerLevel = document.getElementById('player-level');
        const playerExp = document.getElementById('player-exp');
    
        if (playerTitle) playerTitle.textContent = title;
        if (playerName) playerName.innerHTML = `<strong>Name:</strong> ${username}`;
        if (playerLevel) playerLevel.innerHTML = `<strong>Level:</strong> ${level}`;
        if (playerExp) playerExp.innerHTML = `<strong>Experience:</strong> ${exp}`;
    }
    


    // Expose functions to the global scope
    window.initializeBattle = initializeBattle;
    window.shrinkText = shrinkText;
    window.showCurrentEnemy = showCurrentEnemy;
    window.performAttack = performAttack;
    window.enemyCounterAttack = enemyCounterAttack;
    window.defeatCurrentEnemy = defeatCurrentEnemy;
    window.resetBattle = resetBattle;
    window.endBattle = endBattle;
});