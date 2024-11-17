<template>
<!--  <section id="circle-mark" style="padding-top:100px; height:1000px">-->
  <section id="circle-mark">
      <div class="center-wrapper">
        <div class="circle-wrapper">
          <div class="success circle"></div>
          <div class="icon">
            <i class="fa fa-check"></i>
          </div>
        </div>

        <div class="circle-wrapper">
          <div class="warning circle"></div>
          <div class="icon">
            <i class="fa fa-exclamation"></i>
          </div>
        </div>

        <div class="circle-wrapper">
          <div class="error circle"></div>
          <div class="icon">
            <i class="fa fa-times"></i>
          </div>
        </div>
      </div>
  </section>
</template>

<script setup lang="ts">
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css');
@import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');

.center-wrapper {width: fit-content;margin: auto;}
.circle-wrapper {position: relative;width: 100px;height: 100px;float: left;margin: 10px;}
.icon {position: absolute;color: #fff;font-size: 55px;top: 50%;left: 50%;transform: translate(-50%, -50%);}
.circle {display: block;width: 100%;height: 100%;border-radius: 50%;padding: 2.5px;background-clip: content-box;animation: spin 10s linear infinite;}
.circle-wrapper:active .circle {animation: spin 2s linear infinite;}
.success {background-color: #4BB543;border: 2.5px dashed #4BB543;}
.error {background-color: #CA0B00;border: 2.5px dashed #CA0B00;}
.warning {background-color: #F0D500;border: 2.5px dashed #F0D500;}
@keyframes spin { 100% {transform: rotateZ(360deg);} }
.page-wrapper {height: 44vh; /*background-color: #eee;*/display: flex;align-items: center;justify-content: center;}
</style>
