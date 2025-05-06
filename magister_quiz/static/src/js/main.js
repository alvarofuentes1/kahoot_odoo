
/** @odoo-module **/

import { Counter } from "./counter";
import { mount } from "@odoo/owl";

document.addEventListener("DOMContentLoaded", function () {

    console.log("main.js loaded");
    const target = document.querySelector("#my_counter_component");
    if (target) {
        mount(Counter, target);
    }else{
        console.error("Target element not found for mounting the component.");
    }

});
