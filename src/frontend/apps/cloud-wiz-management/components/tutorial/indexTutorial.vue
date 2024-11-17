<template>
  <Breadcrumbs main="Tutorial" title="Play Video" />

  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <div class="card">
          <div class="card-body">
            <div class="form theme-form">
              <div class="row mt-3" v-if="videoUrl">
                <div class="col">
                  <video :src="videoUrl" controls class="w-100" autoplay></video>
                </div>
              </div>
            </div>
            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'VideoPlay',
  setup() {
    const videoUrl = ref('/vedio/vedio.mp4');
    const showVideo = ref(false);
    const errorMessage = ref(null);

    const playVideo = () => {
      if (videoUrl.value) {
        showVideo.value = true;
        errorMessage.value = null;
      } else {
        errorMessage.value = 'Please enter a valid video URL.';
        showVideo.value = false;
      }
    };

    return {
      videoUrl,
      showVideo,
      errorMessage,
      playVideo,
    };
  },
}
</script>

<style scoped>
video {
  max-width: 100%;
  height: auto;
}
</style>
