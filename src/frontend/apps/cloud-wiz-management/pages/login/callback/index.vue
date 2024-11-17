<template>
    <div>
      <h1>Processing Authentication...</h1>
      <!-- Optional: Loading spinner or progress indicator -->
    </div>
  </template>
  
  <script>
  import restApi from '@/utils/axios';
  export default {
    name: 'AuthCallback',
    async mounted() {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const accessToken = urlParams.get('access_token'); // Assuming access_token is part of query params
  
        if (!accessToken) {
          throw new Error('Access token not found');
        }
  
        const { post } = restApi();
        const response = await post('/auth/', {
          token: accessToken
        });
  
        this.$router.push('/');
      } catch (error) {
        console.error('Authentication failed:', error);
        this.$router.push('/login');
      }
    }
  };
  </script>
  