document.addEventListener('DOMContentLoaded', () => {
    // Battle elements
    const battleOverlay = document.getElementById('battleOverlay');
    const showBattleBtn = document.getElementById('showBattleBtn');
    const currentEnemy = document.getElementById('currentEnemy');
    const enemyQueue = document.getElementById('enemyQueue');

    // Available monster images
    const monsterImages = [
        'abyssal_fiend.png', 'ancient_dragon.png', 'berserker_dwarf.png',
        'bone_harbinger.png', 'crimson_imp.png', 'dark_raven.png',
        'demon_warrior.png', 'djinn_mystic.png', 'eclipse_phantom.png',
        'flame_serpent.png', 'forest_beast.png', 'golden_devourer.png',
        'hellhound.png', 'infernal_juggernaut.png', 'mad_orc.png',
        'medusa_enchantress.png', 'nosferos.png', 'obsidian_warlord.png',
        'shadow_striker.png', 'skeletal_spearman.png', 'skull_inferno.png',
        'snow_yeti.png', 'venom_cobra.png', 'wyrmling_drake.png'
    ];

    let tasks = [
        "Read 1 section of PEP 8",
        "Debug a small script",
        "Write a docstring for a function",
        "Solve a CodeWars kata (easy)",
        "Review list comprehensions",
        "Practice string formatting",
        "Explore a new built-in function",
        "Refactor a past project",
        "Write a unit test",
        "Learn about virtual environments",
        "Study dictionary methods",
        "Research a Python library",
        "Implement a simple class",
        "Traceback a given error",
        "Practice file I/O",
        "Review conditional statements",
        "Study for loops",
        "Learn about tuple unpacking",
        "Write a short script using argparse",
        "Explore exception handling",
        "Practice using sets",
        "Review lambda functions",
        "Solve a simple algorithm problem",
        "Read a Python blog post"
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
        return monsterImages[Math.floor(Math.random() * monsterImages.length)];
    }

    function initializeBattle() {
        // get a task from shuffle list
        const taskDescription = document.getElementById('taskDescription');
        taskDescription.focus();
        taskDescription.textContent = tasks.pop()

        resetBattle();
        battleActive = true;
        
        // Set player sprite
        const playerSprite = document.querySelector('.player-character .character-sprite');
        if (playerSprite) {
            playerSprite.style.backgroundImage = "url('/static/assets/images/avatar_icons/players/con1.png')";
        }

        // Generate 3-5 enemies
        const totalEnemies = Math.floor(Math.random() * 3) + 3;
        enemies = Array.from({ length: totalEnemies }, () => ({
            health: Math.floor(Math.random() * 3) + 3,
            maxHealth: Math.floor(Math.random() * 3) + 3,
            image: getRandomMonster()
        }));

        // Create queue indicators
        enemies.forEach((_, index) => {
            const indicator = document.createElement('div');
            indicator.className = `queue-indicator`;
            enemyQueue.appendChild(indicator);
        });

        showCurrentEnemy();
    }

    function showCurrentEnemy() {
        if (!enemies[currentEnemyIndex]) return;
        
        const enemy = enemies[currentEnemyIndex];
        const enemySprite = currentEnemy.querySelector('.character-sprite');
        const hpFill = document.querySelector('.enemy-stats .hp-fill');
        
        if (enemySprite) {
            enemySprite.style.backgroundImage = `url('/static/assets/images/avatar_icons/monsta/${enemy.image}')`;
        }
        
        if (hpFill) {
            hpFill.style.transform = `scaleX(${enemy.health / enemy.maxHealth})`;
        }

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
        
        const taskDescription = document.getElementById('taskDescription');
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
        
        // Player attack animation
        const playerChar = document.querySelector('.player-character');
        playerChar.classList.add('attacking-right');
        
        setTimeout(() => {
            // Enemy takes damage
            enemy.health--;
            const hpFill = document.querySelector('.enemy-stats .hp-fill');
            if (hpFill) {
                hpFill.style.transform = `scaleX(${enemy.health / enemy.maxHealth})`;
            }

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

        const taskDescription = document.getElementById('taskDescription');
        taskDescription.textContent = tasks.pop()

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
                    endBattle(true);
                }, 500);
            }
        }, 1000);
    }

    function resetBattle() {
        tasks.sort(() => Math.random() - 0.5);
        enemyQueue.innerHTML = '';
        currentEnemy.classList.remove('hit', 'defeated', 'attacking-left');
        document.querySelector('.enemy-stats .hp-fill').style.transform = 'scaleX(1)';
        
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
});