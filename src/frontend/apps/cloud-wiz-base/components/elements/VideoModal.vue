<template>
    <!-- copy this stuff and down -->
    <div class="d-flex" @click="toggler">
        <slot name="button"></slot>
    </div>
    <teleport to="body">
        <div class="video-modal" v-if="open">
            <div id="video-popup-overlay" @click="videoClose"></div>
            <div id="video-popup-container">
                <div id="video-popup-close" class="fade" @click="videoClose">&#10006;</div>
                <div id="video-popup-iframe-container">
                    <iframe id="video-popup-iframe" :src="link" width="100%" height="100%" frameborder="0" autoplay=""></iframe>
                </div>
            </div>
        </div>
    </teleport>
</template>
<script>
export default {
    props: ["link"],
    data() {
        return {
            open: false
        };
    },
    methods: {
        toggler() {
            this.open = !this.open;
        },
        videoClose() {
            if (document.getElementById("video-popup-iframe")) {
                document.getElementById("video-popup-iframe").removeAttribute("src");
            }
            this.open = !this.open;
        }
    }
};
</script>
<style lang="scss" scoped>
#video-popup-container {
    background-color: transparent;
    position: fixed;
    transform: translate(-50%, -50%);
    height: auto;
    width: 100%;
    max-height: 70vh;
    max-width: calc(200px + 25vw);
    left: 50%;
    top: 50%;
    z-index: 9997;
}
#video-popup-close {
    cursor: pointer;
    position: absolute;
    right: -16px;
    top: -16px;
    z-index: 9999;
    width: 32px;
    height: 32px;
    border-radius: 25px;
    text-align: center;
    font-size: 16px;
    background-color: #ffffffc2;
    line-height: 32px;
    color: #000;
    opacity: 1 !important;
}
@media only screen and (max-width: 320px) {
    #video-popup-close {
        right: -10px;
        top: -10px;
        width: 20px;
        height: 20px;
        border-radius: 25px;
        font-size: 12px;
        line-height: 24px;
    }
}
#video-popup-iframe-container {
    height: auto;
    width: 100%;
}
#video-popup-iframe {
    aspect-ratio: auto 16/9;
    background-color: #000;
    border: 2px solid #000;
    border-radius: 0.5rem;
    width: 100%;
    height: auto;
}
#video-popup-overlay {
    position: fixed;
    z-index: 999;
    top: 0;
    background-color: #000;
    opacity: 0.8;
    width: 100%;
    height: 100%;
}
#video-popup-close:hover {
    color: #de0023;
}
</style>
