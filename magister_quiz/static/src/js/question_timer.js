

window.addEventListener("load", function () {
    let seconds = 20;  // Aquí podrías usar un valor dinámico
    const timerElement = document.getElementById("question_timer");

    const interval = setInterval(() => {
        timerElement.innerText = `${seconds}s`;
        seconds -= 1;

        if (seconds < 0) {
            clearInterval(interval);
            // Aquí puedes lanzar evento, auto enviar, etc.
            alert("¡Tiempo agotado!");
        }
    }, 1000);
})


