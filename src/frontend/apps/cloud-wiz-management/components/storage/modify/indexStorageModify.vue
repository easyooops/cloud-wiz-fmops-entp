<template>
    <div>
      <Breadcrumbs main="" title="Storage File Manager" />
      <div class="container-fluid">
        <div class="row">
            <filesList />
        </div>
    </div>
    </div>
  </template>
  <script>
import filesList from './filesList.vue'
  export default {
    components:{
      filesList,
    }
   
  }
  </script>