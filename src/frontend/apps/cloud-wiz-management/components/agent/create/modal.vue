<template>
  <div class="customizer-header">
    <Teleport to="body">
      <div class="modal fade modal-bookmark" id="agent-modal" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-md" role="document">
          <div class="modal-content">
            <header id="modal-customizer___BV_modal_header_" class="modal-header">
              <h5 id="modal-customizer___BV_modal_title_" class="modal-title">Agent CURL</h5><button type="button"
                aria-label="Close" data-bs-dismiss="modal" class="close">×</button>
            </header>
            <div class="modal-body">
              <div class="config-popup">
                <p>
                  Please use URI encoding for the value of the query argument.
                </p>
                <div><pre class="curl-code">{{ curlCommand }}</pre></div>
                <button class="btn btn-primary mt-2" @click="copyText()">
                  Copy
                </button>
              </div>
            </div>
            <footer id="modal-customizer___BV_modal_footer_" class="modal-footer">
              <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button> -->
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button></footer>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
  
<script>
  import { mapState } from 'pinia';
  import { useLayoutStore } from '~~/store/layout';
  import { useAgentStore } from '@/store/agent';
  import { useToast } from 'vue-toastification';

  export default {
    name: 'CURL',
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
      ...mapState(useLayoutStore, {
        layout: 'layout'
      }),
      curlCommand() {
        const agentId = this.agentId;
        return this.removeLeadingWhitespace(
          `curl ${import.meta.env.VITE_API_ENDPOINT}/api/v1/agent/prompt/${agentId}?query=What%20is%20fmops%3F \\` +
          `\n-X 'GET' \\` +
          `\n-H 'accept: application/json'`
        );


      },
      agentId() {
        const agentStore = useAgentStore();
        return agentStore.agent ? agentStore.agent.agent_id : '';
      }      
    },
    methods: {
      removeLeadingWhitespace(str) {
        return str.replace(/^\s+/gm, '');
      },
      async copyText() {
        const text = this.curlCommand;
        navigator.clipboard.writeText(text).then(() => {
          this.toast.success('Code Copied to clipboard');
        }).catch(() => {
          this.toast.error('Failed to copy text');
        });
      },
    },
    setup() {
      const toast = useToast();
      return { toast };
    },    
  };
</script>
  
<style scoped>
.modal {
  --bs-modal-width: 900px;
}
.curl-code {
  white-space: pre-wrap;
}
</style>