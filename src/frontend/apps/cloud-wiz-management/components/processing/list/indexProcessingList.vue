<template>
    <Breadcrumbs main="Processing" title="Processing List" />

    <div class="container-fluid">
        <div class="row project-cards">
            <processing />
        </div>
    </div>
</template>

<script>
import processing from './processing.vue'
export default {
    name: 'indexList',
    components: {
        processing
    },

}

</script>
