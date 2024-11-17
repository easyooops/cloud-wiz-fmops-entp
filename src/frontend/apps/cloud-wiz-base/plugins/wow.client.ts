
import WOW from "wow.js"

export default defineNuxtPlugin(nuxtApp => {
    const isMobile = window.innerWidth < 768 && /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(window.navigator.userAgent);
    if (!isMobile) {
        new WOW().init()
    }
})
