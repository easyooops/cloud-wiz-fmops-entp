<template>
    <Breadcrumbs main="Monitoring" title="Trace Log" />

    <div class="container-fluid">
        <traceDatadog />
    </div>
</template>

<script>
import traceDatadog from './traceDatadog.vue'
export default {
    name: 'indexList',
    components: {
        traceDatadog
    },
}
</script>
