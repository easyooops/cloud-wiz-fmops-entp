<template>
    <div>
      <Breadcrumbs main="" title="Compare" />
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