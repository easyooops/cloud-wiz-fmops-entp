<template>
  <div>
    <div class="logo-wrapper">
      <Logo />
      <div class="back-btn" @click="toggle_sidebar">
        <i class="fa fa-angle-left"></i>
      </div>
      <div class="toggle-sidebar" @click="toggle_sidebar">
        <vue-feather class="status_toggle middle sidebar-toggle" type="grid" id="sidebar-toggle"></vue-feather>
      </div>
    </div>
    <div class="logo-icon-wrapper">
      <router-link to="/">
        <img class="img-fluid" src="/images/logo/logo-icon.png" alt="" /></router-link>
    </div>
    <Nav />
  </div>
</template>
<script>
import { mapState } from 'pinia';
import Logo from './logo.vue';
import Nav from './nav.vue';
import { useMenuStore } from '~~/store/menu';

export default {
  name: 'Sidebar',
  components: {
    Logo,
    Nav,
  },
  computed: {
    ...mapState(useMenuStore, {
      menuItems: 'data',
      activeoverlay: 'activeoverlay',
    }),
  },
  methods: {
    toggle_sidebar() {

      useMenuStore().opensidebar()
      useMenuStore().activeoverlay = false
    },
  },
};
</script>
