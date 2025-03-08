document.addEventListener('DOMContentLoaded', () => {
    // Battle elements
    const battleOverlay = document.getElementById('battleOverlay');
    const showBattleBtn = document.getElementById('showBattleBtn');
    const playerAvatar = document.getElementById('playerAvatar');
    const opponentAvatar = document.getElementById('opponentAvatar');
    const attackBtn = document.getElementById('attackBtn');
    const defendBtn = document.getElementById('defendBtn');
    const specialBtn = document.getElementById('specialBtn');

    // Show/Hide battle overlay
    showBattleBtn.addEventListener('click', () => {
        battleOverlay.style.display = 'flex';
        // Initialize stats
        initializeStats();
    });

    // Close battle when clicking outside
    battleOverlay.addEventListener('click', (e) => {
        if (e.target === battleOverlay) {
            battleOverlay.style.display = 'none';
        }
    });

    function initializeStats() {
        // Set initial HP and EXP values
        document.querySelectorAll('.hp .stat-fill').forEach(fill => {
            fill.style.transform = 'scaleX(1)';
        });
        document.querySelectorAll('.exp .stat-fill').forEach(fill => {
            fill.style.transform = 'scaleX(0.5)';
        });
    }

    function attack(attacker, defender, attackClass, reactionClass) {
        // Set z-index for proper layering
        attacker.style.zIndex = '2';
        defender.style.zIndex = '1';

        // Add attack animation
        attacker.classList.add(attackClass);

        // After attack animation starts
        setTimeout(() => {
            // Add defender reaction
            defender.classList.add(reactionClass);

            // Remove defender reaction
            setTimeout(() => {
                defender.classList.remove(reactionClass);
            }, 500);

            // Remove attack animation
            setTimeout(() => {
                attacker.classList.remove(attackClass);
                // Reset z-index
                attacker.style.zIndex = '1';
            }, 300);
        }, 300);
    }

    // Battle controls event listeners
    attackBtn.addEventListener('click', () => {
        attack(playerAvatar, opponentAvatar, 'attack-left', 'hit');
        updateStats();
    });

    defendBtn.addEventListener('click', () => {
        playerAvatar.classList.add('block');
        setTimeout(() => {
            attack(opponentAvatar, playerAvatar, 'attack-right', 'block');
        }, 500);
    });

    specialBtn.addEventListener('click', () => {
        attack(playerAvatar, opponentAvatar, 'attack-left', 'dodge');
        setTimeout(() => {
            attack(opponentAvatar, playerAvatar, 'attack-right', 'hit');
        }, 1000);
    });

    function updateStats() {
        // Simulate HP/EXP changes
        const hpBars = document.querySelectorAll('.hp .stat-fill');
        const expBars = document.querySelectorAll('.exp .stat-fill');

        hpBars.forEach(hp => {
            const currentScale = parseFloat(hp.style.transform.replace('scaleX(', '').replace(')', '')) || 1;
            const newScale = Math.max(0, currentScale - 0.1);
            hp.style.transform = `scaleX(${newScale})`;
        });

        expBars.forEach(exp => {
            const currentScale = parseFloat(exp.style.transform.replace('scaleX(', '').replace(')', '')) || 0.5;
            const newScale = Math.min(1, currentScale + 0.1);
            exp.style.transform = `scaleX(${newScale})`;
        });
    }
});

document.getElementById('startBattle').addEventListener('click', () => {
    document.getElementById('battleArena').style.display = 'block';
});

// Close battle arena when clicking outside
document.querySelector('.battle-overlay').addEventListener('click', (e) => {
    if (e.target.classList.contains('battle-overlay')) {
        document.getElementById('battleArena').style.display = 'none';
    }
});