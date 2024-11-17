<template>
  <div>
    <div class="onhover-show-div bookmark-flip" :class="bookmarkSearchBox || activeclass ? 'active' : ''">
      <div class="flip-card">
        <div class="flip-card-inner" :class="bookmarkSearchBox ? 'flipped' : ''">
          <div class="front">
            <h6 class="f-18 mb-0 dropdown-title">Bookmark</h6>
            <ul class="droplet-dropdown bookmark-dropdown">
              <li class="custom-scrollbar">
                <div class="row">
                  <div class="col-4 text-center" v-for="(items, index) in bookmarkItems.slice(0, 8)" :key="index">
                    <div class="bookmark-content">
                      <div class="bookmark-icon">
                        <svg class="stroke-icon">
                          <use :xlink:href="('/svg/icon-sprite.svg') + `#${items.icon}`"></use>
                        </svg>

                      </div>
                      <span>{{ items.title }}</span>
                    </div>
                  </div>
                </div>
              </li>
              <li class="text-center">
                <a href="javascript:void(0)" class="flip-btn f-w-700" id="flip-btn" @click="openbookmark">
                  Add New Bookmark
                </a>
              </li>
            </ul>
          </div>
          <div class="back">
            <ul>
              <li>
                <div class="bookmark-dropdown flip-back-content">
                  <input type="text" placeholder="search..." v-model="terms" />
                  <div class="bookmark-search custom-scrollbar" :class="
                    searchMenuItems.length
                      ? 'Typeahead-menu is-open'
                      : 'Typeahead-menu'
                  ">
                    <div class="ProfileCard u-cf" v-for="(menuItem, index) in searchMenuItems.slice(0, 8)" :key="index">
                      <div class="ProfileCard-avatar header-search">
                        <svg class="stroke-icon">
                          <use :xlink:href="('/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
                        </svg>

                      </div>
                      <div class="ProfileCard-details">
                        <div class="ProfileCard-realName">
                          <span @click="removeFix()">
                            <router-link :to="{ path: menuItem.path }" class="realname">{{ menuItem.title }}</router-link>
                          </span>
                          <a href="JavaScript:void(0);" @click="addToBookmark(menuItem)">
                            <span><i class="fa fa-star-o f-18 bookmark-search f-right"
                                :class="menuItem.bookmark ? 'text-warning' : ''"></i></span></a>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div :class="
                    bookmarkSearchResultEmpty
                      ? 'Typeahead-menu is-open'
                      : 'Typeahead-menu'
                  ">
                    <div class="tt-dataset tt-dataset-0">
                      <div class="EmptyMessage">
                        Your search turned up 0 results. Opps There are no result
                        found.
                      </div>
                    </div>
                  </div>
                </div>
              </li>
              <li>
                <a href="javascript:void(0)" class="d-block flip-back f-w-700" id="flip-back" @click="openbookmark">
                  Back
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState } from 'pinia';
import { useMenuStore } from '~~/store/menu';

export default {
  props: ['activeclass'],
  data() {
    return {
      terms: '',
      bookmarkSearchBox: false,
      bookmarkSearchResult: false,
      bookmarkSearchResultEmpty: false,
      bookmarkItems: [],
    };
  },
  computed: {
    ...mapState(useMenuStore, {
      menuItems: 'data',
      searchMenuItems: 'searchData',
    }),
  },
  watch: {
    terms: {
      handler(value) {

        this.terms ? this.addFix() : this.removeFix();
        if (!this.searchMenuItems.length) this.bookmarkSearchResultEmpty = true;
        else this.bookmarkSearchResultEmpty = false;
        this.addFix();
        useMenuStore().searchTerm(value)
      }
    },
  },
  mounted() {
    this.menuItems.filter((items) => {
      if (items.bookmark) {
        this.bookmarkItems.push(items);
      }
    });
  },
  methods: {
    openbookmark() {
      this.bookmarkSearchBox = !this.bookmarkSearchBox;
      if (!this.bookmarkSearchBox) this.removeFix();
    },
    searchTerm: function () {
      this.addFix();
      useMenuStore().searchTerm(this.terms)
    },
    addFix() {
      this.bookmarkSearchResult = true;
    },
    removeFix() {
      this.bookmarkSearchResult = false;
      this.text = '';
    },
    addToBookmark(items) {
      const index = this.bookmarkItems.indexOf(items);
      if (index === -1 && !items.bookmark) {
        items.bookmark = true;
        this.bookmarkItems.push(items);
        this.text = '';
      } else {
        this.bookmarkItems.splice(index, 1);
        items.bookmark = false;
      }
    },
  },
};
</script>
