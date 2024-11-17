<template>
  <section class="bg--white-400 py-100 ct-04 content-section division">
    <!-- POSTS WRAPPER -->
    <div class="posts-wrapper">
      <div class="container">
        <div class="main-title-two">
          <h2 class="s-50 w-700 text-center main-text">모니터링</h2><br><br>
          <h3 class="s-25 w-400 text-center main-text">LLM 사용량 및 비용 모니터링, 토큰 사용 및 비용 추적, 토큰 비용 효율성 모니터링</h3><br><br>
        </div>
        <div class="row d-flex align-items-center">
          <!-- IMAGE BLOCK -->
          <div class="col-md-6">
            <div class="img-block left-column wow fadeInRight">
              <img class="img-fluid" src="/assets/images/wiz/main_image_4.gif" width="600px" alt="content-image" />
            </div>
          </div>
          <!-- TEXT BLOCK -->
          <div class="col-md-6">
            <div class="txt-block right-column wow fadeInLeft main-section-two-txt">
              <!-- CONTENT BOX #1 -->
              <div class="cbox-2 process-step">
                <!-- Icon -->
                <div class="ico-wrap">
                  <div class="cbox-2-ico bg--theme color--white">1</div>
                  <span class="cbox-2-line"></span>
                </div>
                <!-- Text -->
                <div class="cbox-2-txt">
                  <h5 class="s-22 w-700">모니터링</h5>
                  <p>✔️ “인프라”에 대한 모니터링을 관제 합니다.</p>
                  <p>✔️ “토큰”사용에 따른 비용을 모니터링을 합니다.</p>
                  <p>✔️ 임계치 설정을 통해 “알람” 기능을 제공 합니다.</p>
                </div>
              </div>
              <!-- END CONTENT BOX #1 -->
              <!-- CONTENT BOX #2 -->
              <div class="cbox-2 process-step">
                <!-- Icon -->
                <div class="ico-wrap">
                  <div class="cbox-2-ico bg--theme color--white">2</div>
                  <span class="cbox-2-line"></span>
                </div>
                <!-- Text -->
                <div class="cbox-2-txt">
                  <h5 class="s-22 w-700">트레이스</h5>
                  <p>✔️ “에이전트”의 실시간 처리 과정에 대한 트레이스 로깅을 제공합니다.</p>
                  <p>✔️ “모델” 사용에 대한 로깅을 제공 합니다.</p>
                </div>
              </div>
              <!-- END CONTENT BOX #2 -->
            </div>
            <div class="dash-btn" >
              <a :href="baseUrl" class="btn r-04 btn--theme hover--tra-black">Get started for free</a>
            </div>
          </div>
          <!-- END TEXT BLOCK -->
      </div>
    </div>
    <!-- END POSTS WRAPPER -->
    </div>
  </section>
</template>

<script setup lang="ts">
const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';
</script>