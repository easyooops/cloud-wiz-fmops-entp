<template>
  <a :href="baseUrl">
    <img class="img-fluid for-light" src="/images/wiz/logo-pink.png" alt="" /><img class="img-fluid for-dark"
      src="/images/wiz/logo-pink.png" alt="" />
  </a>
</template>

<script setup>
const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';
</script>

<script>
export default {
  name: 'Logo',
};
</script>
