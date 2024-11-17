<template>
    <div class="tab-pane fade" :class="{ 'active show': customizer == 'settings' }" id="c-pills-home">
      <h6>Layout Type</h6>
      <ul class="main-layout layout-grid">
        <li data-attr="ltr" :class="{ active: layoutType == 'ltr' }" @click="customizeLayoutType('ltr')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-light sidebar"></li>
              <li class="bg-light body">
                <span class="badge badge-primary">LTR</span>
              </li>
            </ul>
          </div>
        </li>
        <li data-attr="rtl" :class="{ active: layoutType == 'rtl' }" @click="customizeLayoutType('rtl')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-light body">
                <span class="badge badge-primary">RTL</span>
              </li>
              <li class="bg-light sidebar"></li>
            </ul>
          </div>
        </li>
        <li v-bind:style="boxlayout ? '' : 'display: none;'" data-attr="box" :class="{ active: layoutType == 'box-layout' }"
          @click="customizeLayoutType('box-layout')" class="box-layout px-3">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-light sidebar"></li>
              <li class="bg-light body">
                <span class="badge badge-primary">Box</span>
              </li>
            </ul>
          </div>
        </li>
      </ul>
      <h6 class="">Sidebar type</h6>
      <ul class="sidebar-type layout-grid">
        <li data-attr="normal-sidebar" @click="customizeSidebarSetting('horizontal-wrapper', 'horizontal')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-dark sidebar"></li>
              <li class="bg-light body"></li>
            </ul>
          </div>
  
        </li>
        <li data-attr="compact-sidebar" :class="{
          active: layout.settings.sidebar_setting == 'compact-sidebar1',
        }" @click="customizeSidebarSetting('compact-wrapper', 'Dubai')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-dark sidebar compact"></li>
              <li class="bg-light body"></li>
            </ul>
  
          </div>
        </li>
  
      </ul>
      <h6 class="">Sidebar Icon</h6>
      <ul class="sidebar-setting layout-grid">
        <li class="active" data-attr="stroke-svg">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body bg-light" @click="customSvg('stroke-svg')">
            <span class="badge badge-primary">Stroke</span>
          </div>
        </li>
        <li data-attr="fill-svg">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body bg-light" @click="customSvg('fill-svg')">
            <span class="badge badge-primary">Fill</span>
          </div>
        </li>
      </ul>
      <h6 class="">Unlimited Color</h6>
      <ul class="layout-grid unlimited-color-layout">
        <input id="ColorPicker1" type="color" value="#7366ff" name="Background" />
        <input id="ColorPicker2" type="color" value="#f73164" name="Background" />
        <button class="color-apply-btn btn btn-primary color-apply-btn" @click.prevent="customizeColor">
          Apply
        </button>
  
      </ul>
      <h6 class="">Mix Layout</h6>
      <ul class="layout-grid customizer-mix">
        <li class="color-layout" data-attr="light-only" :class="{ active: mixLayout == 'light-only' }"
          @click="customizeMixLayout('light-only')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-light sidebar"></li>
              <li class="bg-light body"></li>
            </ul>
          </div>
        </li>
        <li class="color-layout" data-attr="dark-sidebar" :class="{ active: mixLayout == 'dark-sidebar' }"
          @click="customizeMixLayout('dark-sidebar')">
          <div class="header bg-light">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-dark sidebar"></li>
              <li class="bg-light body"></li>
            </ul>
          </div>
        </li>
        <li class="color-layout" data-attr="dark-only" :class="{ active: mixLayout == 'dark-only' }"
          @click="customizeMixLayout('dark-only')">
          <div class="header bg-dark">
            <ul>
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
          <div class="body">
            <ul>
              <li class="bg-dark sidebar"></li>
              <li class="bg-dark body"></li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </template>
  <script>
  import { mapState } from 'pinia';
  import { useLayoutStore } from '~~/store/layout';
  import { layoutClasses } from '../../constants/layout';
  import { useMenuStore } from '~~/store/menu';
  export default {
    name: 'CustomSetting',
    data() {
      return {
        layoutType: 'ltr',
        mixLayout: 'default',
      };
    },
    computed: {
      ...mapState(useMenuStore, {
        customizer: 'customizer',
  
      }),
      ...mapState(useLayoutStore, {
  
        layout: 'layout',
  
      }),
      boxlayout() {
        return useLayoutStore().boxlayout
      },
      data() {
        return JSON.stringify(useLayoutStore().layout)
      },
    },
    methods: {
      customizeLayoutType(val) {
        useLayoutStore().setLayoutType({ class: val, val: true })
        this.layoutType = val;
      },
      customizeSidebarSetting(val, layout) {
        const layoutobj = layoutClasses.find((item) => Object.keys(item).pop() === layout);
        useLayoutStore().setCustomizeSidebarType(layoutobj[layout])
        this.layout.settings.layout = layout;
        this.$router.push({ query: { layout: layout } }).catch(err => err);
      },
      customizeColor() {
        const primary = document.getElementById('ColorPicker1').value;
        const secondary = document.getElementById('ColorPicker2').value;
        useLayoutStore().setColorScheme({ primary, secondary })
      },
      customizeMixLayout(val) {
        this.mixLayout = val;
        useLayoutStore().setLayout({ class: val })
      },
      customSvg(val) {
        useLayoutStore().setSvg(val)
      }
    },
  };
  </script>