<template>
    <a class="nav-link" :class="{ 'active show': customizer == 'layouts' }" id="c-pills-home-tab"
      @click="openCustomizerSetting('layouts')" href="javascript:void(0)">
      <div class="settings">
        <i class="icon-paint-bucket"></i>
      </div>
      <span>Quick option</span>
    </a>
  </template>
  
  <script>
  import { mapState } from 'pinia';
  import { useMenuStore } from '~~/store/menu';
  
  export default {
    name: 'CustomizerTool',
    computed: {
      ...mapState(useMenuStore, {
        customizer: 'customizer'
      }),
    },
    methods: {
      openCustomizerSetting(val) {
  
        useMenuStore().customizer = val
      },
    }
  };
  </script>