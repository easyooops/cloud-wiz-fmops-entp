<template>
  <div class="translate_wrapper " :class="{ 'active': isActive }">
    <div class="current_lang">
      <div class="lang"><i class="flag-icon" :class="langIcon" @click="display()"></i><span class="lang-txt">{{
        langLangauge }}</span></div>
    </div>

    <div class="more_lang" :class="{ 'active': isActive }">

      <div class="lang" v-for="locale in availableLocales" :key="locale.code">
        <nuxt-link :to="switchLocalePath(locale.code)"> <i class="flag-icon" :class="locale.icon"></i><span
            class="lang-txt" @click="changeLocale(locale)">{{ locale.name }}<span>{{ locale.short }}
            </span></span></nuxt-link>
      </div>

    </div>
    <!-- <pre>{{ availableLocales }}</pre> -->

  </div>
 
</template>
<script>
import { useLanguageStore } from '~~/store/language';
export default {
  name: 'languagePage',
  data() {
    return {
      isActive: false,

    };
  },
  methods: {
    display() {
      this.isActive = !this.isActive
    },


    changeLocale(locale) {
      useLanguageStore().changeLang(locale)
      this.$i18n.locale = locale;

    },
  },
  computed: {
    langIcon() {
      return useLanguageStore().langIcon1
    },
    langLangauge() {
      return useLanguageStore().langLangauge1
    }

  },
  mounted() {
    useLanguageStore().changeLang({ code: localStorage.getItem('currentLanguage') || 'EN', icon: localStorage.getItem('currentLanguageIcon') || 'flag-icon-us' })
  },
  setup() {
    const { locale, locales } = useI18n();
    const switchLocalePath = useSwitchLocalePath()
    const availableLocales = computed(() => {
      return (locales.value).filter(i => i.code !== locale.value)
     
    })
    return {
      switchLocalePath, availableLocales
    }
  }
}
</script>
