<template>
  <div class="mode" :class="mixLayout == 'dark-only' ? 'active' : ''">
    <svg v-show="mixLayout == 'light-only'" @click="customizeMixLayout('dark-only')">
      <use href="@/assets/svg/icon-sprite.svg#moon"></use>
    </svg>

    <svg v-show="mixLayout == 'dark-only'" @click="customizeMixLayout('light-only')">
      <use href="@/assets/svg/icon-sprite.svg#moon"></use>
    </svg>

  </div>
</template>

<script>
import { useLayoutStore } from '~~/store/layout';

export default {
  name: 'Mode',
  data() {
    return {
      mixLayout: 'light-only',
    };
  },
  methods: {
    customizeMixLayout(val) {
      this.mixLayout = val;
      useLayoutStore().setLayout({ class: val })
    },
  },
};
</script>
