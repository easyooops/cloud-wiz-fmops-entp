<template>
    <NuxtLayout>
        <Head>
            <Title>CLOUDWIZ AI FMOPS</Title>
        </Head>
        <NuxtPage />
    </NuxtLayout>
</template>
<script>
import { useLayoutStore } from './store/layout';
export default {
    created() {},
    mounted() {
        window.addEventListener("beforeunload", (event) => {
            localStorage.setItem(
                "primary_color",
                useLayoutStore().primaryColor
            );

            localStorage.setItem(
                "secondary_color",
                useLayoutStore().secondaryColor
            );
        });
        let localPrimaryColor = localStorage.getItem('primary_color') || useLayoutStore().primaryColor;
        let localSecondaryColor = localStorage.getItem('secondary_color') || useLayoutStore().secondaryColor;
        useLayoutStore().intialChange({ localPrimaryColor, localSecondaryColor })
    },
    computed: {
        localPrimaryColor() {},
    },
};
</script>
