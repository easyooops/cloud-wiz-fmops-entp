<template>
  <div class="page-wrapper compact-wrapper" id="pageWrapper">
    <!-- error-500 start-->
    <div class="error-wrapper">
      <div class="container"><img class="img-100" src="/images/other-images/sad.png" alt="">
        <div class="error-heading">
          <h2 class="headline font-primary">500</h2>
        </div>
        <div class="col-md-8 offset-md-2">
          <p class="sub-content">The page you are attempting to reach is currently not available. This may be because the
            page does not exist or has been moved.</p>
        </div>
        <div><router-link class="btn btn-primary-gradien btn-lg" to="/">BACK TO HOME PAGE</router-link></div>
      </div>
    </div>
    <!-- error-500 end-->
  </div>
</template>
<script>
definePageMeta({
  layout: "custom",
});

</script>