import Toast, { POSITION, useToast } from "vue-toastification";
import "vue-toastification/dist/index.css";
import PerfectScrollbar from "vue3-perfect-scrollbar";
import "vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css";
import vue3StarRatings from "vue3-star-ratings";
import DropZone from "dropzone-vue";
import Vue3Tour from "vue3-tour";
import "vue3-tour/dist/vue3-tour.css";
import VueApexCharts from "@/components/apexcharts.vue";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/antd.css";
import Lightbox from "vue-easy-lightbox";
import VueSweetalert2 from "vue-sweetalert2";
import "sweetalert2/dist/sweetalert2.min.css";
import VueAnimateOnScroll from "vue3-animate-onscroll";
import { list } from "@/data/draggable";
const toast = useToast();
import { Popover } from "bootstrap/dist/js/bootstrap.esm.min.js";
import { Tooltip } from "bootstrap/dist/js/bootstrap.esm.min.js";
import AosVue from "aos-vue";
import CKEditor from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
// import  {quillEditor}  from "vue3-quill";
import VueNumber from "vue-number-animation";
import SimpleTypeahead from "vue3-simple-typeahead";
import "vue3-simple-typeahead/dist/vue3-simple-typeahead.css";
import Vue3EasyDataTable from "vue3-easy-data-table";
import "vue3-easy-data-table/dist/style.css";
import "bootstrap/js/dist/dropdown.js";
// import Chartist from 'vue-chartist'
// var chartist=
// import '../node_modules/vue-chartist/index'
// const vueChartist =
//import { createI18n } from "vue-i18n";
import { createPinia } from 'pinia'
export default defineNuxtPlugin((nuxtApp) => {
    // nuxtApp.vueApp.component('quill-editor',quillEditor)
    nuxtApp.vueApp.component("EasyDataTable", Vue3EasyDataTable);
    nuxtApp.vueApp.use(SimpleTypeahead);
    nuxtApp.vueApp.use(VueNumber);
    nuxtApp.vueApp.use(AosVue);
    nuxtApp.vueApp.component("apexchart", VueApexCharts);
    nuxtApp.vueApp.use(PerfectScrollbar);
    nuxtApp.vueApp.use(Toast);
    nuxtApp.vueApp.component("vue3-star-ratings", vue3StarRatings);
    nuxtApp.provide("showToast", (params) =>
        toast[params.type || "sucsess"](params.msg || "default", {
            timeout: params.time || 2000,
            position: params.position || "top-right",
            icon: params.icon,
        })
    );
    nuxtApp.vueApp.use(DropZone);
    nuxtApp.vueApp.use(Vue3Tour);
    // const i18n = createI18n({
    //     locale: locale,
    //     fallbackLocale: 'en',
    //     messages,
    //     silentTranslationWarn: true
    //   });
    // nuxtApp.vueApp.use(i18n)
    // nuxtApp.vueApp.use(require(vue-chartist));
    nuxtApp.vueApp.config;
    nuxtApp.vueApp.use(Lightbox);
    nuxtApp.vueApp.use(VueSweetalert2);
    nuxtApp.vueApp.component("VueSlider", VueSlider);
    nuxtApp.vueApp.use(VueAnimateOnScroll);
    nuxtApp.vueApp.provide("list", list);
    nuxtApp.vueApp.provide("Popover", Popover);
    nuxtApp.vueApp.provide("Tooltip", Tooltip);
    nuxtApp.vueApp.provide("ClassicEditor", ClassicEditor);

    nuxtApp.vueApp.component("ckeditor", CKEditor.component);
});


