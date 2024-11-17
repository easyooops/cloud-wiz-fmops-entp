<template>
    <div class="col-md-12 project-list">
      <div class="card">
        <div class="row">
          <div class="col-md-6 d-flex">
            <ul class="nav nav-tabs border-tab" id="top-tab" role="tablist">
              <li v-for="(item, index) in tab" :key="index" class="nav-item">
                <a class="nav-link" :class="{ 'active': item.active }" :id="item.label" data-bs-toggle="tab" href="javascript:void(0)" role="tab" :aria-controls="item.id" :aria-selected="item.active ? 'true':'false'" @click.prevent="active(item)">
                  <vue-feather :type="item.icon"></vue-feather>{{ item.name }}
                </a>
              </li>
            </ul>
          </div>
          <div class="col-md-6">
            <div class="form-group mb-0 me-0"></div>
            <nuxt-link class="btn btn-primary" to="/agent/create">
              <vue-feather class="me-1" type="plus-square"> </vue-feather>New Create Agent
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
                  <div class="project-box" @click="navigateToEdit(dataItem.agent_id)" @mouseover="onMouseOver" @mouseleave="onMouseLeave">
                    <span class="badge" :class="getBadgeClass(dataItem.fm_provider_type, dataItem.embedding_enabled)">{{ getBadgeLabel(dataItem.fm_provider_type, dataItem.embedding_enabled) }}</span>
                    <h6>{{ dataItem.agent_name }}</h6>
                    <p>{{ dataItem.agent_description }}</p>
                    <div class="row details">
                        <div class="col-6">
                            <span>Request Count</span>
                        </div>
                        <div class="col-6 font-primary">
                            {{ dataItem.expected_request_count }}
                        </div>
                        <div class="col-6">
                            <span>Token Count</span>
                        </div>
                        <div class="col-6 font-primary">
                            {{ formatTokenSize(dataItem.expected_token_count) }}
                        </div>
                        <div class="col-6">
                            <span>Expected Cost</span>
                        </div>
                        <div class="col-6 font-primary">
                            {{ formatCost(dataItem.expected_cost) }}
                        </div>
                    </div>

                    <div class="customers mt-3">
                        <ul>
                            <li class="d-inline-block"><i class="fa fa-code-fork"></i></li>
                            <li class="d-inline-block" v-if="dataItem.embedding_enabled"><i class="fa fa-database"></i></li>
                            <li class="d-inline-block" v-if="dataItem.processing_enabled"><i class="fa fa-cogs"></i></li>
                            <li class="d-inline-block ms-2">
                                <p class="f-12">{{ calculateLikeCount(dataItem) }} chain</p>
                            </li>
                        </ul>
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
  import { useAgentStore } from '@/store/agent';
  import { useAuthStore } from '@/store/auth';
  import { mapState, mapActions } from 'pinia';
  
  export default {
    name: 'ListAgent',
    data() {
      return {
        tab: [
          { type: 'all', name: 'All', active: true, icon: 'target', id: 'top-all', label: 'all-tab' },
          { type: 'T', name: 'Text', active: false, icon: 'file-text', id: 'top-text', label: 'text-tab' },
          { type: 'C', name: 'Chat', active: false, icon: 'message-circle', id: 'top-chat', label: 'chat-tab', hidden: true },
          { type: 'E', name: 'Embedding', active: false, icon: 'database', id: 'top-embedding', label: 'embedding-tab' },
          { type: 'I', name: 'Image', active: false, icon: 'image', id: 'top-image', label: 'image-tab' }
        ],
        loading: false,        
        userId: useAuthStore().userId
      };
    },
    computed: {
      ...mapState(useAgentStore, ['agents']),
      filteredData() {
        if (this.activeTab.type === 'all') return this.agents;
        return this.agents.filter(agent => {
          if (this.activeTab.type === 'E' && agent.embedding_enabled) {
            return true;
          }
          return agent.fm_provider_type === this.activeTab.type;
        });
      },
      activeTab() {
        return this.tab.find(t => t.active);
      }
    },
    methods: {
      ...mapActions(useAgentStore, ['fetchAgentByUserId']),
      active(item) {
        this.tab.forEach(a => (a.active = false));
        item.active = true;
      },
      getBadgeClass(type, embeddingEnabled) {
        if (embeddingEnabled) return 'bg-success';
        switch (type) {
          case 'T':
            return 'badge-primary';
          case 'C':
            return 'badge-secondary';
          case 'I':
            return 'badge-info';
          default:
            return '';
        }
      },
      getBadgeLabel(type, embeddingEnabled) {
        if (embeddingEnabled) return 'embedding';
        switch (type) {
          case 'T':
            return 'text';
          case 'C':
            return 'chat';
          case 'I':
            return 'image';
          default:
            return '';
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
      formatCost(cost) {
            return parseFloat(cost).toFixed(3) + ' $';
      },        
      navigateToEdit(agentId) {
        this.$router.push({ path: '/agent/create', query: { agentId: agentId } });
      },
      onMouseOver(event) {
        event.currentTarget.classList.add('hover');
      },
      onMouseLeave(event) {
        event.currentTarget.classList.remove('hover');
      },
      calculateLikeCount(dataItem) {
        let likeCount = 1;
        
        if (dataItem.embedding_enabled) {
          likeCount++;
        }
        if (dataItem.processing_enabled) {
          likeCount++;
        }
        
        return likeCount;
      },
      async fetchData() {
        try {
          this.loading = true;
          useAgentStore().agents = [];
          await this.fetchAgentByUserId({ userId: this.userId });
          this.loading = false;

        } catch (error) {
          console.error('Error fetching data:', error);
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
.fa {
    font: normal normal normal 25px / 1 FontAwesome;
    margin-right: 10px;
}
.customers li i.fa {
    margin-right: 20px;
}
</style>
  