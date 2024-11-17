<template>
    <Breadcrumbs main="Storage" title="Storage List" />

    <div class="container-fluid">
        <div class="row project-cards">
            <storage />
        </div>
    </div>
</template>

<script>
import storage from './storage.vue'
export default {
    name: 'indexList',
    components: {
        storage
    },

}

</script>
