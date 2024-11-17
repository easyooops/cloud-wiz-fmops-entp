import { defineStore } from "pinia";

export const useTeamStore = defineStore("team", () => {
    const userInfo = ref([]);

    const getUserInfo = computed(() => userInfo);
    function setUserInfo(param) {
        this.userInfo = param
    }

    return { userInfo, getUserInfo, setUserInfo };
});
