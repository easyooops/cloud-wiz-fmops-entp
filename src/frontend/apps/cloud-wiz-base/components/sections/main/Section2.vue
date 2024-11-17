<template>
  <!-- POSTS WRAPPER -->
  <section class="bg--white-400 py-100 ct-04 content-section division">
    <div class="container">
      <!-- SECTION CONTENT (ROW) -->
      <div class="main-title-two">
        <h2 class="s-50 w-700 text-center main-text">쉬운 LLM 솔루션</h2><br><br>
        <h3 class="s-25 w-400 text-center main-text">노코드 기반 쉬운 UI/UX. 쉽게 만드는 맞춤형 AI. 코딩 없이 손쉽게 AI 구현</h3><br><br>
      </div>
      <div class="row d-flex align-items-center">
        <!-- IMAGE BLOCK -->
        <div class="col-md-6">
          <div class="img-block wow fadeInRight">
            <img class="img-fluid" src="/assets/images/wiz/main_image_2.gif" width="600px" alt="content-image" />
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
                <h5 class="s-22 w-700">Agent</h5>
                <p>✔️ “빌더 구성” 을 위한 “노코드” 기반 ”쉬운 UI/UX” 를 제공 합니다.</p>
                <p>✔️ 타사 Builder 보다 더욱 간소화 된 “UI/UX” 를 제공 합니다.</p>
                <p>✔️ “비개발자”도 다룰수 있는 간소화된 “UI/UX” 및 길잡이 역할에 도움을 드립니다.</p>
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
                <h5 class="s-22 w-700">Compare</h5>
                <p>✔️ “생성된 모델 비교”를 통한 “데이터 정합성”을 추론 할 수 있습니다.</p>
                <p>✔️ 모델 사용에 따른 결과 데이터에 대한 토큰 대비 “예상 비용”을 비교할 수 있습니다.</p>
              </div>
            </div>
            <!-- END CONTENT BOX #2 -->
            <!-- CONTENT BOX #3 -->
            <div class="cbox-2 process-step">
              <!-- Icon -->
              <div class="ico-wrap">
                <div class="cbox-2-ico bg--theme color--white">3</div>
              </div>
              <!-- Text -->
              <div class="cbox-2-txt">
                <h5 class="s-22 w-700">Processing</h5>
                <p>✔️ 직관성 높은 “쉬운” 전처리/후처리 기능을 제공 합니다.</p>
                <p>✔️ 나만의 “커스텀 템플릿” 만들어 다른 조직원과 공유가 가능하게 합니다.</p>
              </div>
            </div>
            <!-- END CONTENT BOX #3 -->
            <div class="dash-btn" >
              <a :href="baseUrl" class="btn r-04 btn--theme hover--tra-black">Get started for free</a>
            </div>             
          </div>
        </div>
        <!-- END TEXT BLOCK -->
      </div>
      <!-- END SECTION CONTENT (ROW) -->
    </div>
    <!-- End container -->
  </section>
</template>

<script setup lang="ts">
const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';
</script>