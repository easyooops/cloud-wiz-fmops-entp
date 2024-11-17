<template>
    <div>

        <div class="page-wrapper compact-wrapper" id="pageWrapper">

            <div class="container-fluid p-0">
                <div class="comingsoon auth-bg-video">
                    <video class="bgvideo-comingsoon" id="bgvid" poster="/images/other-images/coming-soon-bg.jpg"
                        playsinline="" autoplay="" muted="" loop="">
                        <source src="@/assets/video/auth-bg.mp4" type="video/mp4">
                    </video>
                    <div class="comingsoon-inner text-center"><img src="/images/other-images/logo-login.png" alt="logo">
                        <h5>WE ARE COMING SOON</h5>
                        <div class="countdown" id="clockdiv">
                            <Timer />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
definePageMeta({
    layout: 'custom'
})
import Timer from './comingsoon_timer';
export default {
    components: {
        Timer
    },
    data() {
        return {
            startTime: 'Apr 29, 2021 00:00:00',
            endTime: 'Apr 29, 2022 00:00:00',
        };
    },
};
</script>
