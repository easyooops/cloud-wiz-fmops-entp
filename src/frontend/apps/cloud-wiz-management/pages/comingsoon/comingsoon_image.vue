<template>
    <div>

        <div class="page-wrapper compact-wrapper" id="pageWrapper">
            <!-- Page Body Start-->
            <div class="container-fluid p-0">
                <div class="comingsoon comingsoon-bgimg">
                    <div class="comingsoon-inner text-center">
                        <img src="/images/other-images/logo-login.png" alt="logo">
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
import Timer from './comingsoon_timer';
definePageMeta({
    layout: 'custom'
})
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
