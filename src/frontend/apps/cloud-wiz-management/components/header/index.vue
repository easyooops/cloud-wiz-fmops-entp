<template>
  <div class="header-wrapper row m-0">
    <SearchBar />
    <Logo />
    <!-- <div class="left-header col-xxl-5 col-xl-6 col-lg-5 col-md-4 col-sm-3 p-0">
      <swiper :slidesPerView="1" :autoplay="{
        delay: 2500,
        disableOnInteraction: false,
      }" :modules="modules" class="notification-slider" direction="vertical">
        <swiper-slide class="h-100">
          <div class="d-flex h-100">
            <img src="/images/giftools.gif" alt="gif">
            <h6 class="mb-0 f-w-400">
              <span class="font-primary">Don't Miss Out! </span><span class="f-light">Out new update has been
                release.</span>
            </h6><i class="icon-arrow-top-right f-light"></i>
          </div>
        </swiper-slide>
        <swiper-slide class="h-100">
          <div class="d-flex h-100">
            <img src="/images/giftools.gif" alt="gif">
            <h6 class="mb-0 f-w-400">
              <span class="f-light">Something you love is now on sale! </span>
            </h6><a class="ms-1" href="https://1.envato.market/3GVzd" target="_blank">Buy now !</a>
          </div>
        </swiper-slide>
      </swiper>
    </div> -->
    <div class="nav-right col-xxl-7 col-xl-6 col-md-7 col-8 pull-right right-header p-0 ms-auto">
      <ul class="nav-menus">
        <!-- <li class="language-nav">
          <Language />
        </li>
        <li>
          <span class="header-search"><svg @click="search_open()">
              <use href="@/assets/svg/icon-sprite.svg#search"></use>
            </svg>
          </span>
        </li>

        <li class="onhover-dropdown">
          <svg @click="bookmark_open()">
            <use href="@/assets/svg/icon-sprite.svg#star"></use>
          </svg>
          <Bookmark v-bind:activeclass="bookmark" />
        </li>
        <li>
          <Mode />
        </li>
        <Cart /> -->
        <!-- <Notifications /> -->
        <Profile />
      </ul>
    </div>
  </div>
</template>
<script>
import { mapState } from 'pinia';
import Bookmark from '../bookmark';
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay } from "swiper/modules";
import "swiper/css";
import Language from './language.vue';
import Notifications from './notifications.vue';
import Mode from './mode';
import Cart from './cart';
import Profile from './profile';
import Logo from './logo.vue';
import SearchBar from './search';
import { useMenuStore } from '~~/store/menu';

export default {
  components: {
    Bookmark,
    Language,
    Notifications,
    Mode,
    Cart,
    Profile,
    Logo,
    Swiper,
    SwiperSlide,
    SearchBar,
  },
  data() {
    return {
      bookmark: false,
    };
  },
  computed: {
    ...mapState(useMenuStore, {
      menuItems: 'searchData',
      megamenuItems: 'megamenu',
      searchOpen: 'searchOpen',
    }),
  },
  methods: {
    search_open() {
      useMenuStore().searchOpen = true
    },
    bookmark_open() {
      this.bookmark = !this.bookmark;
    },
  },
  setup() {
    return {
      modules: [Autoplay],
    };
  },
};
</script>
