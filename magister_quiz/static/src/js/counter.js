/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";

export class Counter extends Component {
    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
    }

    onMounted() {
        console.log("Counter component mounted");
    }

    static template = /*xml*/`
    <div>
        <p>Contador: <span t-esc="state.count"/></p>
        <button t-on-click="increment">Incrementar</button>
    </div>
`;

    static props = {
        title: { type: String, optional: true },
    };
}

