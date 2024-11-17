<template>
<ClientOnly>
    <VueApexCharts :height="height" :type="type" :options="options" :series="series"/>
</ClientOnly>    
</template>
<script>
import VueApexCharts from "vue3-apexcharts";
export default {
    props: ['height','type','options','series'],
    components:{
        VueApexCharts
    }
}
</script>