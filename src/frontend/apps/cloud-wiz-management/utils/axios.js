import axios from 'axios';
import { useAuthStore } from '@/store/auth';

const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT + '/api/v1';

const axiosInstance = axios.create({
  baseURL: API_ENDPOINT,
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      navigateTo('/login');
    }
    return Promise.reject(error);
  }
);

const useFetch = async (url, options) => {
  try {
    const response = await axiosInstance({
      url,
      method: options.method,
      headers: options.headers,
      data: options.body,
    });
    return response;
  } catch (error) {
    throw error;
  }
};

const restApi = () => {

  const authStore = useAuthStore();

  const get = async (url) => {
    return await useFetch(`${API_ENDPOINT}${url}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    });
  };

  const post = async (url, body) => {
    return await useFetch(`${API_ENDPOINT}${url}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      },
      body: JSON.stringify(body)
    });
  };

  const put = async (url, body) => {
    return await useFetch(`${API_ENDPOINT}${url}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      },
      body: JSON.stringify(body)
    });
  };

  const del = async (url) => {
    return await useFetch(`${API_ENDPOINT}${url}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      },
    });
  };

  return { get, post, put, del };
};

export default restApi;
