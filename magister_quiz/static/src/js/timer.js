document.addEventListener("DOMContentLoaded", function () {

    const temporizador = document.getElementById("question_timer");
    let intervalo;

    function iniciarTemporizador() {
        let segundos = 10;
        temporizador.innerHTML = segundos + 's';

        if (intervalo) clearInterval(intervalo);

        intervalo = setInterval(() => {
            segundos--;
            temporizador.innerHTML = segundos + 's';

            if (segundos <= 0) {
                temporizador.innerHTML = '¡Tiempo!';
                clearInterval(intervalo);

                setTimeout(() => {
                    // Simular el clic en el botón de enviar
                    const boton = document.querySelector("button[type='submit']");
                    if (boton) boton.click();
                }, 1000);
            }
        }, 1000);
    }

    const surveyContainer = document.querySelector('.o_survey_answer_wrapper');
    if (!surveyContainer) {
        console.log("El temporizador NO se ejecuta en esta página.");
    } else {
        console.log("El temporizador SI se ejecuta en esta página.");
        iniciarTemporizador();
    }

    document.addEventListener("click", function (event) {
        const clickedElement = event.target; // Elemento que fue clicado
        if (clickedElement.tagName === "BUTTON" && clickedElement.type === "submit") {
            console.log("Se hizo clic en un botón de tipo submit. Reiniciando temporizador...");
            iniciarTemporizador();
        }
    });

});
