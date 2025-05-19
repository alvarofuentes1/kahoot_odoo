
document.addEventListener('click', function (event) {

    const surveyContainer = document.querySelector('.o_survey_answer_wrapper');
    if (surveyContainer) {
        eventoSubmit(); // Registrar el tiempo de inicio al cargar la página
    }

    async function eventoSubmit(postData) {
        const clickedElement = event.target;
        if (clickedElement.tagName === "BUTTON" && clickedElement.type === "submit") {
                
            mostrarExplicacion();
        }
    }

    function mostrarExplicacion() {
        const explanation = document.querySelector('.answer-explanation');
        if (explanation) {
            explanation.classList.remove('d-none')
        } else console.log("No hay explacaion disponible")
    }
})

