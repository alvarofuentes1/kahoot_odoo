document.addEventListener("DOMContentLoaded", function () {
    // DOMContentLoaded se dispara cuando el DOM ha sido completamente cargado y analizado
    // sin esperar a que se carguen las hojas de estilo, imágenes y subtramas.


    let intervalo;

    function iniciarTemporizador() {
        const temporizador = document.getElementById("question_timer"); //Variable donde aparecen los segundos
        const titulo = temporizador?.dataset?.surveyTitle; //Variable donde aparece el título del temporizador

        if (!temporizador) {
            console.warn("No se encontró el elemento del temporizador.");
            return;
        }

        // LLamada a la API para obtener la configuración del temporizador
        fetch(`/quiz/timer/${encodeURIComponent(titulo)}`)
            .then(response => response.json())
            .then(data => {

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

    let startTime = null; // Variable para almacenar el tiempo de inicio

    function registrarTiempoDeInicio() {
        startTime = Date.now();
        console.log("Tiempo de inicio registrado:", startTime);
    }

    function calcularTiempoDeRespuesta() {
        if (startTime) {
            const tiempoDeRespuesta = (Date.now() - startTime) / 1000; // Convertir a segundos
            return tiempoDeRespuesta;
        } else {
            console.warn("El tiempo de inicio no está registrado.");
            return 0;
        }
    }

    function enviarTiempoDeRespuesta(questionId, responseTime) {
        fetch("/survey/set_response_time", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({
                question_id: 57,
                response_time: 8.4
            })
        })
            .then(response => {
                console.log("Respuesta del servidor:", response);
                return response.json()
            })
            .then(data => {
                console.log("Respuesta del servidor:", data);
                if (data.status === "ok") {
                    console.log("Tiempo de respuesta guardado en survey.user_input_line");
                } else {
                    console.error("Error:", data.message);
                }
            })
            .catch(error => console.error("Error en fetch:", error));
    }


    function inicializarEventos() {
        // Registrar el tiempo de inicio al cargar la página o la pregunta
        const surveyContainer = document.querySelector('.o_survey_answer_wrapper');
        if (surveyContainer) {
            registrarTiempoDeInicio(); // Registrar el tiempo de inicio al cargar la página
        }

        // Escuchar clics en el botón de envío
        document.addEventListener("click", function (event) {
            const clickedElement = event.target;
            if (clickedElement.tagName === "BUTTON" && clickedElement.type === "submit") {
                console.log("Botón clicado, calculando tiempo de respuesta...");
                const tiempoDeRespuesta = calcularTiempoDeRespuesta();
                console.log("Tiempo de respuesta:", tiempoDeRespuesta);

                // Seleccionar el contenedor principal
                const answerWrapper = document.querySelector('.o_survey_answer_wrapper');

                if (answerWrapper) {
                    const questionId = answerWrapper.getAttribute('data-name');
                    console.log("Question ID:", questionId);

                    if (questionId) {
                        enviarTiempoDeRespuesta(questionId, tiempoDeRespuesta);
                    } else {
                        console.warn("No se encontró el ID de la pregunta.");
                    }

                } else {
                    console.warn("No se encontró el contenedor o_survey_answer_wrapper.");
                }

                // Reiniciar el tiempo de inicio para la siguiente pregunta
                registrarTiempoDeInicio();
            }
        });
    }

    // Inicializar eventos al cargar la página
    inicializarEventos();

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
