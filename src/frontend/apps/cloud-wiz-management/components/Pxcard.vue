

<template>
  <div>
    <b-card :class="{ 'full-card': fullCard }">
      <template v-slot:header v-if="showHeader || useSlots().headerCustom">
        <h5 v-if="title">{{ title }}</h5>

        <div v-if="showAction">
          <slot name="headerAction">
            <div class="card-header-right">
              <ul class="list-unstyled card-option" :class="{ openaction: openActions }">
                <li>

                  <i class='fa fa-spin fa-cog'></i>
                </li>
                <li @click="openFullCard()">
                  <i class="icofont full-card" :class="fullCard ? 'icofont-resize' : 'icofont-maximize'"></i>
                </li>
                <li @click="toggleCard()">
                  <i class="icofont minimize-card" :class="cardToggle ? 'icofont-minus' : 'icofont-plus'"></i>
                </li>
              </ul>
            </div>
          </slot>
        </div>
        <slot name="headerCustom"></slot>
      </template>
      <div class="card-body p-0" v-if="useSlots().default"
        :style="cardToggle ? { 'display': 'block' } : { 'display': 'none' }">
        <div>
          <slot></slot>
        </div>
      </div>
      <div class="card-body" v-else :style="cardToggle ? { 'display': 'block' } : { 'display': 'none' }">

        <slot name="with-padding"></slot>

      </div>


      <template v-slot:footer v-if="useSlots().footer">
        <slot name="footer"></slot>
      </template>


      <slot name="custom-content"></slot>
    </b-card>

  </div>
</template>

<script>
export default {
  name: 'px-card',
  props: {
    title: String,
    actions: {
      type: Boolean,
      default: true,
    }
  },
  data() {
    return {
      openActions: false,
      fullCard: false,
      cardToggle: true
    };
  },

  computed: {
    showHeader() {
      return this.title;
    },
    showAction() {
    }
  },
  methods: {
    openCardActions() {
      this.openActions = !this.openActions;
    },
    openFullCard() {
      this.fullCard = !this.fullCard;
    },
    toggleCard() {
      this.cardToggle = !this.cardToggle;
    }
  }
};
</script>