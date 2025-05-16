/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class AnswerFeedback extends Component {
    static template = "magister_quiz.AnswerFeedback";
    static props = {
        isCorrect: { type: Boolean },
        explanation: { type: String },
        showAfterNext: { type: Boolean, optional: true }
    }; 

    setup() {
        console.log(this.props.isCorrect)
        console.log(this.props.explanation)
        this.state = useState({
            showFeedback: false
        });
    }

    onMounted() {
        const container = document.querySelector('.o_survey_form');
        if (container) {
            container.addEventListener('click', (event) => {
                if (event.target.matches('.btn-primary[type="submit"]')) {
                    console.log("Botón siguiente pulsado vía delegación");
                    this.state.showFeedback = true;
                }
            });
        }
    }
    
}

registry.category("public_components").add("magister_quiz.AnswerFeedback", AnswerFeedback);