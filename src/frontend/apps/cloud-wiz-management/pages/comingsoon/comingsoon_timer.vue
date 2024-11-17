<template>
  <div>
    <ul>
      <li><span class="time digits">{{ days }}</span><span class="title">days</span></li>
      <li><span class="time digits" v-text="hours"></span><span class="title">Hours</span></li>
      <li><span class="time digits" v-text="minutes"></span><span class="title">Minutes</span></li>
      <li><span class="time digits" v-text="seconds"></span><span class="title">Seconds</span></li>
    </ul>
  </div>
</template>

 
<script>

export default {
  data() {
    return {
      td: 0,
      days: 0,
      hours: 0,
      minutes: 0,
      seconds: 0,
      startTime: '',
      endTime: '',
    };
  },
  mounted() {
    this.timer()

  },
  methods: {
    timer() {
      setInterval(() => {
        this.endTime = new Date().getTime()
        this.startTime = new Date('Apr 29, 2021 00:00:00').getTime(),
          this.td = this.endTime - this.startTime
        if (this.td >= 0) {
          this.seconds = Math.floor(this.td / 1000 % 60);
          this.minutes = Math.floor(this.td / 1000 / 60 % 60);
          this.hours = Math.floor(this.td / (1000 * 60 * 60) % 24);
          this.days = Math.floor(this.td / (1000 * 60 * 60 * 24));
        } else {
          this.seconds = this.minutes = this.hours = this.days = 0;
        }
      });


    }
  },
  beforeUnmount() {

    clearInterval(this.timer())
  },

}
</script>
