<template>
  <div>
    <div class="container-fluid">
      <div class="row ">
        <div class="col-12 p-0">
          <div class="login-card">

            <div class="loader-overlay" v-if="loading">
                <div class="loader-box">
                    <div class="loader-30"></div>
                </div>
            </div> 

            <div>
              <div class="login-main">
                <form class="theme-form">
                  <h4>Sign in to account</h4>
                  <div class="mt-4">
                    <div class="social mt-4" id="googleButton"></div>
                  </div>
                </form>
                <div>
                  <a class="logo">
                    <img class="img-fluid" src="/images/wiz/logo-pink.png" alt="looginpage" width="300" />
                  </a>
                </div>                   
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { useAuthStore } from '@/store/auth';
import { mapActions } from 'pinia';

definePageMeta({
  layout: 'custom'
})

export default {
  name: 'login',
  data() {
    return {
      loading: false
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['loginWithGoogle']),
    async login() {
      if (this.user.name.value.trim() === '') {
        this.user.name.errormsg = 'Please enter your name.';
        return;
      }

      try {
        await this.loginWithGoogle({ name: this.user.name.value });
      } catch (error) {
        console.error('Login failed:', error);
      } finally {
      }
    },
    googleInitialize() {
      const config = useRuntimeConfig()
      const clientId = config.app.googleClientId;
      
      google.accounts.id.initialize({
        client_id: clientId,
        callback: this.handleCallback,
        context: 'use'
      })
      google.accounts.id.renderButton(
        document.getElementById('googleButton'),
        {
          type: 'standard',         // Button type: standard, icon
          theme:'filled_blue',      // Theme: outline, filled_blue, filled_black
          size: 'large',            // Button size: large, medium, small
          text: 'signin_with',      // Button text: signin_with, signup_with, continue_with, signIn
          shape: 'rectangular',     // Button shape: rectangular, pill, circle, square
          logo_alignment: 'center',
          width: 50,
        }
      )
    },
    async handleCallback(response){
      this.loading = true;
      try {              
        if (response && response.credential) {
          const token = response.credential
          // const base64Payload = token.split('.')[1]
          // const payload = atob(base64Payload);
          // const result = JSON.parse(payload);

          await this.loginWithGoogle(token)

          this.loading = false;
          this.$router.push('/');
          
        } else {
          console.error('No credential found in response');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false;
      }        
    }    
  },
  mounted() {
    this.googleInitialize()
  }
};
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