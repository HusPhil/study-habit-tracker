document.addEventListener('DOMContentLoaded', () => {
    // Battle elements
    const battleOverlay = document.getElementById('battleOverlay');
    const showBattleBtn = document.getElementById('showBattleBtn');
    const currentEnemy = document.getElementById('currentEnemy');
    const enemyQueue = document.getElementById('enemyQueue');

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
    
    // ✅ Observe only `style` attribute changes
    observer.observe(battleOverlay, { attributes: true, attributeFilter: ["style"] });


    // Available monster images and names
    const monsters = {
        'abyssal_fiend.png': 'Abyssal Fiend',
        'ancient_dragon.png': 'Ancient Dragon',
        'berserker_dwarf.png': 'Berserker Dwarf',
        'bone_harbinger.png': 'Bone Harbinger',
        'crimson_imp.png': 'Crimson Imp',
        'dark_raven.png': 'Dark Raven',
        'demon_warrior.png': 'Demon Warrior',
        'djinn_mystic.png': 'Djinn Mystic',
        'eclipse_phantom.png': 'Eclipse Phantom',
        'flame_serpent.png': 'Flame Serpent',
        'forest_beast.png': 'Forest Beast',
        'golden_devourer.png': 'Golden Devourer',
        'hellhound.png': 'Hellhound',
        'infernal_juggernaut.png': 'Infernal Juggernaut',
        'mad_orc.png': 'Mad Orc',
        'medusa_enchantress.png': 'Medusa Enchantress',
        'nosferos.png': 'Nosferos',
        'obsidian_warlord.png': 'Obsidian Warlord',
        'shadow_striker.png': 'Shadow Striker',
        'skeletal_spearman.png': 'Skeletal Spearman',
        'skull_inferno.png': 'Skull Inferno',
        'snow_yeti.png': 'Snow Yeti',
        'venom_cobra.png': 'Venom Cobra',
        'wyrmling_drake.png': 'Wyrmling Drake'
    };

    const monsterImages = Object.keys(monsters);

    let tasks = [
        "Design and develop a complete object-oriented architecture for a complex system using inheritance, polymorphism, and encapsulation principles", // Very long
        "Create a simple class definition", // Medium
        "Study list methods in Python", // Medium
        "Code", // Very short
        "Test", // Very short
        "Create an extensive unit test suite that covers all edge cases and potential scenarios while maintaining proper test documentation", // Very long
        "Debug", // Very short
        "Review Python decorators", // Medium
        "Test", // Very short
        "Practice list comprehensions", // Medium
        "Implement a complete database migration system with rollback capabilities and proper version control integration", // Very long
        "Code", // Very short
        "Study generators in Python", // Medium
        "Create a comprehensive documentation system that includes API references, usage examples, and troubleshooting guides", // Very long
        "Debug", // Very short
        "Learn about virtual environments", // Medium
        "Develop a full-featured REST API with authentication, rate limiting, and comprehensive swagger documentation", // Very long
        "Test", // Very short
        "Practice string methods", // Medium
        "Build an advanced caching system with multiple storage backends and intelligent cache invalidation strategies", // Very long
        "Write a basic Python function", // Medium
        "Master advanced Python concepts including metaclasses, descriptors, and context managers while building practical examples for each concept", // Very long
        "Debug", // Very short
        "Long Implement comprehensive error handling and logging mechanisms in your Python application while following best practices and industry standards Implement comprehensive error handling and logging mechanisms in your Python application while following best practices and industry standards", // Very long
    ]
     
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

    

    function getRandomMonster() {
        const image = monsterImages[Math.floor(Math.random() * monsterImages.length)];
        return {
            image: image,
            name: monsters[image]
        };
    }

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

    function initializeBattle() {
        // get a task from shuffle list
        const taskDescription = document.getElementById('taskDescription');
        taskDescription.focus();
        taskDescription.textContent = tasks.pop();
        shrinkText(taskDescription, taskDescription);

        const durationMinutes = 30;
        const battleTimer = document.getElementById('battleTimer');

        startBattleTimer(durationMinutes, battleTimer);


        resetBattle();
        battleActive = true;
        
        // Set player sprite
        const playerSprite = document.querySelector('.player-character .character-sprite');
        if (playerSprite) {
            playerSprite.style.backgroundImage = "url('/static/assets/images/avatar_icons/players/con1.png')";
        }

        // Generate 3-5 enemies
        const totalEnemies = Math.floor(Math.random() * 3) + 3;
        enemies = Array.from({ length: totalEnemies }, () => {
            const monster = getRandomMonster();
            return {
                health: Math.floor(Math.random() * 3) + 3,
                maxHealth: Math.floor(Math.random() * 3) + 3,
                image: monster.image,
                name: monster.name
            };
        });

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

    function showCurrentEnemy() {
        if (!enemies[currentEnemyIndex]) return;

        const enemy = enemies[currentEnemyIndex];
        const enemySprite = currentEnemy.querySelector('.character-sprite');

        const enemyName = document.querySelector('.enemy-stats .stat-name');
        if (enemyName) {
            enemyName.textContent = enemy.name;
        }
        
        const taskDescription = document.getElementById('taskDescription');
        taskDescription.textContent = tasks.pop()
        shrinkText(taskDescription, taskDescription);

        if(enemySprite) {
            enemySprite.style.backgroundImage = `url('/static/assets/images/avatar_icons/monsta/${enemy.image}')`;
        }   

        const healthPercentage = (enemy.health / enemy.maxHealth) * 100;
        taskDescription.style.background = `linear-gradient(90deg, 
            rgba(231, 76, 60, 0.3) ${healthPercentage}%, 
            rgba(44, 62, 80, 0.9) ${healthPercentage}% )`;

        currentEnemy.addEventListener('click', () => {
            if (!isAnimating && battleActive) {
                performAttack();
            }
        });

        document.addEventListener('keydown', (event) => {
            event.stopPropagation();
            if (event.key === " " && !isAnimating && battleActive) {
                performAttack();
            }
        });
        
        taskDescription.addEventListener('click', () => {
            if (!isAnimating && battleActive) {
                performAttack();
            }
        });
    }

    function performAttack() {
        if (!enemies[currentEnemyIndex]) return;

        isAnimating = true;
        const enemy = enemies[currentEnemyIndex];
        const taskDescription = document.getElementById('taskDescription');
        const taskText = taskDescription.querySelector('.task-text');
        
        // Player attack animation
        const playerChar = document.querySelector('.player-character');
        playerChar.classList.add('attacking-right');
        
        setTimeout(() => {
            // Enemy takes damage
            enemy.health--;
            
            // Update task text with new health
            if (taskText) {
                taskText.innerHTML = `<span class="enemy-name">${enemy.name}</span> (${enemy.health}/${enemy.maxHealth} HP)`;
                shrinkText(taskDescription, taskText); // Shrink text after updating
            }

            // Update health bar in button
            const healthPercentage = (enemy.health / enemy.maxHealth) * 100;
            taskDescription.style.background = `linear-gradient(90deg, 
                rgba(231, 76, 60, 0.3) ${healthPercentage}%, 
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

    // Badge stuff
    function dropBage(enemy) {
        if (enemy.health <= 0) {
            return { title: "Dragon Slayer", rarity: "legendary" };
        }
        return null;
    }

    function handleBadgeDrop(enemy) {
        const badge = dropBage(enemy);
        if (badge) {
            console.log(`You got a ${badge.rarity} badge: ${badge.title}`);
            fetch('/enemy/drop_badge', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: playerId,
                    title: badge.title,
                    rarity: badge.rarity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Failed to add badge to player:', data.error);
                } else {
                    console.log('Badge added to player successfully:', data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }

    function defeatCurrentEnemy() {
        const indicators = enemyQueue.children;

        // indicators[currentEnemyIndex].classList.add('defeated');
        indicators[currentEnemyIndex].classList.add('active');

        currentEnemy.classList.add('defeated');
        handleBadgeDrop(enemies[currentEnemyIndex]);
        // Drop item


        setTimeout(() => {
            currentEnemyIndex++;
            
            if (currentEnemyIndex < enemies.length) {
                if (indicators[currentEnemyIndex]) {
                    // indicators[currentEnemyIndex].classList.add('active');
                }
                currentEnemy.classList.remove('defeated');
                // drop item
                showCurrentEnemy();
                isAnimating = false;
            } else {
                setTimeout(() => {
                    endBattle(true);
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

        const taskDescription = document.getElementById('taskDescription');
        const taskText = taskDescription.querySelector('.task-text');
        
        if (taskText) {
            taskText.textContent = 'Start Battle';
        }

        taskDescription.style.background = 'rgba(44, 62, 80, 0.9)';
        
        const playerChar = document.querySelector('.player-character');
        if (playerChar) {
            playerChar.classList.remove('attacking-right', 'hit');
        }
        
        enemies = [];
        currentEnemyIndex = 0;
        isAnimating = false;
    }

    function endBattle(victory = false) {
        if (victory) {
            alert('Victory! All enemies defeated!');
        }
        battleActive = false;
        battleOverlay.style.display = 'none';
        resetBattle();
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