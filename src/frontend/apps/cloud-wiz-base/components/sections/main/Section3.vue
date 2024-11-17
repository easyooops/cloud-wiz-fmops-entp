<template>
  <section class="pt-100 ct-04 content-section division main-section-three">
    <div class="container">
      <!-- SECTION CONTENT (ROW) -->
      <div class="main-title-two">
        <h2 class="s-50 w-700 text-center main-text">지속 가능한 관리와 운영</h2><br><br>
        <h3 class="s-25 w-400 text-center main-text">지속 통합 가능한 관리, 통합된 관리 운영 시스템, 효율적인 관리와 운영.</h3><br><br>
      </div>
      <div class="row d-flex align-items-center">
        <!-- TEXT BLOCK -->
        <div class="col-md-6 order-last order-md-2">
          <div class="txt-block left-column wow fadeInRight">
            <!-- CONTENT BOX #1 -->
            <div class="cbox-2 process-step">
              <!-- Icon -->
              <div class="ico-wrap">
                <div class="cbox-2-ico bg--theme color--white">1</div>
                <span class="cbox-2-line"></span>
              </div>
              <!-- Text -->
              <div class="cbox-2-txt">
                <h5 class="s-22 w-700">Deployment</h5>
                <p>✔️ 하나의 “파이프라인”을 구성하여 생성된 모델에 대해 즉시 배포를 할 수 있게 구성되어 있습니다.</p>
                <p>✔️ 배포 후 즉시 모델에 대한 “검증 및 평가”에 대한 테스트를 진행 할 수 있습니다.</p>
                <p>✔️ “인프라” 배포는 “공용 호스팅/단독 호스팅”을 통해 안전한 서비스 격리 및 쉽고 빠른 서비스 배포를 구성할 수 있습니다.</p>
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
                <h5 class="s-22 w-700">CSP Provider</h5>
                <p>✔️ AWS BedRock / Azure AI Studio / Google AI 서비스를 활용한 서비스 구축 및 운영을 합니다.</p>
                <p>✔️ API / SDK 활용한 FMOps Builder 구축 합니다.</p>
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
                <h5 class="s-22 w-700">Prompt Chain</h5>
                <p class="mb-0">✔️ LangChain / Transformer API 활용한 LLM Builder 구축을 합니다.</p>
              </div>
            </div>
            <!-- END CONTENT BOX #3 -->
            <div class="dash-btn" >
              <a :href="baseUrl" class="btn r-04 btn--theme hover--tra-black">Get started for free</a>
            </div>
          </div>
        </div>
        <!-- END TEXT BLOCK -->
        <!-- IMAGE BLOCK -->
        <div class="col-md-6 order-first order-md-2">
          <div class="img-block wow fadeInLeft">
            <img class="img-fluid" src="/assets/images/wiz/main_image_3.png"  width="900px" alt="content-image" />
          </div>
        </div>
      </div>
      <!-- END SECTION CONTENT (ROW) -->
    </div>
    <!-- End container -->
  </section>

</template>

<script setup lang="ts">
const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';
</script>