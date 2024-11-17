<template>
    <div>
        <defaultDashboard />
    </div>
</template>
<script>
import defaultDashboard from './dashboard/default12.vue'
definePageMeta({
  layout: 'default'
})
export default {
    components: {
        defaultDashboard
    }
}
</script>
