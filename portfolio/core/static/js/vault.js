let holdTimer;

function startHold() {
    holdTimer = setTimeout(() => {
        document.getElementById("adminMenu").style.display = "block";
    }, 2000); // Hold for 2 seconds
}

function endHold() {
    clearTimeout(holdTimer);
}
