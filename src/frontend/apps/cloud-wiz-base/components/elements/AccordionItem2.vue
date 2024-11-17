<template>
    <li class="accordion-item" :class="{ 'is-active': isActive }" >
        <div class="accordion-thumb" @click="toggleAccordion">
            <h5 class="s-22 w-700"> {{ title }} </h5>
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