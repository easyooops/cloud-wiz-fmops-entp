<template>
    <div class="col-xl-3 xl-40 box-col-12">
      <div class="md-sidebar">
        <a class="btn btn-primary email-aside-toggle md-sidebar-toggle" @click="isOpen">Job filter</a>
        <div class="md-sidebar-aside job-sidebar" :class="open ? 'open' : ''">
          <div class="default-according style-1 faq-accordion job-accordion">
            <div class="accordion" id="accordionExample">

                <div class="card">
                    <div class="card-header" id="headingOne">
                        <h2 class="mb-0">
                            <button class="btn btn-link btn-block text-start" type="button" data-bs-target="#collapseOne"
                                :aria-expanded="active ? 'false' : 'true'" aria-controls="collapseOne" @click="showOpen">Filter</button>
                        </h2>
                    </div>
                    <div class="collapse " :class="active ? '' : 'show'" id="collapseOne" aria-labelledby="headingOne"
                        data-bs-parent="#accordionExample">
                        <div class="card-body filter-cards-view animate-chk">
                            <div class="job-filter mb-2">
                                <div class="faq-form">
                                    <input class="form-control" type="text" placeholder="Search.."><i class="search-icon"
                                        data-feather="search"></i>
                                </div>
                            </div>
                            <div class="checkbox-animated">
                                <label class="d-block" for="chk-ani">
                                    <input class="checkbox_animated" id="chk-ani" type="checkbox">Default Chat Type
                                </label>
                                <label class="d-block" for="chk-ani1">
                                    <input class="checkbox_animated" id="chk-ani1" type="checkbox">Default Text Type
                                </label>
                                <label class="d-block" for="chk-ani2">
                                    <input class="checkbox_animated" id="chk-ani2" type="checkbox">Default Embedding Type
                                </label>
                            </div>
                            <button class="btn btn-primary text-center" type="button">Find Agents</button>
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
  export default {
    components: {
      
    },
    methods: {
      isOpen() {
        this.open = !this.open
      },
      showOpen() {
        this.active = !this.active
      },
      showOpen1() {
        this.active1 = !this.active1
      },
    },
    data() {
      return {
        open: false,
        active: false,
        active1: false,
      }
    }
  }
  </script>