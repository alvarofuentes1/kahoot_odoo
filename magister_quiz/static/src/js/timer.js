odoo.define('magister_quiz.timer', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.QuestionTimer = publicWidget.Widget.extend({
        selector: '#question_timer',
        start: function () {
            let interval;
            const timerElement = this.$el;

            const startTimer = () => {
                let seconds = 5;
                timerElement.text(`${seconds}s`);

                if (interval) {
                    clearInterval(interval);
                }

                interval = setInterval(() => {
                    timerElement.text(`${seconds}s`);
                    seconds--;

                    if (seconds < 0) {
                        clearInterval(interval);
                        const submitButton = document.querySelector("button[type='submit']");
                        if (submitButton) {
                            submitButton.click();
                        } else {
                            console.warn("No se encontró el botón de submit.");
                        }
                    }
                }, 1000);
            };

            // Observa cambios en el DOM para reiniciar el temporizador
            const surveyContainer = document.querySelector('.o_survey_form');
            if (surveyContainer) {
                const observer = new MutationObserver(() => {
                    console.log("Se detectaron cambios en el DOM. Reiniciando temporizador...");
                    startTimer();
                });

                observer.observe(surveyContainer, {
                    childList: true,
                    subtree: true,
                });
            }

            // Inicia el temporizador por primera vez
            startTimer();
        }
    });
});