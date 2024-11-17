<template>
    <div class="wsmobileheader clearfix">
        <span class="smllogo"><img src="/assets/images/wiz/logo-pink.png" alt="mobile-logo" /></span>
        <a id="wsnavtoggle" class="wsanimated-arrow" @click="toggleMobileMenu">
            <span></span>
        </a>

        <!-- ※ Mobile에서만 해당되는 Noti Bell + Avatar.
        PC에 대한 Noti Bell + Avatar 컴포넌트는 components/header/menu.vue에 구현 -->
        <span class="navbar-avatar wrap-noti-avatar" v-if="isLogin">
            <!--Noti Bell 영역-->
            <span class="noti-bell">
                <v-badge content="2" color="error">
                    <v-icon size="x-large">mdi-bell-outline</v-icon>
                </v-badge>
            </span>
            <!--아바타 영역-->
            <HeaderAvatar></HeaderAvatar>
        </span>
    </div>
</template>

<script>
import {useAuthStore} from "~/store/auth";
export default {
    setup() {
        const isLogin = ref(useAuthStore().authenticated);
        watch(useAuthStore(), () => {
            isLogin.value = false;
        });

        return {
            isLogin
        }
    },
    methods: {
        toggleMobileMenu() {
            // toggle body class "dark-mode"
            document.body.classList.toggle("wsactive");
        }
    }
};
</script>
<style>
    /* noti bell 중앙정렬 */
    .wrap-noti-avatar {
        display:table;
    }
    /* Mobile navbar avatar Menu icon (X ICON) */
    .navbar-avatar {
        position: absolute;
        right: 80px;
        top: 0;
        z-index: 102;
        -webkit-transition: all 0.4s ease-in-out;
        -moz-transition: all 0.4s ease-in-out;
        -o-transition: all 0.4s ease-in-out;
        -ms-transition: all 0.4s ease-in-out;
        transition: all 0.4s ease-in-out;
    }
    .navbar-avatar {
        cursor: pointer;
        padding: 10px 35px 16px 0px;
        margin: 7px 0 0 15px;
    }
</style>
