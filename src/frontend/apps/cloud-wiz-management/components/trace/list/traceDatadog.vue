<template>
  <div>
    <div class="container-fluid">
      <div class="row widget-grid">
        <div class="col-sm-12">
          <div class="card">
            <div class="card-body">

              <!-- Loading Indicator -->
              <div class="loader-box" v-if="loading">
                <div class="loader-30"></div>
              </div>

              <div class="iframe-container">
                <iframe
                    :src="dashboardUrl"
                    width="100%"
                    height="800px"
                    frameborder="0"
                    ref="iframe"
                ></iframe>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue';
export default defineComponent({
  setup() {
    const dashboardUrl = ref(
        'https://p.datadoghq.com/sb/eb4d74c2-eb97-11ec-b30d-da7ad0900002-a04b2cf16634bf73b900b8553c71e602'
    );
    const iframeRef = ref<HTMLIFrameElement | null>(null);
    const loading = ref(true);
    let interval: ReturnType<typeof setInterval> | null = null;
    const reloadIframe = () => {
      if (iframeRef.value) {
        loading.value = true; // 로딩 바 표시
        const tempSrc = iframeRef.value.src;
        iframeRef.value.src = '';
        iframeRef.value.onload = () => {
          // loading.value = false; // iframe 로드 완료 후 로딩 바 숨김
        };
      }
    };
    const onIframeLoaded = () => {
      loading.value = false; // Hide loading indicator
    };
    onMounted(() => {
      // interval = setInterval(reloadIframe, 60000); // 1분마다 새로고침

      setTimeout(() => {
        loading.value = false;
        reloadIframe();
      }, 4000);
    });
    onUnmounted(() => {
      if (interval) {
        clearInterval(interval);
      }
    });
    return {
      dashboardUrl,
      iframeRef,
      loading,
      onIframeLoaded,
    };
  },
});
</script>
<style scoped>
iframe {
  border: 0;
  width: 100%;
  height: 1000px;
}
</style>
