import { defineStore } from 'pinia';
import restApi from '@/utils/axios';

export const useOpinionStore = defineStore({
  id: 'opinion',
  state: () => ({
    opinions: [],
    opinion: null,
    loading: false,
    error: null,
  }),
  getters: {
    allOpinions: (state) => state.opinions,
    getOpinionById: (state) => (id) => state.opinions.find(opinion => opinion.opinion_id === id)
  },
  actions: {
    async fetchOpinions() {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get('/opinion/');
        this.opinions = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async fetchOpinionById(opinionId) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/opinion/${opinionId}`);
        this.opinion = response.data;
        if (!this.opinion) {
          throw new Error('Opinion not found');
        }
      } catch (error) {
        this.error = error;
        router.push('/opinions/list');
      } finally {
        this.loading = false;
      }
    },
    async createOpinion(opinionData) {
      this.loading = true;
      this.error = null;
      try {
        const { post } = restApi();
        const response = await post('/opinion/', opinionData);
        this.opinion = response.data;        
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async updateOpinion(opinionData) {
      this.loading = true;
      this.error = null;
      try {
        const { put } = restApi();
        await put(`/opinion/${opinionData.opinion_id}`, opinionData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async deleteOpinion(opinionId) {
      this.loading = true;
      this.error = null;
      try {
        const { del } = restApi();
        await del(`/opinion/${opinionId}`);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async resetOpinion() {
      this.opinion = null;
    }     
  },
});
