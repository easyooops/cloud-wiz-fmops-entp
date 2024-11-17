<template>
  <Breadcrumbs main="Provider" title="Provider Create" />

  <div class="container-fluid">
    <div class="loader-overlay" v-if="loading">
      <div class="loader-box">
        <div class="loader-30"></div>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12">
        <div class="card">
          <div class="card-body">

            <form @submit.prevent="handleSubmit">
              <div class="form theme-form">
                <div class="row">
                  <div class="col-sm-4">
                    <div class="mb-3">
                      <label>Provider Type</label>
                      <select class="form-select" v-model="selectedType">
                        <option value="M">Model</option>
                        <option value="S">Storage</option>
                        <option value="L">Document Loader</option>
                        <option value="V">VectorDB</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm-4">
                    <div class="mb-3">
                      <label>Provider</label>
                      <select class="form-select" v-model="selectedProvider">
                        <option v-for="provider in providers" :key="provider.provider_id" :value="provider.provider_id">
                          {{ provider.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col">
                    <div class="mb-3">
                      <label>Provider Name</label>
                      <input v-model="providerName" class="form-control" type="text" placeholder="Provider Name *" required>
                    </div>
                  </div>
                </div>
                <div class="row" v-if="isAmazonWebServices">
                  <div class="col">
                    <div class="mb-3">
                      <label>Access Key</label>
                      <input v-model="accessKey" class="form-control" type="text" placeholder="Access Key *">
                    </div>
                  </div>
                  <div class="col">
                    <div class="mb-3">
                      <label>Secret Access Key</label>
                      <input v-model="secretAccessKey" class="form-control" type="text" placeholder="Secret Access Key *">
                    </div>
                  </div>
                  <!-- <div class="col">
                      <div class="mb-3">
                          <label>Session Key</label>
                          <input v-model="sessionKey" class="form-control" type="text" placeholder="Session Key *">
                      </div>
                  </div> -->
                </div>
                <div class="row" v-else-if="isGoogleDrive">
                </div>
                <div class="row" v-else-if="isNotion">
                  <div class="col">
                    <div class="mb-3">
                      <label>Access Token</label>
                      <input v-model="accessToken" class="form-control" type="text" placeholder="Access Token *">
                    </div>
                  </div>
                  <div class="col">
                      <div class="mb-3">
                        <label>DB Database</label>
                        <input v-model="dbDatabase" class="form-control" type="text" placeholder="DB Database *">
                      </div>
                    </div>                  
                </div>
                <div class="row" v-else-if="isGit">
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>Clone URL</label>
                        <input v-model="gitCloneUrl" class="form-control" type="text" placeholder="CLONE URL *">
                      </div>
                    </div>
                    <div class="col">
                      <div class="mb-3">
                        <label>Branch</label>
                        <input v-model="gitBranch" class="form-control" type="text" placeholder="main *">
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>Repo Path</label>
                        <input v-model="gitRepoPath" class="form-control" type="text" placeholder="/tmp/repo *">
                      </div>
                    </div>
                    <div class="col">
                      <div class="mb-3">
                        <label>File Filter</label>
                        <input v-model="gitFileFilter" class="form-control" type="text" placeholder=".md *">
                      </div>
                    </div>
                  </div>                 
                </div>

                <div class="row" v-else-if="isSnowflake">
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>DB User</label>
                        <input v-model="dbUser" class="form-control" type="text" placeholder="DB User *">
                      </div>
                    </div>
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Password</label>
                        <input v-model="dbPassword" class="form-control" type="text" placeholder="DB Password *">
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Account</label>
                        <input v-model="dbAccount" class="form-control" type="text" placeholder="DB Account *">
                      </div>
                    </div>
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Role</label>
                        <input v-model="dbRole" class="form-control" type="text" placeholder="DB Role *">
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Database</label>
                        <input v-model="dbDatabase" class="form-control" type="text" placeholder="DB Database *">
                      </div>
                    </div>
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Schema</label>
                        <input v-model="dbSchema" class="form-control" type="text" placeholder="DB Schema *">
                      </div>
                    </div>                  
                  </div> 
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>DB Warehouse</label>
                        <input v-model="dbWarehouse" class="form-control" type="text" placeholder="DB Warehouse *">
                      </div>
                    </div>
                  </div> 
                  <div class="row">
                    <div class="col">
                      <div class="mb-3">
                        <label>Query</label>
                        <input v-model="dbQuery" class="form-control" type="text" placeholder="Query *">
                      </div>
                    </div>
                  </div>                                        
                </div>  

                <div class="row" v-else>
                  <div class="col">
                    <div class="mb-3">
                      <label>API Key</label>
                      <input v-model="apiKey" class="form-control" type="text" placeholder="API Key *">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col">
                    <button type="submit" class="btn btn-primary me-2">Submit</button>
                    <router-link to="/provider/list" class="btn btn-secondary">Back to List</router-link>
                  </div>
                </div>
              </div>
            </form>

            <!-- loading area -->
            <!-- <div class="loader-box" v-if="loading">
                <div class="loader-30"></div>
            </div> -->

            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
            <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, computed } from 'vue';
import { useProviderStore } from '@/store/provider';
import { useAuthStore } from '@/store/auth';
import { useRouter, useRoute } from 'vue-router';
import { useNuxtApp } from '#app'
import restApi from "~/utils/axios";

export default {
  name: 'createProvider',
  setup() {
    const providerStore = useProviderStore();
    const router = useRouter();
    const route = useRoute();
    const selectedType = ref('M');
    const selectedProvider = ref(null);
    const providerName = ref('');
    const accessKey = ref('');
    const secretAccessKey = ref('');
    const sessionKey = ref('');
    const accessToken = ref('');
    const apiKey = ref('');
    const apiEndpoint = ref('');
    const dbUser = ref('');
    const dbPassword = ref('');
    const dbAccount = ref('');
    const dbRole = ref('');
    const dbDatabase = ref('');
    const dbSchema = ref('');
    const dbWarehouse = ref('');
    const dbQuery = ref('');
    const gitCloneUrl = ref('');
    const gitBranch = ref('');
    const gitRepoPath = ref('');
    const gitFileFilter = ref('');

    const allProviders = ref([]);
    const providers = ref([]);
    const selectedCompany = ref(null);
    const loading = ref(false);
    const errorMessage = ref(null);
    const successMessage = ref(null);
    const userId = ref(useAuthStore().userId);

    const fetchAllProviders = async () => {
      loading.value = true;
      try {
        await providerStore.fetchProviders();
        allProviders.value = providerStore.allProviders;
        filterProvidersByType(selectedType.value);
      } finally {
        loading.value = false;
      }
    };

    const filterProvidersByType = (type) => {
      providers.value = allProviders.value.filter(provider => provider.type === type);
      if (providers.value.length > 0) {
        selectedProvider.value = providers.value[0].provider_id;
        selectedCompany.value = providers.value[0].company;
      } else {
        selectedProvider.value = null;
        selectedCompany.value = null;
      }
    };
    const redirectToGoogleAuth = () => {
      const clientId = this.$config.googleClientId;
      const environment = import.meta.env.VITE_ENVIRONMENT;
      const scope = 'https://www.googleapis.com/auth/drive';
      const responseType = 'code';
      const accessType = 'offline';
      const prompt = 'consent'
      let authUrl;

      if (environment === 'local'){
        const redirectUri = 'http://localhost:5006/google/callback';
        authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&response_type=${responseType}&access_type=${accessType}&prompt=${prompt}`;

      }else{
        const redirectUri = 'https://management.cloudwiz-ai.com/google/callback';
        authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&response_type=${responseType}&access_type=${accessType}&prompt=${prompt}`;
      }
      window.location.href = authUrl;
    };
    
    const redirectToGoogleAuth_v2 = async () => {
      const { $googleAuth } = useNuxtApp()
      let providerStore = useProviderStore()

      try {
        console.log($googleAuth);
        let code = await $googleAuth.getAuthCode()
        console.log('authCode: ' + code)

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
        }

        await providerStore.createCredential(credentialData)

        sessionStorage.removeItem('userId')
        sessionStorage.removeItem('selectedProvider')
        sessionStorage.removeItem('providerName')
        router.push('/provider/list')
      } catch (error) {
        console.error('Google Sign-In error', error)
        router.push('/provider/list')
      }
    };

    const redirectToGoogleAuth_v3 = async () => {
      const { signIn } = useAuth();
      await signIn('google')
    };

    const isAmazonWebServices = computed(() => {
      return selectedCompany.value && (selectedCompany.value.includes('Amazon') || selectedCompany.value.includes('Bedrock'));
    });

    const isGit = computed(() => {
      return selectedCompany.value && (selectedCompany.value.includes('GIT'));
    });

    const isNotion = computed(() => {
      return selectedCompany.value && (selectedCompany.value.includes('Notion'));
    });    

    const isGoogleDrive = computed(() => {
      return selectedCompany.value && selectedCompany.value.includes('Google');
    });

    const isSnowflake = computed(() => {
      return selectedCompany.value && selectedCompany.value.includes('Snowflake');
    });    

    const createCredential = async (credentialData) => {
      loading.value = true;
      errorMessage.value = null;
      successMessage.value = null;

      try {
        await providerStore.createCredential(credentialData);
        successMessage.value = 'Credential created successfully.';
        router.push('/provider/list');
      } catch (error) {
        errorMessage.value = 'An error occurred while creating the credential.';
      } finally {
        loading.value = false;
      }
    };

    const handleSubmit = async () => {

      const selectedProviderObj = allProviders.value.find(provider => provider.provider_id === selectedProvider.value);

      if (selectedProviderObj && selectedProviderObj.pvd_key === 'GD') {
        sessionStorage.setItem('userId', userId.value);
        sessionStorage.setItem('selectedProvider', selectedProvider.value);
        sessionStorage.setItem('providerName', providerName.value);
        redirectToGoogleAuth();
        // redirectToGoogleAuth_v2();
        // redirectToGoogleAuth_v3();
      } else {
        await createCredential({
          user_id: userId.value,
          provider_id: selectedProvider.value,
          credential_name: providerName.value,
          
          access_key: accessKey.value,
          secret_key: secretAccessKey.value,
          session_key: sessionKey.value,
          access_token: accessToken.value,
          api_key: apiKey.value,
          api_endpoint: apiEndpoint.value,
          db_user: dbUser.value,
          db_password: dbPassword.value,
          db_account: dbAccount.value,
          db_role: dbRole.value,
          db_database: dbDatabase.value,
          db_schema: dbSchema.value,
          db_warehouse: dbWarehouse.value,
          db_query: dbQuery.value,
          git_clone_url: gitCloneUrl.value,
          git_branch: gitBranch.value,
          git_repo_path: gitRepoPath.value,
          git_file_filter: gitFileFilter.value,

          creator_id: userId.value,
          updater_id: userId.value
        });
      }
    };

    const handleGoogleCallback = async () => {
      const code = route.query.code;
      if (code) {
        try {
          const selectedProviderObj = providers.value.find(provider => provider.provider_id === selectedProvider.value);
          const providerNameValue = providerName.value;

          if (!selectedProviderObj || !providerNameValue) {
            errorMessage.value = 'Provider or provider name is not selected properly.';
            return;
          }
          providerStore.setUserId(userId.value);
          providerStore.setSelectedProvider(selectedProvider.value);
          providerStore.setProviderName(providerName.value);
          await providerStore.createGoogleCredential(code, userId.value, selectedProviderObj.provider_id, providerNameValue);
        } catch (error) {
          errorMessage.value = 'Google Drive Authentication failed';
        }
      }
    };


    onMounted(() => {
      fetchAllProviders();
      handleGoogleCallback();
    });

    watch(selectedType, (newType) => {
      filterProvidersByType(newType);
    });

    watch(selectedProvider, (newProviderId) => {
      const selectedProviderObj = providers.value.find(provider => provider.provider_id === newProviderId);
      if (selectedProviderObj) {
        selectedCompany.value = selectedProviderObj.company;
      }
    });

    return {
      selectedType,
      selectedProvider,
      providerName,

      accessKey,
      secretAccessKey,
      sessionKey,
      accessToken,
      apiKey,
      apiEndpoint,
      dbUser,
      dbPassword,
      dbAccount,
      dbRole,
      dbDatabase,
      dbSchema,
      dbWarehouse,
      dbQuery,
      gitCloneUrl,
      gitBranch,
      gitRepoPath,
      gitFileFilter,
      allProviders,
      providers,
      isAmazonWebServices,
      isGit,
      isNotion,
      isGoogleDrive,
      isSnowflake,
      loading,
      errorMessage,
      successMessage,
      handleSubmit,
    };
  }
}
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 검정색 배경, 투명도 조절 가능 */
  z-index: 999; /* 로딩 오버레이가 최상위에 오도록 설정 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-box {
  width: 100px; /* 로딩 바의 너비 설정 */
  height: 100px; /* 로딩 바의 높이 설정 */
  background-color: #fff; /* 로딩 바의 배경색 */
  border-radius: 10px; /* 로딩 바 모서리 둥글게 */
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.5); /* 로딩 바에 그림자 효과 추가 */
}
</style>