<template>
  <div>
      <Breadcrumbs main="" title="Agent Create" />
      <div class="container-fluid">
        <div class="row">
            <mainAgent />
            <Modal />
        </div>
    </div>
  </div>
</template>
<script>
import mainAgent from './mainAgent.vue';
import Modal from './modal.vue';
export default {
  components:{
      mainAgent,
      Modal
  }
  
}
</script>