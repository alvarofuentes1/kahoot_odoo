odoo.define('your_module.question_timer', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.QuestionTimer = publicWidget.Widget.extend({
        selector: '#question-timer-container', // El contenedor donde se va a mostrar el timer
        events: {
            'click #start-timer': '_startTimer', // Iniciar el temporizador si es necesario
        },

        init: function (parent, options) {
            this._super(parent, options);
            this.timeLimit = 30; // Límite de tiempo de la pregunta en segundos
            this.timeLeft = this.timeLimit;
            this.timerInterval = null;
        },

        // Método para empezar el temporizador
        startTimer: function () {
            var self = this;
            this.timerInterval = setInterval(function () {
                if (self.timeLeft > 0) {
                    self.timeLeft--;
                    $('#question-timer').text(self.timeLeft + "s");
                } else {
                    self.stopTimer();
                    self.onTimeUp();
                }
            }, 1000); // El temporizador cuenta cada segundo
        },

        // Método para detener el temporizador
        stopTimer: function () {
            clearInterval(this.timerInterval);
        },

        // Acción cuando se acaba el tiempo
        onTimeUp: function () {
            // Aquí puedes hacer lo que desees, por ejemplo, pasar a la siguiente pregunta
            alert("¡Se acabó el tiempo! Pasando a la siguiente pregunta...");
            // Código para cambiar a la siguiente pregunta o actualizar la interfaz.
        },

        // Método para inicializar el temporizador cuando cambia la pregunta
        resetTimer: function () {
            this.stopTimer();
            this.timeLeft = this.timeLimit;
            $('#question-timer').text(this.timeLeft + "s");
            this.startTimer();
        },
    });

    return publicWidget.registry.QuestionTimer;
});
