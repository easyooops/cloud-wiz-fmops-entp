<template>
  <div id="main-menu" class="wsmainfull menu clearfix">
    <div class="wsmainwp clearfix">
      <!-- HEADER BLACK LOGO -->
      <div class="desktoplogo">
        <NuxtLink to="/" class="logo-black"><img src="/assets/images/wiz/logo-pink.png" alt="logo" /></NuxtLink>
      </div>

      <!-- HEADER WHITE LOGO -->
     <div class="desktoplogo col-sm-1">
        <NuxtLink to="/" class="logo-white"><img src="/assets/images/wiz/logo-pink.png" alt="logo" /></NuxtLink>
     </div>

      <!-- ※ PC에서만 해당되는 Noti Bell + Avatar.
      mobile에 대한 Noti Bell + Avatar 컴포넌트는 components/header/logo.vue에 구현 -->
      <div class="wrap-noti-avatar" v-if="isLogin">
        <!--Noti Bell 영역-->
        <span class="noti-bell">
          <v-badge content="2" color="error">
            <v-icon >mdi-bell-outline</v-icon>
          </v-badge>
        </span>
        <!--아바타 영역-->
        <span class="navbar-avatar-pc">
          <HeaderAvatar></HeaderAvatar>
        </span>
      </div>
      <!-- MAIN MENU -->
     <nav :class="['wsmenu', 'clearfix', 'col']">
        <ul class="wsmenu-list nav-theme">
          <!-- Contact Us -->
          <li class="nl-simple reg-fst-link mobile-last-link" aria-haspopup="true" v-if="!isLogin">
            <NuxtLink to="/consulting/contact-us" class="h-link">Contact Us</NuxtLink>
          </li>
          <!-- SIGN IN BUTTON -->
          <li class="nl-simple" aria-haspopup="true">
            <a :href="viteManagementUrl" class="btn r-04 btn--theme hover--tra-white last-link">Sign in</a>
          </li>

        </ul>
      </nav>
      <!-- END MAIN MENU -->
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';
import {useAuthStore} from "~/store/auth";
export default {
  setup() {

    const viteManagementUrl = import.meta.env.VITE_MANAGEMENT_URL

    const state = reactive({
      isOpen: [false, false]
    });
    const toggle = (index) => {
      state.isOpen[index] = !state.isOpen[index];
    };

    const isLogin = ref(useAuthStore().authenticated);
    watch(useAuthStore(), () => {
        isLogin.value = false;
    });

    const profileMenu = [
        { title: 'My Page', Destination: "/preparing"},
        { title: 'Log Out', Destination: "/logout"},
    ];

    return {
      toggle,
      isOpen: state.isOpen,
      isLogin,
      profileMenu,
      viteManagementUrl
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    handleScroll() {
      const menu = document.getElementById("main-menu");
      const header = document.getElementById("header");
      if (window.pageYOffset > 100) {
        menu.classList.add("scroll");
        header.classList.add("scroll");
      } else {
        menu.classList.remove("scroll");
        header.classList.remove("scroll");
      }
    }
  },
};
</script>
<style>
  /* 자식요소(noti bell, avatar 수직 중앙 정렬을 위한 스타일) */
  .wrap-noti-avatar {
      display:table;
      float: right;
      padding: 5px 25px 0px 28px;
  }

  /* pc의 경우과 mobile 사이즈에 대한 avatar, noti bell 배치방식 차이발생 > 별도 Style 적용 */
  .noti-bell {
      padding: 10px 20px 0px 0px;
      display:table-cell;
      vertical-align:middle;
      cursor: pointer;
  }
  .navbar-avatar-pc {
      display:table-cell;
      vertical-align:middle;
  }
</style>
