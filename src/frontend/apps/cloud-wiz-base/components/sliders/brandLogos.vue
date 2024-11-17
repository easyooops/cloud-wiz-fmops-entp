<template>
    <div class="brands-carousel-5">
        <Swiper
            :modules="[SwiperAutoplay, SwiperEffectCreative]"
            :slides-per-view="2"
            :loop="true"
            :autoplay="{
                delay: 8000,
                disableOnInteraction: true
            }"
            :breakpoints="{
                400:{ slidesPerView:2 },
                600:{ slidesPerView:3 },
                900:{ slidesPerView:4, },
                1024:{ slidesPerView:5, },
            }"
        >
            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-1.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-1-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-2.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-2-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-3.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-3-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-4.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-4-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-5.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-5-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-6.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-6-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-7.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-7-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-8.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-8-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>

            <SwiperSlide>
                <div class="brand-logo">
                    <img class="img-fluid theme-light" src="/assets/images/brand-9.png" alt="brand-logo" />
                    <img class="img-fluid theme-dark" src="/assets/images/brand-9-white.png" alt="brand-logo" />
                </div>
            </SwiperSlide>
        </Swiper>
    </div>
</template>
