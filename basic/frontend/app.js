const presedientCanidate = document.getElementById('president-canidate');
let anyPresidentClicked = false;

if (presedientCanidate) {
    const confirmButton = document.querySelector('.confirm-btn');
    if (confirmButton) {
        confirmButton.setAttribute('disabled', true);
    }

    const pVoteButtons = presedientCanidate.querySelectorAll('.president button[title="vote"]');
    const voteButtons = document.querySelectorAll('.directors button[title="vote"]');
    const directorRows = document.querySelectorAll('.directors .single');

    function checkConditions() {
        anyPresidentClicked = Array.from(pVoteButtons).some(button => button.classList.contains('active'));

        const allRowsHaveDisabled = Array.from(directorRows).every(row => {
            return Array.from(row.querySelectorAll('button[title="vote"]')).some(btn => btn.classList.contains('active')
            );
        });

        if (allRowsHaveDisabled && anyPresidentClicked) {
            confirmButton.removeAttribute('disabled');
        } else {
            confirmButton.setAttribute('disabled', true);
        }
    }

    function handleVote(btn) {
        const row = btn.closest('tr');

        const buttons = row.querySelectorAll('button[title="vote"]');

        buttons.forEach(b => {
            if (b !== btn) {
                b.disabled = true;
                b.classList.add('disabled');
            }
        });
    }

    // Vote button logic for directors
    voteButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            if (!btn.classList.contains('active')) {
                btn.innerHTML = '<img src="./images/check-mark.png" alt="Voted" style="width: 50px; height: 50px;">';
                btn.classList.add('active');
                handleVote(btn);
            }

            checkConditions();
        });
    });

    // President vote button logic
    pVoteButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            // Disable all other president buttons
            pVoteButtons.forEach(pBtn => {
                if (pBtn !== btn) {
                    pBtn.disabled = true;
                    pBtn.classList.add('disabled');
                }
            });
            btn.classList.add('active');
            checkConditions(); // Check conditions after each president click
        });
    });

    if (confirmButton) {
        confirmButton.addEventListener('click', function () {
            const modal = document.querySelector('.modal')
            modal.classList.add('active')
        });
    }
}






// counter function with a promise to handle asynchronous updates
function counter() {
    return new Promise(resolve => {
        const voteElements = document.querySelectorAll('.total-vote');
        let completed = 0;

        voteElements.forEach(el => {
            const maxVote = parseInt(el.innerText);
            let currentVote = 0;
            const increment = Math.ceil(maxVote / 120);
            const speed = 60;

            const updateCounter = () => {
                currentVote += increment;
                if (currentVote > maxVote) currentVote = maxVote;
                el.innerText = currentVote;

                if (currentVote < maxVote) {
                    setTimeout(updateCounter, speed);
                } else {
                    completed += 1;
                    if (completed === voteElements.length) resolve();
                }
            };

            setTimeout(updateCounter, speed);
        });
    });
}

// change vote and sort rows by votes immediately after
function changeVotesAndSort() {
    const voteElements = document.querySelectorAll('.total-vote');

    voteElements.forEach((el, index) => {
        setTimeout(() => {
            const currentVotes = parseInt(el.innerText, 10);
            const newVote = currentVotes + Math.floor(Math.random() * 3) + 1;
            el.innerText = newVote;

            // Sort table after each vote update
            sortTableByVotes('present-table');
        }, index * 2000);
    });
}

// Sort function to reorder rows based on votes
function sortTableByVotes(element) {
    const tableBody = document.getElementById(element);
    const rows = [...tableBody.querySelectorAll('tr')];

    rows.sort((a, b) => {
        const voteA = parseInt(a.querySelector('.total-vote').innerText, 10);
        const voteB = parseInt(b.querySelector('.total-vote').innerText, 10);
        return voteB - voteA;
    });

    rows.forEach(row => tableBody.appendChild(row));

    rows.forEach((row, index) => {
        const titleCell = row.querySelector('.title.fw-bolder.fs-xxl');
        if (titleCell) titleCell.innerText = index + 1;
    });
}

// Async function to update votes and sort the table
async function updateVotes() {
    await counter();
    changeVotesAndSort();
}

// When the page reloads
document.addEventListener('DOMContentLoaded', function () {
    updateVotes();
    setInterval(changeVotesAndSort, 3500); // Change and sort votes every 3.5 seconds
});
