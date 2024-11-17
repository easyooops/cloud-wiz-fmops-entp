<template>
   
        <div class="card">
            <div class="card-header" v-if="useSlots().header">
            <slot name="header"></slot>
            </div>
                <slot></slot>
            <div class="card-footer" v-if="useSlots().footer" >
                <div>
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
   
</template>
<script>
export default {
    props:{
        actions: Boolean
    }
}
</script>