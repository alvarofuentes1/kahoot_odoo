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
    let tiempoDeRespuesta = 0; // Variable para almacenar el tiempo de respuesta

    function registrarTiempoDeInicio() {
        startTime = Date.now();
    }

    function calcularTiempoDeRespuesta() {
        if (startTime) {
            tiempoDeRespuesta = (Date.now() - startTime) / 1000; // Convertir a segundos
            return tiempoDeRespuesta;
        } else {
            return 0;
        }
    }
    
    // Antes de enviar el tiempo de respuesta, llama a la función enviarRespuestasYTiempo para obtener el ID de la respuesta(user_input.line)
    // async function enviarRespuestasYTiempo(postData, tiempoDeRespuesta, questionId) {
    //     const pathParts = window.location.pathname.split('/');
    //     const survey_token = pathParts[3];
    //     const answer_token = pathParts[4];

    //     // Primero envías las respuestas como lo hace Odoo normalmente
    //     const response = await fetch("/survey/submit/" + survey_token + "/" + answer_token, {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify(postData)
    //     });
    
    //     const data = await response.json();
    
    //     // Una vez se ha guardado el input_line, ahora sí envías el tiempo
    //     if (data && !data.error) {
    //         console.log("Respuesta guardada correctamente:", data);
    //     } else {
    //         console.warn("No se pudo guardar la respuesta, no se envía tiempo");
    //     }
    // }

    function enviarTiempoDeRespuesta(questionId, tiempoDeRespuesta) {


        fetch("/survey/set_response_time", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question_id: questionId,
                response_time: tiempoDeRespuesta,
            })
        })
            .then(response => {
                console.log("Response:", response);
                return response.json()
            })
            .then(data => {
                console.log("Data:", data);
                if (data.result.status === "ok") {
                    console.log("Tiempo de respuesta guardado en survey.user_input.line");
                } else {
                    console.error("Data error:", data.message);
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
                tiempoDeRespuesta = calcularTiempoDeRespuesta();
                console.log("Tiempo de respuesta:", tiempoDeRespuesta);

                // Seleccionar el contenedor principal
                const answerWrapper = document.querySelector('.o_survey_answer_wrapper');

                if (answerWrapper) {
                    questionId = answerWrapper.getAttribute('data-name');
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
        iniciarTemporizador();
    }

    //Cuando se hace clic en un botón de tipo submit, reinicia el temporizador
    document.addEventListener("click", function (event) {
        const clickedElement = event.target; // Elemento que fue clicado
        if (clickedElement.tagName === "BUTTON" && clickedElement.type === "submit") {
            iniciarTemporizador();
        }
    });

});
