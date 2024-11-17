<template>
    <div>
      <Breadcrumbs main="" title="Agent Create" />
      <div class="container-fluid">
        <div class="row">
            <mainAgentCompare />
        </div>
    </div>
    </div>
  </template>
  <script>
import mainAgentCompare from './mainAgentCompare.vue';
  export default {
    components:{
        mainAgentCompare,
    }
   
  }
  </script>