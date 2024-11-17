<template>
    <Breadcrumbs main="Provider" title="Providers List" />

    <div class="container-fluid">
        <div class="row project-cards">
            <provider />
        </div>
    </div>
</template>

<script>
import provider from './provider.vue'
export default {
    name: 'indexList',
    components: {
        provider
    },

}

</script>
