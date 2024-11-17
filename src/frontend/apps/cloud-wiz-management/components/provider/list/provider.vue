<template>
  <div class="col-md-12 project-list">
    <div class="card">
      <div class="row">
        <div class="col-md-6 d-flex">
          <ul class="nav nav-tabs border-tab" id="top-tab" role="tablist">
            <li v-for="(item,index) in tab" :key="index" class="nav-item">
              <a class="nav-link" :class="{ 'active': item.active }" :id="item.label" data-bs-toggle="tab" href="javascript:void(0)" role="tab" :aria-controls="item.id" :aria-selected="item.active ? 'true':'false'" @click.prevent="active(item)">
                <vue-feather :type="item.icon"></vue-feather>{{ item.name }}
              </a>
            </li>
          </ul>
        </div>
        <div class="col-md-6">
          <div class="form-group mb-0 me-0"></div>
          <nuxt-link class="btn btn-primary" to="/provider/create">
            <vue-feather class="me-1" type="plus-square"> </vue-feather>Add Provider
          </nuxt-link>
        </div>
      </div>
    </div>
  </div>
  <div class="col-sm-12">
    <div class="card">
      <div class="card-body">

        <!-- loading area -->
        <div class="loader-box" v-if="loading">
          <div class="loader-30"></div>
        </div> 
        
        <div class="tab-content" id="top-tabContent"> 
          <div v-for="(item, index) in tab" :key="index" :class="{ 'tab-pane': true, 'fade': !item.active, 'active show': item.active }" :id="item.id" role="tabpanel" :aria-labelledby="item.label">
            <div class="row">
              <div class="col-lg-4 col-md-6" v-for="(dataItem, dataIndex) in filteredData" :key="dataIndex">
                  <div class="project-box" @click="navigateToEdit(dataItem.credential_id)" @mouseover="onMouseOver" @mouseleave="onMouseLeave">
                    <span class="badge" :class="getBadgeClass(dataItem.provider_type)">{{ getBadgeLabel(dataItem.provider_type) }}</span>
                      <h6>{{ dataItem.credential_name }}</h6>
                      <div class="d-flex mb-3"><img class="img-20 me-2 rounded-circle" :src="`/images/provider/${dataItem.provider_logo}`" alt="" data-original-title="" title="">
                          <div class="flex-grow-1 project-box-item">
                              <p>{{ dataItem.provider_company }}</p>
                          </div>
                      </div>
                      <p>{{ dataItem.provider_desc }}</p>
                      <div class="row details" v-if="!dataItem.inner_used">
                          <div class="col-6" v-if="dataItem.access_key"><span>Access Key </span></div>
                          <div class="col-6 font-primary" v-if="dataItem.access_key">{{ dataItem.access_key }} </div>
                          <div class="col-6" v-if="dataItem.secret_key"> <span>Secret Access Key</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.secret_key">{{ dataItem.secret_key }}</div>
                          <div class="col-6" v-if="dataItem.session_key"> <span>Session Key</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.session_key">{{ dataItem.session_key }}</div>
                          <div class="col-6" v-if="dataItem.access_token"> <span>Access Token</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.access_token">{{ dataItem.access_token }}</div>
                          <div class="col-6" v-if="dataItem.api_key"> <span>API Key</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.api_key">{{ dataItem.api_key }}</div>
                          <div class="col-6" v-if="dataItem.db_database"> <span>DB Database</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.db_database">{{ dataItem.db_database }}</div>                          
                          <!-- <div class="col-6" v-if="dataItem.client_id"><span>Google Client ID</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.client_id">{{ dataItem.client_id }}</div>
                          <div class="col-6" v-if="dataItem.auth_secret_key"><span>Auth Secret Key</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.auth_secret_key">{{ dataItem.auth_secret_key }}</div> -->
                      </div>

                      <div class="row details" v-if="dataItem.provider_type != 'L'">
                          <div class="col-6"><span>Used </span></div>
                          <div class="col-6 font-primary">{{ formatTokenSize(dataItem.expected_count) }} </div>
                          <div class="col-6" v-if="dataItem.inner_used"> <span>Limit</span></div>
                          <div class="col-6 font-primary" v-if="dataItem.inner_used">{{ formatTokenSize(dataItem.limit_cnt) }}</div>
                      </div>

                      <div class="project-status mt-4" v-if="dataItem.inner_used">
                        <div class="d-flex mb-0">
                            <p>{{ calculatePercentage(dataItem.expected_count, dataItem.limit_cnt) }}% </p>
                            <div class="flex-grow-1 text-end"><span>Expiry</span></div>
                        </div>
                        <div class="progress" style="height: 5px">
                            <div class="progress-bar-animated  progress-bar-striped" :class="'badge-secondary'" role="progressbar"
                                :style="{ 'width': calculatePercentage(dataItem.expected_count, dataItem.limit_cnt)+'%' }" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>                      
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div> 
</template>
  
