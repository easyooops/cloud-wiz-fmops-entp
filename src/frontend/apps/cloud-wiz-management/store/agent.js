import { defineStore } from 'pinia';
import restApi from '@/utils/axios';

export const useAgentStore = defineStore({
  id: 'agent',
  state: () => ({
    agents: [],
    agent: null,
    loading: false,
    error: null,
    llmsResponse: null
  }),
  getters: {
    allAgents: (state) => state.agents,
    getAgentById: (state) => (id) => state.agents.find(agent => agent.agent_id === id)
  },
  actions: {
    async fetchAgents() {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get('/agent/');
        this.agents = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async fetchAgentById(agentId) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/agent/${agentId}`);
        this.agent = response.data;
        if (!this.agent) {
          throw new Error('Agent not found');
        }
      } catch (error) {
        this.error = error;
        router.push('/agent/list');
      } finally {
        this.loading = false;
      }
    },
    async fetchAgentByUserId({ userId }) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/agent/?user_id=${userId}`, null);
        this.agents = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },     
    async createAgent(agentData) {
      this.loading = true;
      this.error = null;
      try {
        const { post } = restApi();
        const response = await post('/agent/', agentData);
        this.agent = response.data;        
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async updateAgent(agentData) {
      this.loading = true;
      this.error = null;
      try {
        const { put } = restApi();
        await put(`/agent/${agentData.agent_id}`, agentData);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async deleteAgent(agentId) {
      this.loading = true;
      this.error = null;
      try {
        const { del } = restApi();
        await del(`/agent/${agentId}`);
      } catch (error) {
        throw error;
      } finally {
        this.loading = false;
      }
    },
    async fetchLLMS(agentId, query) {
      this.loading = true;
      this.error = null;
      try {
        const { get } = restApi();
        const response = await get(`/agent/prompt/${agentId}?query=${encodeURIComponent(query)}`);
        this.llmsResponse = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async resetAgent() {
      this.agent = null;
    }     
  },
});
