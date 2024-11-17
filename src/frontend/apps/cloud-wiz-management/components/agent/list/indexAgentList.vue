<template>
    <Breadcrumbs main="Agent" title="Agents List" />
    <div class="container-fluid">
        <div class="row project-cards">
            <mainAgent />
        </div>
    </div>
</template>

<script>
import mainAgent from './mainAgent.vue'

export default {
    name: 'indexList',
    components: {
        mainAgent
    },

}

</script>
