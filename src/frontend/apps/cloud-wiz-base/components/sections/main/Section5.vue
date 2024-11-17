<template>
  <section id="banner-7" class="banner-section">
      <div class="banner-overlay py-100">
          <div class="container">
              <!-- BANNER-7 WRAPPER -->
              <div class="banner-7-wrapper">
                  <div class="row justify-content-center">
                      <!-- BANNER-7 TEXT -->
                      <div class="col-md-8">
                          <div class="banner-7-txt text-center">
                              <!-- Title -->
                              <h2 class="s-50 w-700">Starting with Cloudwiz AI FMOps is easy, fast and free</h2>
                              <!-- Buttons -->
                              <div class="btns-group">
                                  <a :href="baseUrl" class="btn r-04 btn--theme hover--tra-black">Get srarted - it's free</a>
                                  <NuxtLink to="/consulting/contact-us" class="btn r-04 btn--tra-black hover--theme">Contact-Us</NuxtLink>
                              </div>
                              <!-- Button Text -->
                              <p class="btn-txt ico-15">Only Free - no credit card required.</p>
                          </div>
                      </div>
                  </div>
                  <!-- End row -->
              </div>
              <!-- END BANNER-7 WRAPPER -->
          </div>
          <!-- End container -->
      </div>
      <!-- End banner overlay -->
  </section>
</template>

<script setup lang="ts">
const baseUrl = import.meta.env.VITE_MANAGEMENT_URL || '/';
</script>