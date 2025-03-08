const fighter1 = document.getElementById("fighter1");
const fighter2 = document.getElementById("fighter2");

function attack(fighter, opponent, attackClass) {
    fighter.classList.add(attackClass);
    setTimeout(() => {
        fighter.classList.remove(attackClass);
        opponent.classList.add("hit");
        setTimeout(() => {
            opponent.classList.remove("hit");
        }, 200);
    }, 300);
}

// Automatic Fighting Loop
function fightLoop() {
    setTimeout(() => {
        attack(fighter1, fighter2, "attack-left");
    }, 1000);

    setTimeout(() => {
        attack(fighter2, fighter1, "attack-right");
    }, 2000);

    setTimeout(fightLoop, 3000); // Repeat loop
}

fightLoop();
