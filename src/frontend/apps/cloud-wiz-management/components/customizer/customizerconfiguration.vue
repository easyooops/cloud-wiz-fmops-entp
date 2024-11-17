<template>
    <div class="customizer-header">
      <i class="icofont-close icon-close" @click="closecustomizer()"></i>
      <h5>Preview Settings</h5>
      <p class="mb-0">
        Try It Real Time <i class="fa fa-thumbs-o-up txt-primary"></i>
      </p>
      <button data-bs-toggle="modal" data-bs-target="#modal-customizer" class="btn btn-primary plus-popup mt-2">
        Configuration
      </button>
      <Teleport to="body">
        <div class="modal fade modal-bookmark" id="modal-customizer" tabindex="-1" role="dialog"
          aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-md" role="document">
            <div class="modal-content">
              <header id="modal-customizer___BV_modal_header_" class="modal-header">
                <h5 id="modal-customizer___BV_modal_title_" class="modal-title">Modal Title</h5><button type="button"
                  aria-label="Close" data-bs-dismiss="modal" class="close">×</button>
              </header>
              <div class="modal-header modal-copy-header">
                <h5 class="headerTitle mb-0">Customizer configuration</h5>
              </div>
              <div class="modal-body">
                <div class="config-popup">
                  <p>
                    To replace our design with your desired theme. Please do
                    configuration as mention
                  </p>
                  <p>
                    <b>Path : src > data > layout.json</b>
                  </p>
                  <div>
                    <pre>
                              <code>
                                <textarea :value="data" ref="layout" rows="1" v-bind:style="styleObject"/>
                                {{ layout }}
                              </code>
                            </pre>
                  </div>
                  <button class="btn btn-primary mt-2" @click="copyText()">
                    Copy Json
                  </button>
                </div>
              </div>
              <footer id="modal-customizer___BV_modal_footer_" class="modal-footer"><button type="button"
                  class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button><button type="button"
                  class="btn btn-primary" data-bs-dismiss="modal">OK</button></footer>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </template>
  
  <script>
  import { mapState } from 'pinia';
  import { useLayoutStore } from '~~/store/layout';
  import { useMenuStore } from '~~/store/menu';
  
  export default {
    name: 'CustomizerConfiguration',
    data() {
      return {
        styleObject: {
          position: 'fixed',
          left: '0',
          top: '0',
          opacity: '0',
        },
      };
    },
    computed: {
      ...mapState(useMenuStore, {
        customizer: 'customizer',
      }),
      ...mapState(useLayoutStore, {
  
        layout: 'layout',
      }),
      data() {
        return JSON.stringify(useLayoutStore().layout)
      }
    },
    methods: {
      closecustomizer() {
        useMenuStore().customizer = ''
      },
      copyText() {
        this.$refs.layout.select();
        document.execCommand('copy');
        this.$toasted.show('Code Copied to clipboard', {
          theme: 'outline',
          position: 'top-right',
          type: 'default',
          duration: 2000,
        });
      },
    },
  };
  </script>