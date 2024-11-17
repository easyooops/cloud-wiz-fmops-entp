<template>
    <Breadcrumbs main="Provider" title="Provider Modify" />

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
                        <form>
                            <div class="form theme-form">
                                <div class="row">
                                    <div class="col-sm-4">
                                        <div class="mb-3">
                                            <label>Provider Type</label>
                                            <select class="form-select" v-model="selectedType" disabled>
                                                <option :value="'M'">Model</option>
                                                <option :value="'S'">Storage</option>
                                                <option :value="'L'">Document Loader</option>
                                                <option :value="'V'">VectorDB</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-4">
                                        <div class="mb-3">
                                            <label>Provider</label>
                                            <select class="form-select" v-model="selectedProvider" disabled>
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
                                            <input v-model="providerName" class="form-control" type="text" placeholder="Provider Name *" required  disabled>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="!innerUsed">
                                    <div class="row" v-if="isAmazonWebServices">
                                        <div class="col">
                                            <div class="mb-3">
                                                <label>Access Key</label>
                                                <input v-model="accessKey" class="form-control" type="text" placeholder="Access Key *" disabled>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <div class="mb-3">
                                                <label>Secret Access Key</label>
                                                <input v-model="secretAccessKey" class="form-control" type="text" placeholder="Secret Access Key *" disabled>
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
                                                <input v-model="accessToken" class="form-control" type="text" placeholder="Access Token *" disabled>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <div class="mb-3">
                                                <label>DB Database</label>
                                                <input v-model="dbDatabase" class="form-control" type="text" placeholder="DB Database *" disabled>
                                            </div>
                                        </div>                  
                                    </div>
                                    <div class="row" v-else-if="isGit">
                                        <div class="row">
                                            <div class="col">
                                                <div class="mb-3">
                                                    <label>Clone URL</label>
                                                    <input v-model="gitCloneUrl" class="form-control" type="text" placeholder="CLONE URL *" disabled>
                                                </div>
                                            </div>
                                            <div class="col">
                                                <div class="mb-3">
                                                    <label>Branch</label>
                                                    <input v-model="gitBranch" class="form-control" type="text" placeholder="main *" disabled>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col">
                                                <div class="mb-3">
                                                    <label>Repo Path</label>
                                                    <input v-model="gitRepoPath" class="form-control" type="text" placeholder="/tmp/repo *" disabled>
                                                </div>
                                            </div>
                                            <div class="col">
                                                <div class="mb-3">
                                                    <label>File Filter</label>
                                                    <input v-model="gitFileFilter" class="form-control" type="text" placeholder=".md *" disabled>
                                                </div>
                                            </div>
                                        </div>                 
                                    </div>

                                    <div class="row" v-else-if="isSnowflake">
                                        <div class="row">
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB User</label>
                                                <input v-model="dbUser" class="form-control" type="text" placeholder="DB User *" disabled>
                                            </div>
                                            </div>
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Password</label>
                                                <input v-model="dbPassword" class="form-control" type="text" placeholder="DB Password *" disabled>
                                            </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Account</label>
                                                <input v-model="dbAccount" class="form-control" type="text" placeholder="DB Account *" disabled>
                                            </div>
                                            </div>
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Role</label>
                                                <input v-model="dbRole" class="form-control" type="text" placeholder="DB Role *" disabled>
                                            </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Database</label>
                                                <input v-model="dbDatabase" class="form-control" type="text" placeholder="DB Database *" disabled>
                                            </div>
                                            </div>
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Schema</label>
                                                <input v-model="dbSchema" class="form-control" type="text" placeholder="DB Schema *" disabled>
                                            </div>
                                            </div>                  
                                        </div> 
                                        <div class="row">
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>DB Warehouse</label>
                                                <input v-model="dbWarehouse" class="form-control" type="text" placeholder="DB Warehouse *" disabled>
                                            </div>
                                            </div>
                                        </div> 
                                        <div class="row">
                                            <div class="col">
                                            <div class="mb-3">
                                                <label>Query</label>
                                                <input v-model="dbQuery" class="form-control" type="text" placeholder="Query *" disabled>
                                            </div>
                                            </div>
                                        </div>                                        
                                        </div>
                                                                            
                                    <div class="row" v-else>
                                        <div class="col">
                                            <div class="mb-3">
                                                <label>API Key</label>
                                                <input v-model="apiKey" class="form-control" type="text" placeholder="API Key *" disabled>
                                            </div>
                                        </div>
                                    </div>     
                                </div>       
                                <div class="row">
                                    <div class="col mt-3">
                                        <!-- <button type="submit" class="btn btn-primary me-2">Update</button> -->
                                        <button @click.prevent="deleteCredential" class="btn btn-danger me-2">Delete</button>
                                        <router-link to="/provider/list" class="btn btn-secondary">Back to List</router-link>
                                    </div>
                                </div>                                              
                            </div>
                        </form>

                        <!-- loading area -->
                        <!-- <div class="loader-box" v-if="loading">
                            <div class="loader-30"></div>
                        </div>                         -->
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
import { useRouter } from 'vue-router';

