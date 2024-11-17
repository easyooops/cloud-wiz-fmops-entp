<template>
  <section id="hero-15" class="bg--scroll hero-section">
      <div class="container">
          <div class="row d-flex align-items-center">
              <!-- HERO TEXT -->
              <div class="col-md-6">
                  <div class="hero-15-txt wow fadeInRight">
                      <!-- Title -->
                      <h2 class="s-55 w-700">미래를 여는 LLM 기반 AI 플랫폼</h2>
                      <!-- Text -->
                      <p class="p-lg">노코드 기반의 쉬운 UI로 누구나 AI를 만들 수 있습니다. 지속적으로 발전하는 LLM 모델을 활용하여 시장 변화에 빠르게 대응하고 다양한 산업에 창의적인 솔루션을 제공합니다.</p>
                      <!-- Button -->
                      <a :href="baseUrl" class="btn r-04 btn--theme hover--tra-black">Get started for free</a>
                  </div>
              </div>
              <!-- END HERO TEXT -->
              <!-- HERO IMAGE -->
              <div class="col-md-6">
                  <div class="hero-15-img text-center wow fadeInLeft">
                      <img class="img-fluid" src="/assets/images/hero-15-img.png" alt="hero-image" />
                  </div>
              </div>
          </div>
          <!-- End row -->
      </div>
      <!-- End container -->
  </section>
</template>

<script setup lang="ts">

import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';

// const scrollSections = ref([])
// const currentSectionIndex = ref(0)
//
// const scrollToSection = (index) => {
//   if (index >= 0 && index < scrollSections.value.length) {
//     let totalOffset = 0;
//
//     // 현재 섹션까지의 높이 누적 계산
//     for (let i = 0; i < index; i++) {
//       totalOffset += scrollSections.value[i].offsetHeight;
//     }
//
//     window.scrollTo({ top: totalOffset, behavior: 'smooth' });
//     console.log('이동');
//   }
// }
//
// const handleScroll = () => {
//   const windowHeight = window.innerHeight
//
//   // 현재 보이는 섹션 감지
//   for (let i = 0 ; i < scrollSections.value.length ; i++) {
//     const section = scrollSections.value[i]
//     const sectionTop = section.getBoundingClientRect().top
//
//     if (sectionTop >= 0 && sectionTop < windowHeight / 2) {
//       currentSectionIndex.value = i
//       break
//     }
//   }
// }


// onMounted(() => {
//   scrollSections.value = Array.from(document.querySelectorAll('._scrollto'))
//   window.addEventListener('scroll', handleScroll)
// })
//
// onBeforeUnmount(() => {
//   window.removeEventListener('scroll', handleScroll)
// })

// watch(currentSectionIndex, (newIndex) => {
//   // 현재 섹션이 변경될 때마다 해당 섹션으로 스크롤
//   scrollToSection(newIndex)
//   console.log(newIndex)
// })



</script>
