<template>
    <div class="counter-up" ref="counterRef">
        <span>{{ count }}</span>
    </div>
</template>
<script>
export default {
    data() {
        return {
            count: 0,
            inViewport: false
        };
    },
    props: {
        start: {
            type: Number,
            default: 0
        },
        end: {
            type: Number,
            required: true
        },
        duration: {
            type: Number,
            default: 1000 // In milliseconds
        }
    },
    mounted() {
        this.observer = new IntersectionObserver(this.handleIntersection, {
            threshold: 0.2 // 20% of the element is visible
        });
        this.observer.observe(this.$refs.counterRef);
    },
    beforeUnmount() {
        this.observer.disconnect();
    },
    methods: {
        handleIntersection(entries) {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !this.inViewport) {
                    this.inViewport = true;
                    this.startCounter();
                }
            });
        },
        startCounter() {
            let startTime;
            const step = (timestamp) => {
                if (!startTime) startTime = timestamp;
                const progress = timestamp - startTime;
                this.count = Math.floor((this.end - this.start) * (progress / this.duration) + this.start);
                if (progress < this.duration && this.inViewport) {
                    requestAnimationFrame(step);
                }
            };
            requestAnimationFrame(step);
        }
    }
};
</script>
