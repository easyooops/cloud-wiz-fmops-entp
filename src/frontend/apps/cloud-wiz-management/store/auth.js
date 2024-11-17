import { defineStore } from 'pinia';
import restApi from '@/utils/axios';

const TOKEN_KEY = 'accessToken';
const GOOGLE_TOKEN_KEY = 'googleToken';
const USER_KEY = 'userData';

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    auth: null,
    googleToken: localStorage.getItem(GOOGLE_TOKEN_KEY) || '',
    accessToken: localStorage.getItem(TOKEN_KEY) || '',
    userName: localStorage.getItem(USER_KEY) ? JSON.parse(localStorage.getItem(USER_KEY)).userName : '',
    userId: localStorage.getItem(USER_KEY) ? JSON.parse(localStorage.getItem(USER_KEY)).userId : '',    
    error: null,
    loading: false,
  }),
  actions: {
    async loginWithGoogle(token) {
      this.error = null;
      try {
        const body = {
          token: token
        };

        const { post } = restApi();
        const response = await post('/auth/', body);

        this.auth = response.data;
        if (!this.auth) {
          throw new Error('Auth not found');
        }

        this.accessToken = response.data.accessToken;
        this.userName = response.data.userName;
        this.userId = response.data.userId;

        localStorage.setItem(TOKEN_KEY, this.accessToken);
        // localStorage.setItem(GOOGLE_TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify({ userName: this.userName, userId: this.userId }));

      } catch (error) {
        this.error = error;
        console.error('Google login failed:', error);
      }
    },
    async logout() {

      try {

        const body = {
          token: this.googleToken
        };

        this.auth = null;
        this.accessToken = '';
        // this.googleToken = '';
        this.userName = '';
        this.userId = '';

        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        // localStorage.removeItem(GOOGLE_TOKEN_KEY);

        // const { post } = restApi();
        // await post('/auth/logout', body);

      } catch (error) {
        this.error = error;
        console.error('Google login failed:', error);
      }
    },
  },
  getters: {
    isAuthenticated() {
      return !!this.accessToken;
    },
  },
});


