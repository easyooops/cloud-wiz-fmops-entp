import { defineRule, configure } from 'vee-validate';
import * as AllRules from '@vee-validate/rules';

export default defineNuxtPlugin((nuxtApp) => {
    Object.keys(AllRules).forEach(rule => {
        const ruleDefinition = AllRules[rule];
        if (typeof ruleDefinition === 'function') {
            defineRule(rule, ruleDefinition);
        } else {
            console.warn(`Skipping invalid rule: ${rule}`);
        }
    });

    // vee-validate config
    configure({
        // classes: {
        //     valid: 'is-valid',
        //     invalid: 'is-invalid'
        // },
        // bails: true,
        // skipOptional: true,
        // mode: 'aggressive',
        // useConstraintAttrs: true
    });
});
