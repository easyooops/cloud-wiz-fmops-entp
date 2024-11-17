<template>
  <div>
    <h1>Processing Google Drive Authentication...</h1>
    <!-- Optional: Loading spinner or progress indicator -->
  </div>
</template>

<script>
import { useProviderStore } from '@/store/provider';
import restApi from "~/utils/axios";

export default {
  name: 'GoogleDriveCallback',
  async mounted() {
    const providerStore = useProviderStore();
    const urlParams = new URLSearchParams(window.location.search);

    const code = urlParams.get('code');

    if (!code) {
      console.error('Authorization code not found');
      this.$router.push('/provider/list');
      return;
    }

    try {
      const { get } = restApi();
      const response = await get(`/auth/google/callback?code=${code}`);
      const tokens = await response.data;

      const userId = sessionStorage.getItem('userId');
      const selectedProvider = sessionStorage.getItem('selectedProvider');
      const providerName = sessionStorage.getItem('providerName');

      const credentialData = {
        user_id: userId,
        provider_id: selectedProvider,
        credential_name: providerName,
        access_token: tokens.access_token,
        refresh_token: tokens.refresh_token,
        creator_id: userId,
        updater_id: userId,
      };

      await providerStore.createCredential(credentialData);

      sessionStorage.removeItem('userId');
      sessionStorage.removeItem('selectedProvider');
      sessionStorage.removeItem('providerName');
      this.$router.push('/provider/list');
    } catch (error) {
      this.$router.push('/provider/list');
    }
  }
};
</script>
