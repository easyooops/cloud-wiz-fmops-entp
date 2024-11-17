<template>
    <span :class="['go-to-top', { show: showGoToTop }]" @click="scrollToTop">
        <img class="img-fluid" src="/assets/images/up_arrow.svg" alt="brand-logo" />
    </span>
</template>
<script>
export default {
    data() {
        return {
            showGoToTop: false
        };
    },
    mounted() {
        window.addEventListener("scroll", this.handleScroll);
    },
    beforeDestroy() {
        window.removeEventListener("scroll", this.handleScroll);
    },
    methods: {
        handleScroll() {
            const scrollY = window.scrollY;
            this.showGoToTop = scrollY > 200;
        },
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    }
};
</script>
<style lang="scss">
.go-to-top {
    display: block;
    position: fixed;
    bottom: -10px;
    right: 30px;
    width: 48px;
    height: 48px;
    line-height: 45px;
    background-color: #232734;
    border-radius: 100px;
    box-shadow: 0 0 10px 10px rgba(0, 0, 0, 0.05);
    z-index: 999;
    text-align: center;
    opacity: 0;
    transition-duration: 0.2s;
    cursor: pointer;
    &.show {
        opacity: 1;
        bottom: 30px;
        transition-duration: 0.2s;
    }
}
</style>
