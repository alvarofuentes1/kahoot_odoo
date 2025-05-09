/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";

class CountdownTimer extends Component {

    static template = "magister_quiz.CountdownTimer";
    static props = {
        surveyTitle: { type: String },
        questionId: { type: String },
        onTimeUp: { type: Function, optional: true },
    };

    setup() {
        console.log("Props: " + this.props.surveyTitle + " and " + this.props.questionId)
        this.state = useState({
            timeLeft: 0,
            isActive: false,
            startTime: null,
            responseTime: 0
        });
        this.interval = null;

        onMounted(async () => {
            await this.initializeTimer();
        });

        onWillUnmount(() => {
            this.clearCountdown();
        });

        onWillUpdateProps(async (nextProps) => {
            if (nextProps.questionId !== this.props.questionId) {
                await this.initializeTimer();
            }
        });
    }

    async initializeTimer() {
        try {
            const response = await fetch(`/quiz/timer/${encodeURIComponent(this.props.surveyTitle)}`);
            const data = await response.json();

            if (!data.is_question_timed) {
                console.log("El cuestionario no tiene temporizador activado.");
                return;
            }

            this.clearCountdown();
            this.state.timeLeft = data.time_per_question;
            this.state.isActive = true;
            this.state.startTime = Date.now();
            this.startCountdown();
        } catch (error) {
            console.error("Error al obtener configuración del temporizador:", error);
        }
    }

    startCountdown() {
        this.interval = setInterval(() => {
            if (this.state.timeLeft > 0) {
                this.state.timeLeft -= 1;
            } else {
                this.handleTimeUp();
            }
        }, 1000);
    }

    clearCountdown() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    async handleTimeUp() {
        this.clearCountdown();
        this.state.isActive = false;
        
        // Calcular tiempo de respuesta
        this.state.responseTime = (Date.now() - this.state.startTime) / 1000;
        
        // Enviar tiempo de respuesta al servidor
        await this.sendResponseTime();
        
        // Llamar al callback si existe
        if (this.props.onTimeUp) {
            this.props.onTimeUp();
        }
    }

    async sendResponseTime() {
        const userInputToken = window.location.pathname.split('/')[3];
        
        try {
            const response = await fetch("/survey/set_response_time", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question_id: this.props.questionId,
                    response_time: this.state.responseTime,
                    user_input_token: userInputToken
                })
            });

            const data = await response.json();
            if (data.result.status === "ok") {
                console.log("Tiempo de respuesta guardado correctamente");
            } else {
                console.error("Error al guardar tiempo de respuesta:", data.message);
            }
        } catch (error) {
            console.error("Error al enviar tiempo de respuesta:", error);
        }
    }
}

registry.category("public_components").add("magister_quiz.CountdownTimer", CountdownTimer);