<template>
  <div>
    <footer class="footer" :class="footer == 'footer-dark' ? 'footer-dark' : ''">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12 footer-copyright text-center">
            <p class="mb-0">Copyright 2023 © Cuba theme by pixelstrap </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { useLayoutStore } from '~~/store/layout';
import json from '@/data/menu';

export default {

  data() {
    return {
      customizer: false,
      data:
        'data:text/json;charset=utf-8,' +
        encodeURIComponent(JSON.stringify(json)),
    };
  },
  computed: {

    footer() {
      return useLayoutStore().footer123
    }
  }
};
</script>