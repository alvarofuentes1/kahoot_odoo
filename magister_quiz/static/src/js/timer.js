document.addEventListener("DOMContentLoaded", function () {
    // DOMContentLoaded se dispara cuando el DOM ha sido completamente cargado y analizado
    // sin esperar a que se carguen las hojas de estilo, imágenes y subtramas.


    let intervalo;

    function iniciarTemporizador() {
        const temporizador = document.getElementById("question_timer"); //Variable donde aparecen los segundos
        if (!temporizador) {
            console.warn("No se encontró el elemento del temporizador.");
            return;
        }
    
        // LLamada a la API para obtener la configuración del temporizador
        fetch('/quiz/timer/cuestionario de prueba')
            .then(response => response.json())
            .then(data => {
                console.log("Config del temporizador:", data);
    
                if (!data.is_question_timed) {
                    console.log("El cuestionario no tiene temporizador activado.");
                    return;
                }
    
                let segundos = data.time_per_question;
                temporizador.innerHTML = segundos + 's';
    
                if (intervalo) clearInterval(intervalo);
    
                intervalo = setInterval(() => {
                    segundos--;
                    temporizador.innerHTML = segundos + 's';
    
                    if (segundos <= 0) {
                        temporizador.innerHTML = '¡Tiempo!';
                        clearInterval(intervalo);
    
                        setTimeout(() => {
                            const boton = document.querySelector("button[type='submit']");
                            if (boton) boton.click();
                        }, 1000);
                    }
                }, 1000);
            })
            .catch(error => {
                console.error("Error al obtener configuración del temporizador:", error);
            });
    }
    
    // Solo se ejecuta el temporizador si encontramos el contenedor de la encuesta
    const surveyContainer = document.querySelector('.o_survey_answer_wrapper');
    if (!surveyContainer) {
        console.log("El temporizador NO se ejecuta en esta página.");
    } else {
        console.log("El temporizador SI se ejecuta en esta página.");
        iniciarTemporizador();
    }

    //Cuando se hace clic en un botón de tipo submit, reinicia el temporizador
    document.addEventListener("click", function (event) {
        const clickedElement = event.target; // Elemento que fue clicado
        if (clickedElement.tagName === "BUTTON" && clickedElement.type === "submit") {
            console.log("Se hizo clic en un botón de tipo submit. Reiniciando temporizador...");
            iniciarTemporizador();
        }
    });

});
