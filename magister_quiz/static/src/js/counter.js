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
    <div class="p-4 bg-gray-100 rounded-lg shadow">
        <h2 class="text-xl font-bold mb-2">Contador Simple</h2>
        <p class="mb-4">Valor actual: <span class="font-bold" t-esc="state.count"/></p>
        <div class="flex space-x-2">
            <button t-on-click="increment">
                Incrementar
            </button>
        </div>
    </div>
`;

    static props = {
        title: { type: String, optional: true },
    };
}

