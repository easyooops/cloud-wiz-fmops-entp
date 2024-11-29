<template>
    <Breadcrumbs main="Prebuilt" title="Prebuilt List" />
    <div class="container-fluid">
        <div class="row project-cards">
            <mainPrebuilt />
        </div>
    </div>
</template>

<script>
import mainPrebuilt from './mainPrebuilt.vue'

export default {
    name: 'indexList',
    components: {
        mainPrebuilt
    },

}

</script>
