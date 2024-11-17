import { defineStore } from 'pinia';
import restApi from '@/utils/axios';

export const useStorageStore = defineStore({
  id: 'storage',
  state: () => ({
    storages: [],
    storageDetail: null,
    loading: false,
    error: null
  }),
  getters: {
    allStorages: (state) => state.storages,
    getStorageById: (state) => (id) => state.storages.find(storage => storage.id === id)
  },
  actions: {
    async fetchAllStorages(userId) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/store/${userId}`);
        this.storages = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async fetchStorageById(userId, storageId) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/store/${userId}/${storageId}`);
        this.storageDetail = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async createStorage(storageData) {
      this.loading = true;
      this.error = null;
      try {
        const { post } = restApi();
        await post(`/store/${storageData.user_id}`, storageData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async updateStorage(userId, storageData) {
      this.loading = true;
      this.error = null;
      try {
        const { put } = restApi();
        await put(`/store/${userId}/${storageData.id}`, storageData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async deleteStorage(userId, storageId) {
      this.loading = true;
      this.error = null;
      try {
        const { del } = restApi();
        await del(`/store/${userId}/${storageId}`);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async createIndexing(embeddings) {
      this.loading = true;
      this.error = null;
      try {
        const { put } = restApi();
        await put(`/store/${embeddings.user_id}/${embeddings.storage_provider_id}/indexing`, embeddings);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },    
    async uploadFile(userId, file, storageId) {
      this.loading = true;
      this.error = null;
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const { post } = restApi();
        await post(`/store/${userId}/${storageId}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async fetchFiles(userId, storageId) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/store/${userId}/${storageId}/files`);
        return response.data;
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async deleteFile(userId, storageId, fileKey) {
      this.loading = true;
      this.error = null;
      try {
        const { del } = restApi();
        await del(`/store/${userId}/${storageId}/files/${fileKey}`);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
  }
});