<script>
import { useProviderStore } from '@/store/provider';
import { useAuthStore } from '@/store/auth';
import { mapState, mapActions } from 'pinia';

export default {
  name: 'ListProvider',
  data() {
    return {
      tab: [
        { type: 'all', name: 'All', active: true, icon: 'target', id: 'top-all', label: 'all-tab' },
        { type: 'M', name: 'Model', active: false, icon: 'cpu', id: 'top-model', label: 'model-tab' },
        { type: 'S', name: 'Storage', active: false, icon: 'database', id: 'top-storage', label: 'storage-tab' },
        { type: 'L', name: 'Document Loader', active: false, icon: 'database', id: 'top-dl', label: 'dl-tab' },
        { type: 'V', name: 'VectorDB', active: false, icon: 'database', id: 'top-vector', label: 'vector-tab' }
      ],
      loading: false,
      userId: useAuthStore().userId

    };
  },
  computed: {
    ...mapState(useProviderStore, ['credentials']),
    filteredData() {
      if (this.activeTab.type === 'all') return this.credentials;
      return this.credentials.filter(provider => provider.provider_type === this.activeTab.type);
    },
    activeTab() {
      return this.tab.find(t => t.active);
    }
  },
  methods: {
    ...mapActions(useProviderStore, ['fetchCredential']),
    active(item) {
      this.tab.forEach(a => (a.active = false));
      item.active = true;
    },
    mask(value) {
      if (value.length <= 3) return value;
      return value.slice(0, 3) + '*************';
    },
    navigateToEdit(credentialId) {
      this.$router.push({ path: '/provider/modify', query: { credentialId: credentialId } });
    },
    onMouseOver(event) {
      event.currentTarget.classList.add('hover');
    },
    onMouseLeave(event) {
      event.currentTarget.classList.remove('hover');
    },
    getBadgeClass(type) {
      switch (type) {
        case 'M':
          return 'badge-primary';
        case 'S':
          return 'badge-secondary';
        case 'V':
          return 'badge-info';  
        case 'L':
          return 'badge-info';                      
        default:
          return '';
      }
    },
    getBadgeLabel(type) {
      switch (type) {
        case 'M':
          return 'model';
        case 'S':
          return 'storage';
        case 'V':
          return 'vector';
        case 'L':
          return 'document loader';          
        default:
          return '';
      }
    },
    calculatePercentage(expectedCount, limitCnt) {
      if (limitCnt === 0) {
        return 0;
      } else {
        return ((expectedCount / limitCnt) * 100).toFixed(3);
      }
    },
    formatTokenSize(bytes) {
      if (bytes === 0) return '0 B';
      const units = ['B', 'KB', 'MB', 'GB', 'TB'];
      const decimalPlaces = 3;
      const k = 1024;
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(decimalPlaces)) + ' ' + units[i];
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
};
</script>

<style scoped>
.project-box {
  transition: transform 0.3s;
  cursor: pointer;
}
.project-box h6 {
    font-weight: bold;
}
.project-box.hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>  