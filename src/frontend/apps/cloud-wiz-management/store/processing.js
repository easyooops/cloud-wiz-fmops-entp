import { defineStore } from 'pinia';
import restApi from '@/utils/axios';

export const useProcessingStore = defineStore({
  id: 'processing',
  state: () => ({
    processings: [],
    loading: false,
    error: null
  }),
  getters: {
    allProcessings: (state) => state.processings,
    getProcessingById: (state) => (id) => state.processings.find(processing => processing.processing_id === id)
  },
  actions: {
    async fetchProcessings() {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get('/processing/', null);
        this.processings = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async fetchProcessingsById({ userId }) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/processing/?user_id=${userId}`, null);
        this.processings = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },    
    async fetchProcessingsByType(processing_type) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/processing/?processing_type=${processing_type}`, null);
        this.processings = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async createProcessing(processingData) {
      this.loading = true;
      this.error = null;
      try {
        const { post } = restApi();
        await post('/processing/', processingData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async updateProcessing(processingData) {
      this.loading = true;
      this.error = null;
      try {
        const { put } = restApi();
        await put(`/processing/${processingData.processing_id}`, processingData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async deleteProcessing(processingId) {
      this.loading = true;
      this.error = null;
      try {
        const { del } = restApi();
        await del(`/processing/${processingId}`);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
