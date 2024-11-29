import { defineStore } from 'pinia';  
import restApi from '@/utils/axios';  
  
const TOKEN_KEY = 'accessToken';  
const GOOGLE_TOKEN_KEY = 'googleToken';  
const USER_KEY = 'userData';  
  
function isTokenExpired(token) {  
  if (!token) return true;  
  const payload = JSON.parse(atob(token.split('.')[1]));  
  const expiry = payload.exp * 1000; // 만료 시간 (밀리초)  
  return Date.now() > expiry;  
}  
  
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
        const body = { token: token };  
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
        localStorage.setItem(USER_KEY, JSON.stringify({ userName: this.userName, userId: this.userId }));  
      } catch (error) {  
        this.error = error;  
        console.error('Google login failed:', error);  
      }  
    },  
    async logout() {  
      try {  
        const body = { token: this.googleToken };  
        this.auth = null;  
        this.accessToken = '';  
        this.userName = '';  
        this.userId = '';  
  
        localStorage.removeItem(TOKEN_KEY);  
        localStorage.removeItem(USER_KEY);  
      } catch (error) {  
        this.error = error;  
        console.error('Logout failed:', error);  
      }  
    },  
    clearLocalStorage() {  
      localStorage.removeItem(TOKEN_KEY);  
      localStorage.removeItem(GOOGLE_TOKEN_KEY);  
      localStorage.removeItem(USER_KEY);  
    }  
  },  
  getters: {  
    isAuthenticated() {  
      const token = this.accessToken;  
      if (token && !isTokenExpired(token)) {  
        return true;  
      } else {  
        this.clearLocalStorage(); // 토큰이 만료되었거나 없으면 localStorage 초기화  
        return false;  
      }  
    },  
  },  
});  