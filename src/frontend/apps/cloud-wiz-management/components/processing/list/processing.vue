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
          <nuxt-link class="btn btn-primary" to="/processing/create">
            <vue-feather class="me-1" type="plus-square"> </vue-feather>Create New Processing
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
                  <div class="project-box" @click="navigateToEdit(dataItem.processing_id)" @mouseover="onMouseOver" @mouseleave="onMouseLeave">
                    <span class="badge" :class="getBadgeClass(dataItem.processing_type)">{{ dataItem.processing_type }}</span>
                      <h6>{{ dataItem.processing_name }}</h6>
                      <div class="d-flex mb-3">
                          <div class="flex-grow-1 project-box-item">
                              <p>{{ dataItem.processing_desc }}</p>
                          </div>
                      </div>
                      <!-- Additional details as needed -->
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
  import { useProcessingStore } from '@/store/processing';
  import { useAuthStore } from '@/store/auth';
  import { mapState, mapActions } from 'pinia';
  
  export default {
    name: 'ListProcessing',
    data() {
      return {
        tab: [
          { type: 'all', name: 'All', active: true, icon: 'target', id: 'top-all', label: 'all-tab' },
          { type: 'pre', name: 'Pre-Processing', active: false, icon: 'chevrons-left', id: 'top-pre', label: 'pre-tab' },
          { type: 'post', name: 'Post-Processing', active: false, icon: 'chevrons-right', id: 'top-post', label: 'post-tab' }
        ],
        loading: false,        
        userId: useAuthStore().userId
      };
    },
    computed: {
      ...mapState(useProcessingStore, ['processings']),
      filteredData() {
        if (this.activeTab.type === 'all') return this.processings;
        return this.processings.filter(process => process.processing_type === this.activeTab.type);
      },
      activeTab() {
        return this.tab.find(t => t.active);
      }
    },
    methods: {
      ...mapActions(useProcessingStore, ['fetchProcessingsById']),
      active(item) {
        this.tab.forEach(a => (a.active = false));
        item.active = true;
      },
      navigateToEdit(processingId) {
        this.$router.push({ path: '/processing/create', query: { processingId: processingId } });
      },
      onMouseOver(event) {
        event.currentTarget.classList.add('hover');
      },
      onMouseLeave(event) {
        event.currentTarget.classList.remove('hover');
      },
      getBadgeClass(type) {
        switch (type) {
          case 'pre':
            return 'badge-primary';
          case 'post':
            return 'badge-secondary';
          default:
            return '';
        }
      },
      async fetchData() {
        try {
          this.loading = true;
          useProcessingStore().processings = [];
          await this.fetchProcessingsById({ userId: this.userId });
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