<template>
    <Breadcrumbs main="Storage" title="Storage Create" />
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <div class="loader-overlay" v-if="loading">
                    <div class="loader-box">
                        <div class="loader-30"></div>
                    </div>
                </div>

                <form @submit.prevent="createStorage">
                    <div class="card">
                        <div class="card-body">                                    
                            <div class="row">
                                <div class="col-xl-4 mb-3">
                                    <div class="col-form-label">Storage Provider *</div>
                                    <select class="form-select form-control-primary" v-model="selectedProvider">
                                        <option value="" disabled hidden>Select Storage Provider</option>
                                        <option v-for="provider in filteredProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                    </select>
                                </div>                                            
                            </div>                            
                            <!-- <div class="row">
                                <div class="col-xl-4 mb-3">
                                    <div class="col-form-label">Vector Provider *</div>
                                    <select class="form-select form-control-primary" v-model="selectedVectorProvider">
                                        <option value="" disabled hidden>Select Vector Provider</option>
                                        <option v-for="provider in filteredVectorProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                    </select>
                                </div>                                            
                            </div>                             -->
                        </div>
                    </div> 

                    <div class="card">
                        <div class="card-body">
                            <div class="form theme-form"> 
                                <div class="row">
                                    <div class="col">
                                        <div class="mb-3">
                                            <label>Storage Name</label>
                                            <input v-model="storageName" class="form-control" type="text" placeholder="Storage Name *" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <div class="mb-5">
                                            <label>Storage Description</label>
                                            <input v-model="storageDescription" class="form-control" type="text" placeholder="Storage Description *">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <button type="submit" class="btn btn-primary me-2">Create Storage</button>
                                        <router-link to="/storage/list" class="btn btn-secondary">Back to List</router-link>
                                    </div>
                                </div>                                                                       
                            </div>
                            
                            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
                            <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
                        </div>
                    </div>
                </form>

            </div>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { useStorageStore } from '@/store/storage';
import { useProviderStore } from '@/store/provider';
import { mapState, mapActions } from 'pinia';

export default {
    name: 'createStorage',
    data() {
        return {
            storageName: '',
            storageDescription: '',
            loading: false,
            errorMessage: null,
            successMessage: null,
            selectedProvider: '', 
            selectedVectorProvider: '', 
            userId: useAuthStore().userId,
        }
    },
    computed: {
        ...mapState(useProviderStore, ['credentials']),
        filteredProviders() {
            return this.credentials.filter(provider => provider.provider_type === "S");
        },
        filteredVectorProviders() {
            return this.credentials.filter(provider => provider.provider_type === "V");
        }        
    },
    methods: {
        ...mapActions(useProviderStore, ['fetchCredential']),
        async createStorage() {
            this.loading = true;
            this.errorMessage = null;
            this.successMessage = null;

            try {
                await useStorageStore().createStorage({
                    user_id: this.userId,
                    credential_id: this.selectedProvider,
                    store_name: this.storageName,
                    description: this.storageDescription,
                    creator_id: this.userId,
                    updater_id: this.userId
                });
                this.successMessage = 'Storage created successfully.';
                this.$router.push('/storage/list');
            } catch (error) {
                this.errorMessage = 'An error occurred while creating the storage.';
            } finally {
                this.loading = false;
                setTimeout(() => {
                    this.errorMessage = '';
                    this.successMessage = '';
                }, 2000);                 
            }
        },
        async fetchData() {
            try {
                this.loading = true;
                useProviderStore().credentials = [];
                await this.fetchCredential({ userId: this.userId });
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                this.loading = false;
            } 
        }        
    },
    async mounted() {
        await this.fetchData();         
    }
}
</script>

<style scoped>
.fa {
    font: normal normal normal 30px / 1 FontAwesome;
}
.fa-minus {
    font: normal normal normal 10px / 1 FontAwesome;
}
.fa-plus {
    font: normal normal normal 10px / 1 FontAwesome;
}
.product-name {
    margin-left: 10px;
}
.prooduct-details-box {
    cursor: pointer;
    padding: 10px;
}
.media.selected {
    border: 2px solid #007bff;
    background-color: #e7f1ff;
}
.form-control-primary {
    border-color: var(--theme-deafult);
    color: var(--theme-deafult);
}
.disabled-card {
    pointer-events: none;
    opacity: 0.6;
}
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