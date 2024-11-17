import { useAuthStore } from '@/store/auth';

export default defineNuxtRouteMiddleware((to, from) => {
    const authStore = useAuthStore();

    const publicPaths = ['/login'];

    if ((!authStore.isAuthenticated && (to.path === '/' || to.path === '')) || 
        (!authStore.isAuthenticated && !publicPaths.includes(to.path))) {
      return navigateTo('/login');
    }
});