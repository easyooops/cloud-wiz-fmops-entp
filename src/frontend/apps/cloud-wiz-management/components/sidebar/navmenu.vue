<template>
  <div id="sidebar-menu">

    <ul class="sidebar-links custom-scrollbar" id="myDIV"
      :style="[layoutobject.split(' ').includes('horizontal-wrapper') ? layout.settings.layout_type == 'rtl' ? { 'margin-right': margin + 'px' } : { 'margin-left': margin + 'px' } : { margin: '0px' }]">
      <li class="back-btn">
        <router-link to="/">
          <img class="img-fluid" src="/images/logo/logo-icon.png" alt="" /></router-link>
        <div class="mobile-back text-end">
          <span>Back</span><i class="fa fa-angle-right ps-2" aria-hidden="true"></i>
        </div>
      </li>
      <li class="pin-title sidebar-main-title " :class="showPinTitle ? 'show' : ''">
        <div>
          <h6>Pinned</h6>
        </div>
      </li>
      <li v-for="(menuItem, index) in menuItems" :key="index" class="sidebar-list"
        :class="{ 'sidebar-main-title': menuItem.type == 'headtitle', 'hoverd': menuItem.active == true && this.layoutobject.split(' ').includes('horizontal-wrapper') }, menuItem.showPin ? 'pined' : ''">

        <div v-if="menuItem.type == 'headtitle'">
          <h6 class="lan-1">{{ $t(menuItem.headTitle1) }}</h6>

        </div>

        <i v-if="menuItem.type != 'headtitle'" class="fa fa-thumb-tack" @click="togglePinnedName({ item: menuItem })"></i>
        <label :class="'badge badge-' + menuItem.badgeType" v-if="menuItem.badgeType">{{ (menuItem.badgeValue) }}</label>
        <a href="javascript:void(0)" class="sidebar-link sidebar-title" :class="{ 'active': menuItem.active }"
          v-if="menuItem.type == 'sub'" @click="setNavActive(menuItem, index)"
          @mouseover="setNavActiveh(menuItem, index)">
          <svg class="stroke-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
          </svg>
          <svg class="fill-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.iconf}`"></use>
          </svg>

          <span class="lan-3">
            {{ $t(menuItem.title) }}
          </span>
          <div class="according-menu" v-if="menuItem.children">
            <i class="fa fa-angle-right pull-right"></i>
          </div>
        </a>

        <router-link :to="menuItem.path" class="sidebar-link sidebar-title" v-if="menuItem.type == 'link'"
          :class="{ 'active': menuItem.active }" v-on:click="hidesecondmenu()" @click="setNavActive(menuItem, index)"
          @mouseover="setNavActiveh(menuItem, index)">
          <svg class="stroke-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
          </svg>
          <svg class="fill-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.iconf}`"></use>
          </svg>

          <span>
            {{ $t(menuItem.title) }}
          </span>
          <i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
        </router-link>

        <a :href="menuItem.path" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extLink'"
          @click="setNavActive(menuItem, index)">
          <svg class="stroke-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
          </svg>
          <svg class="fill-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.iconf}`"></use>
          </svg>

          <span>
            {{ $t(menuItem.title) }}
          </span>
          <i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
        </a>

        <a :href="menuItem.path" target="_blank" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extTabLink'"
          @click="setNavActive(menuItem, index)">

          <svg class="stroke-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
          </svg>
          <svg class="fill-icon">
            <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.iconf}`"></use>
          </svg>
          <span>
            {{ $t(menuItem.title) }}
          </span>
          <i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
        </a>


        <ul class="sidebar-submenu" v-if="menuItem.children" :class="{ 'menu-open': menuItem.active }"
          :style="{ display: menuItem.active ? 'block' : 'none' }">
          <li v-for="(childrenItem, index) in menuItem.children" :key="index">

            <a class="lan-4" :class="{ 'active': childrenItem.active }" href="javascript:void(0)"
              v-if="childrenItem.type == 'sub'" @click="setNavActive(childrenItem, index)">
              {{ $t(childrenItem.title) }}
              <label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
                childrenItem.badgeValue }}</label>
              <i class="fa pull-right mt-1"
                v-bind:class="[childrenItem.active ? 'fa fa-angle-down' : 'fa fa-angle-right']"
                v-if="childrenItem.children"></i>
            </a>

            <router-link class="lan-4" :class="{ 'active': childrenItem.active }" :to="childrenItem.path"
              v-if="childrenItem.type == 'link'" @click="setNavActive(childrenItem, index)" v-on:click="hidesecondmenu()">
              {{ $t(childrenItem.title) }}
              <label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
                (childrenItem.badgeValue) }}</label>
              <i class="fa fa-angle-right pull-right mt-1" v-if="childrenItem.children"></i>
            </router-link>

            <a :href="childrenItem.path" v-if="childrenItem.type == 'extLink'" class="submenu-title">
              {{ (childrenItem.title) }}
              <label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
                $t(childrenItem.badgeValue) }}</label>
              <i class="fa fa-angle-right pull-right mt-1" v-if="childrenItem.children"></i>
            </a>

            <a class="submenu-title" :href="childrenItem.path" target="_blank" v-if="childrenItem.type == 'extTabLink'">
              {{ $t(childrenItem.title) }}
              <label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
                (childrenItem.badgeValue) }}</label>
              <i class="fa fa-angle-right pull-right mt-1" v-if="childrenItem.children"></i>
            </a>

            <ul class="nav-sub-childmenu submenu-content" v-if="childrenItem.children"
              :class="{ 'opensubchild': childrenItem.active }">
              <li v-for="(childrenSubItem, index) in childrenItem.children" :key="index">

                <router-link :class="{ 'active': childrenSubItem.active }" :to="childrenSubItem.path"
                  v-if="childrenSubItem.type == 'link'" router-link-exact-active exact v-on:click="hidesecondmenu()"
                  @click="setNavActive(childrenSubItem, index)">
                  {{ $t(childrenSubItem.title) }}
                  <label :class="'badge badge-' + childrenSubItem.badgeType + ' pull-right'"
                    v-if="childrenSubItem.badgeType">{{ (childrenSubItem.badgeValue) }}</label>
                  <i class="fa fa-angle-right pull-right" v-if="childrenSubItem.children"></i>
                </router-link>

                <router-link :to="childrenSubItem.path" v-if="childrenSubItem.type == 'extLink'" router-link-exact-active>
                  {{ $t(childrenSubItem.title) }}
                  <label :class="'badge badge-' + childrenSubItem.badgeType + ' pull-right'"
                    v-if="childrenSubItem.badgeType">{{ (childrenSubItem.badgeValue) }}</label>
                  <i class="fa fa-angle-right pull-right" v-if="childrenSubItem.children"></i>
                </router-link>

                <router-link :to="childrenSubItem.path" v-if="childrenSubItem.type == 'extLink'" router-link-exact-active>
                  {{ $t(childrenSubItem.title) }}
                  <label :class="'badge badge-' + childrenSubItem.badgeType + ' pull-right'"
                    v-if="childrenSubItem.badgeType">{{ (childrenSubItem.badgeValue) }}</label>
                  <i class="fa fa-angle-right pull-right" v-if="childrenSubItem.children"></i>
                </router-link>
              </li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
<script>
import { mapState } from 'pinia';
import { useLayoutStore } from '~~/store/layout';
import { useMenuStore } from '~~/store/menu';
import { layoutClasses } from '../../constants/layout';
import { useWindowScroll } from '@vueuse/core'
import { useWindowSize, useLocalStorage } from '@vueuse/core'
export default {
  name: 'Navmenu',
  data() {
    return {
      layoutobj: {},
      scrolled: useWindowScroll().x,
      rolled: useWindowScroll().y,
      windowWidt: useWindowSize().width
    };
  },
  computed: {
    ...mapState(useMenuStore, {
      menuItems: 'data',
      activeoverlay: 'activeoverlay',
      togglesidebar: 'togglesidebar',
      width: 'width',
      height: 'height',
      margin: 'margin',
      menuWidth: 'menuWidth',

    }),
    showPinTitle: {
      get() {
        let show = false;
        this.menuItems.every(item => {
          item.showPin && (show = true)
          return !show
        })
        return show
      }
    },
    ...mapState(useLayoutStore, {
      layout: 'layout',
      sidebar: 'sidebarType',
    }),
    layoutobject: {
      get: function () {
        return JSON.parse(JSON.stringify(layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout)))[this.layout.settings.layout];
      },
      set: function () {
        this.layoutobj = layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout);
        this.layoutobj = JSON.parse(JSON.stringify(this.layoutobj))[this.layout.settings.layout];
        return this.layoutobj;
      }
    }
  },
  watch: {
    scrolled() {
      this.handleResize()
    },
    rolled() {
      this.handleScroll()
    },
    width() {
      this.handleResize();
      this.handleScroll();
      if (useWindowScroll().x < 992) {
        const newlayout = JSON.parse(JSON.stringify(this.layoutobject).replace('horizontal-wrapper', 'compact-wrapper'));
        document.querySelector('.page-wrapper').className = 'page-wrapper ' + newlayout;
        useMenuStore().margin = 0;
      } else {
        document.querySelector('.page-wrapper').className = 'page-wrapper ' + this.layoutobject;
      }

      if ((useWindowScroll().x < 1199 && this.layout.settings.layout === 'Tokyo') || (useWindowScroll().x < 1199 && this.layout.settings.layout === 'Moscow') || (useWindowScroll().x < 1199 && this.layout.settings.layout === 'Rome')) {
        this.menuItems.filter(menuItem => {
          menuItem.active = false;
        });
      }
    }
  },
  created() {
    this.handleResize();
    if (useMenuStore().width < 991) {
      this.layout.settings.layout = 'Dubai';
      this.margin = 0;
    }
    setTimeout(() => {
      const elmnt = document.getElementById('myDIV');
      useMenuStore().menuWidth = elmnt.offsetWidth;
      useMenuStore().menuWidth > useWindowScroll().x ?
        (useMenuStore().hideRightArrow = false, useMenuStore().hideLeftArrowRTL = false) :
        (useMenuStore().hideRightArrow = false, useMenuStore().hideLeftArrowRTL = true);
    }, 500);
    this.layoutobject = layoutClasses.find((item) => Object.keys(item).pop() === this.layout.settings.layout);
    this.layoutobject = JSON.parse(JSON.stringify(this.layoutobject))[this.layout.settings.layout];
  },

  mounted() {
    window.addEventListener('unload', this.HandleUnload)
    let LocalPins = JSON.parse(localStorage.getItem('pins') || '[]')
    LocalPins.forEach(pin => {
      let pinIndex = this.menuItems.findIndex(menu => menu.title == pin);
      pinIndex > -1 && (this.menuItems[pinIndex].showPin = true)
    })
    this.menuItems.filter(items => {
      if (items.path === this.$route.path)
        useMenuStore().setActiveRoute(items)
      if (!items.children) return false;
      items.children.filter(subItems => {
        if (subItems.path === this.$route.path)
          useMenuStore().setActiveRoute(subItems)

        if (!subItems.children) return false;
        subItems.children.filter(subSubItems => {
          if (subSubItems.path === this.$route.path)
            useMenuStore().setActiveRoute(subSubItems)

        });
      });
    });
  },
  methods: {
    HandleUnload() {
      let pinsArray = [];
      this.menuItems.forEach(item => {
        item.showPin && pinsArray.push(item.title);
      })
      localStorage.setItem('pins', JSON.stringify(pinsArray))
    },
    handleScroll() {
      if (process.client) {
        if (useWindowScroll().y > 400) {
          if (this.layoutobject.split(' ').pop() === 'material-type' || this.layoutobject.split(' ').pop() === 'advance-layout')
            document.querySelector('.sidebar-main').className = 'sidebar-main hovered';
        } else {
          if (document.getElementById('sidebar-main'))
            document.querySelector('.sidebar-main').className = 'sidebar-main';
        }
      }
    },
    togglePinnedName({ item }) {
      item.showPin = !item.showPin
      if (this.menuItems.length > 0) {
        this.menuItems = 'show'
      } else {
        this.menuItems = ''
      }
    },
    setNavActive(item) {
      useMenuStore().setNavActive(item)
      if (this.layoutobject.split(' ').includes('compact-sidebar') && useWindowScroll().x > 991) {
        if (this.menuItems.some(menuItem => menuItem.active === true)) {
          useMenuStore().activeoverlay = true;
        } else {
          useMenuStore().activeoverlay = false;
        }
      }
    },
    setNavActiveh(item) {
      if (this.layoutobject.split(' ').includes('horizontal-wrapper')) {
        useMenuStore().setNavActive(item)
        if (this.layoutobject.split(' ').includes('compact-sidebar') && window.innerWidth > 991) {
          if (this.menuItems.some(menuItem => menuItem.active === true)) {
            this.$store.state.menu.activeoverlay = true;
          } else {
            this.$store.state.menu.activeoverlay = false;
          }
        }
      }

    },
    hidesecondmenu() {
      if (useWindowScroll().x < 991) {
        useMenuStore().activeoverlay = false,
          useMenuStore().togglesidebar = false;
        this.menuItems.filter(menuItem => {
          menuItem.active = false;
        });
      } else if (this.layoutobject.split(' ').includes('compact-sidebar')) {
        useMenuStore().activeoverlay = false,
          this.menuItems.filter(menuItem => {
            menuItem.active = false;
          });
      }
    },
    handleResize() {
      useMenuStore().width = this.windowWidt - 450;
    },
  }
};
</script>
