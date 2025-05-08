/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class AnswerFeedback extends Component {
    static template = "magister_quiz.AnswerFeedback";
    static props = {
        isCorrect: { type: Boolean },
        explanation: { type: String, optional: true },
    };

    setup() {
        this.state = {
            showFeedback: true
        };
    }
}

registry.category("public_components").add("magister_quiz.AnswerFeedback", AnswerFeedback);