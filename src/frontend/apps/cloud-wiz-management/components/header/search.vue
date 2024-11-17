<template>
  <form class="form-inline search-full col" action="#" method="get" @submit.prevent="" :class="searchOpen ? 'open' : ''">
    <div class="form-group w-100">
      <div class="Typeahead Typeahead--twitterUsers">
        <div class="u-posRelative">
          <input class="demo-input Typeahead-input form-control-plaintext w-100" type="text" v-model="terms"
            placeholder="Search Cuba .." name="q" title="" autofocus />
          <div class="spinner-border Typeahead-spinner" role="status">
            <span class="sr-only">Loading...</span>
          </div>
          <vue-feather class="close-search" type="x" @click="search_close()"></vue-feather>
        </div>
        <div :class="searchResult ? 'Typeahead-menu is-open' : 'Typeahead-menu'" v-if="menuItems.length">
          <div class="ProfileCard u-cf" v-for="(menuItem, index) in menuItems.slice(0, 8)" :key="index">
            <div class="ProfileCard-avatar header-search">

              <svg class="stroke-icon">
                <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
              </svg>
            </div>

            <div class="ProfileCard-details">
              <div class="ProfileCard-realName">
                <span @click="removeFix()">
                  <nuxt-link :to="menuItem.path" class="realname">
                    {{ menuItem.title }}</nuxt-link></span>
              </div>
            </div>
          </div>
        </div>
        <div :class="
          searchResultEmpty ? 'Typeahead-menu is-open' : 'Typeahead-menu'
        ">
          <div class="tt-dataset tt-dataset-0">
            <div class="EmptyMessage">
              Your search turned up 0 results. Opps There are no result found.
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { mapState } from 'pinia';
import { useMenuStore } from '~~/store/menu';

export default {
  name: 'SearchBar',
  data() {
    return {
      terms: '',
      searchResult: false,
      searchResultEmpty: false,
    };
  },
  computed: {
    ...mapState(useMenuStore, {
      menuItems: 'searchData',
      searchOpen: 'searchOpen'
    }),
  },
  watch: {
    terms: {
      handler(value) {
        this.terms ? this.addFix() : this.removeFix();
        useMenuStore().searchTerm(value)
        if (!this.menuItems.length) this.searchResultEmpty = true;
        else this.searchResultEmpty = false;
      }, deep: true
    }
  },
  methods: {
    search_open() {
      useMenuStore().searchOpen = true
    },
    search_close() {
      useMenuStore().searchOpen = false
    },
    searchterm() {
      useMenuStore().searchTerm(this.terms)
    },
    addFix() {
      this.searchResult = true;
    },
    removeFix() {
      this.searchResult = false;
      this.terms = '';
    },
  },
};
</script>
