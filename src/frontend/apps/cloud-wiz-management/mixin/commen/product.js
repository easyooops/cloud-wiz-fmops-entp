import { useProductStore } from '~~/store/product'
import { mapState } from 'pinia'
export default{
    data() {
        return {
            isActive: false,
            modalShow: false,
            quickViewProduct: [],
            counter: 1,
            priceArray: [],
            allfilters: [],
            items: [],
            filtered: false,
        }
    },
    computed: {
        ...mapState(useProductStore, {
            products: 'products',
            productslist: 'productslist',
        }),
        tags() {
            return useProductStore().setTags
        },
        name() {
            return useProductStore().col2
        },
        col3() {
            return useProductStore().col3
        },
        col4() {
            return useProductStore().col4
        },
        col6() {
            return useProductStore().col6
        },
        listViewEnable() {
            return useProductStore().listViewEnable
        },
        filterPage() {
            return useProductStore().filterProducts
        }
    },
    mounted() {
       
    },
    methods: {
        grid2() {
            useProductStore().grid2(true)
        },
        grid3() {
            useProductStore().grid3()
        },
        grid4() {
            useProductStore().grid4()
        },
        grid6() {
            useProductStore().grid6()
        },
        listView() {
            useProductStore().listView()
        },
        gridView() {
            useProductStore().grid6()
        },
        disp() {
            this.isActive = !this.isActive
        },
        getImgUrl(path) {
            return ("/images/" + path);
        },
        addToCart: function (product, qty) {
            product.quantity = qty ? qty : 1;
            useProductStore().addToCart(product)
        },
        quickView: function (product) {
            return (this.quickViewProduct = product);
        },
        quickViewClose: function () {
            this.modalShow = false;
        },
        increment() {
            if (this.counter < this.quickViewProduct.stock) this.counter++;
        },
        decrement() {
            if (this.counter > 1) this.counter--;
        },
    }
}