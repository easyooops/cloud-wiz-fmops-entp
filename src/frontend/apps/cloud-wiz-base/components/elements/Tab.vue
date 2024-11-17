<template>
    <div class="tab-panel" role="tabPanel">
        <div class="tab-content"><slot></slot></div>
    </div>
</template>
<script>
import { defineComponent } from "vue";
export default defineComponent({
    name: "Tab",
    props: ["title", "titleSlot", "disabled"]
});
</script>
<style lang="scss">
.tab-panel {
    .tab-content {
        padding: 0.5rem;
    }
}
</style>