export default {
    name: 'ModifyProvider',
    setup() {
        const providerStore = useProviderStore();
        const router = useRouter();
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
        const credentialId = ref(null);
        const innerUsed = ref(null);
        const limitCnt = ref(null);

        const fetchAllProviders = async () => {
            loading.value = true;
            try {
                await providerStore.fetchProviders();
                allProviders.value = providerStore.allProviders;
            } finally {
            }
        };

        const fetchCredentialData = async () => {
            
            try {
                credentialId.value = String(router.currentRoute.value.query.credentialId);
                await providerStore.fetchCredentialById(credentialId.value);
                const credential = providerStore.credential;
                selectedType.value = credential.provider_type;
                selectedProvider.value = credential.provider_id;
                providerName.value = credential.credential_name;
                accessKey.value = credential.access_key;
                secretAccessKey.value = credential.secret_key;
                sessionKey.value = credential.session_key;
                accessToken.value = credential.access_token;
                apiKey.value = credential.api_key;
                apiEndpoint.value = credential.api_endpoint;
                dbUser.value = credential.db_user;
                dbPassword.value = credential.db_password;
                dbAccount.value = credential.db_account;
                dbRole.value = credential.db_role;
                dbDatabase.value = credential.db_database;
                dbSchema.value = credential.db_schema;
                dbWarehouse.value = credential.db_warehouse;
                dbQuery.value = credential.db_query;
                gitCloneUrl.value = credential.git_clone_url;
                gitBranch.value = credential.git_branch;
                gitRepoPath.value = credential.git_repo_path;
                gitFileFilter.value = credential.git_file_filter;

                innerUsed.value = credential.inner_used;
                limitCnt.value = credential.limit_cnt;

                filterProvidersByType(selectedType.value);
            } catch (error) {
                errorMessage.value = 'An error occurred while fetching the credential data.';
            } finally {
                loading.value = false;
            }
        };

        const filterProvidersByType = (type) => {
            providers.value = allProviders.value.filter(provider => provider.type === type);
            const selectedProviderObj = providers.value.find(provider => provider.provider_id === selectedProvider.value);
            if (selectedProviderObj) {
                selectedCompany.value = selectedProviderObj.company;
            } else {
                selectedProvider.value = providers.value[0].provider_id;
                selectedCompany.value = providers.value[0].company;
            }       
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

        const updateCredential = async () => {
            loading.value = true;
            errorMessage.value = null;
            successMessage.value = null;

            try {
                await providerStore.updateCredential({
                    credential_id: credentialId.value,
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

                    updater_id: userId.value
                });
                successMessage.value = 'Credential updated successfully.';
                router.push('/provider/list');
            } catch (error) {
                errorMessage.value = 'An error occurred while updating the credential.';
            } finally {
                loading.value = false;
            }
        };

        const deleteCredential = async () => {
            loading.value = true;
            errorMessage.value = null;
            successMessage.value = null;

            try {
                await providerStore.deleteCredential(credentialId.value);
                successMessage.value = 'Credential deleted successfully.';
            } catch (error) {
                errorMessage.value = 'An error occurred while deleting the credential.';
            } finally {
                loading.value = false;
                router.push('/provider/list');
            }
        };

        onMounted(async () => {
            await fetchAllProviders();
            await fetchCredentialData();
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
            innerUsed,
            limitCnt,
            providers,
            isAmazonWebServices,
            isGit,
            isNotion,
            isGoogleDrive,
            isSnowflake,
            loading,
            errorMessage,
            successMessage,
            updateCredential,
            deleteCredential
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
