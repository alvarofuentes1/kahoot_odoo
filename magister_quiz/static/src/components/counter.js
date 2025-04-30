/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
    }
}
Counter.template = "your_module.CounterTemplate";
