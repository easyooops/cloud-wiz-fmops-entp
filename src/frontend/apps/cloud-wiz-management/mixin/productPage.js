import { useProductStore } from '~~/store/product';

export default{
    data() {
        return {
          counter: 1,
          modalShow: false,
          activeTab: 'fabric',
          
        };
      },
      computed: {
        products() {
            return useProductStore().products.find((item) => {
                if (parseInt(useRouter().currentRoute._rawValue.params.id) === item.id) return item;
              })
            },
             swiper() {
          return this.$refs.mySwiper.swiper;
        },
      },
  
      methods: {
        getImgUrl(path) {
          return require('/images/' + path);
        },
        slideTo(id) {
          this.swiper.slideTo(id, 1000, false);
        },
        addToCart: function (product, qty) {
          product.quantity = qty ? qty : 1;
          this.$store.dispatch('products/addToCart', product);
        },
        increment() {
          if (this.counter < this.quickViewProduct.stock) this.counter++;
        },
        decrement() {
          if (this.counter > 1) this.counter--;
        },
        tabContent(val) {
          this.activeTab = val;
        },
      },
}