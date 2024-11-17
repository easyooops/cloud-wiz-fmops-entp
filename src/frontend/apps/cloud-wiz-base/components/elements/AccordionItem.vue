<template>
    <li class="accordion-item" :class="{ 'is-active': isActive }">
        <div class="accordion-thumb" @click="toggleAccordion">
            <h4 class="s-28 w-700">{{ title }}</h4>
        </div>
        <div v-if="isActive" class="accordion-panel">
            <slot></slot>
        </div>
    </li>
</template>
<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            isActive: false
        };
    },
    methods: {
        toggleAccordion() {
            this.isActive = !this.isActive;
        }
    }
};
</script>
