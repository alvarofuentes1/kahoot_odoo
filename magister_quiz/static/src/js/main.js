
/** @odoo-module **/

import { Counter } from "../components/counter";
import { mount } from "@odoo/owl";

document.addEventListener("DOMContentLoaded", function () {
    const target = document.getElementById("my_counter_component");
    if (target) {
        mount(Counter, { target });
        console.log("Counter component mounted successfully.");
    }
});