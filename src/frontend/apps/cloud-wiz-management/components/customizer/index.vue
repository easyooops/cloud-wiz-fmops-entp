<template>
    <div>
      <div class="customizer-links" :class="{ open: customizer }">
        <div class="nav flex-column nac-pills" id="c-pills-tab">
          <CustomizerTool />
          <CustomizerSetting />
          <Support />
          <Document />
          <CheckFeatures />
          <BuyNow />
        </div>
      </div>
      <div class="customizer-contain" :class="{ open: customizer }">
        <div class="tab-content">
          <CustomizerConfiguration />
          <div class="customizer-body custom-scrollbar">
            <Customlayout />
            <CustomSetting />
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
    import { mapState } from 'pinia';
    import BuyNow from './buynow';
    import CheckFeatures from './checkfeatures';
    import Document from './document';
    import Support from './support';
    import CustomizerTool from './customizertool';
    import CustomizerSetting from './customizersetting';
    import CustomizerConfiguration from './customizerconfiguration';
    import Customlayout from './customlayout';
    import CustomSetting from './customsetting';
  import { useMenuStore } from '~~/store/menu';
    
  
    export default {
      name: 'customizer',
      components : {
        BuyNow,
        CheckFeatures,
        Document,
        Support,
        CustomizerTool,
        CustomizerSetting,
        CustomizerConfiguration,
        Customlayout,
        CustomSetting
      },
      computed: {
        ...mapState(useMenuStore,{
          customizer: 'customizer',
        }),
      },
    };
  </script>