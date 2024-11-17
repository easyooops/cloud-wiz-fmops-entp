<template>
  <Breadcrumbs main="Opinion" title="Create Opinion" />

  <div class="container-fluid">
    <div class="loader-overlay" v-if="loading">
      <div class="loader-box">
        <div class="loader-30"></div>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12">
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="handleSubmit">
              <div class="form theme-form">
                <div class="row">
                  <div class="col">
                    <div class="mb-3">
                      <h4><label>Title</label></h4>
                      <input v-model="title" class="form-control" type="text" placeholder="Title *" required>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col">
                    <div class="mb-3">
                      <h4><label>Opinion</label></h4>
                      <textarea v-model="content" class="form-control" rows="20" placeholder="Content *" required></textarea>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col">
                    <button type="submit" class="btn btn-primary me-2">Submit</button>
                    <!-- <router-link to="/opinions" class="btn btn-secondary">Back to List</router-link> -->
                  </div>
                </div>
              </div>
            </form>
            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
            <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useOpinionStore } from '@/store/opinions';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'OpinionCreate',
  setup() {
    const opinionStore = useOpinionStore();
    const authStore = useAuthStore();
    const router = useRouter();
    const title = ref('');
    const content = ref('');
    const loading = ref(false);
    const errorMessage = ref(null);
    const successMessage = ref(null);

    const handleSubmit = async () => {
      loading.value = true;
      errorMessage.value = null;
      successMessage.value = null;

      try {
        const userId = authStore.userId;
        await opinionStore.createOpinion({
          title: title.value,
          content: content.value,
          creator_id: userId,
          updater_id: userId,
        });
        successMessage.value = 'Opinion created successfully.';
      } catch (error) {
        errorMessage.value = 'An error occurred while creating the opinion.';
      } finally {
          loading.value = false;
          setTimeout(() => {
            successMessage.value = '';
            successMessage.value = '';
          }, 2000);  
      }
    };

    return {
      title,
      content,
      loading,
      errorMessage,
      successMessage,
      handleSubmit,
    };
  },
}
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 검정색 배경, 투명도 조절 가능 */
  z-index: 999; /* 로딩 오버레이가 최상위에 오도록 설정 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-box {
  width: 100px; /* 로딩 바의 너비 설정 */
  height: 100px; /* 로딩 바의 높이 설정 */
  background-color: #fff; /* 로딩 바의 배경색 */
  border-radius: 10px; /* 로딩 바 모서리 둥글게 */
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.5); /* 로딩 바에 그림자 효과 추가 */
}
</style>
