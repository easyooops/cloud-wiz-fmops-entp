import { useCommonStore } from '~~/store/common';
export default{
    methods: {
        getImgUrl(path) {
          return ('/images/' + path);
        },
        say: function (message) {
          useCommonStore().active(message)
        },
        collapseFilter() {
          this.filtered = !this.filtered;
        },
        setFavourite(item) {
          useCommonStore().setFavourite(item)
        },
        getActive(itemId) {
          useCommonStore().getActive(itemId)
        },
        basic_warning_alert: function (item) {
          this.$swal({
            icon: 'warning', title: "Are you sure?", text: 'Once deleted, you will not be able to recover this imaginary file!',
            showCancelButton: true, confirmButtonText: 'Ok', confirmButtonColor: '#e64942', cancelButtonText: 'Cancel', cancelButtonColor: '#efefef',
          }).then((result) => {
            if (result.value) {
              this.bookmark.splice(item, 1)
              this.$swal({ icon: 'success', text: 'Poof! Your imaginary file has been deleted!', type: 'success', });
            } else {
              this.$swal({ text: 'Your imaginary file is safe!' });
            }
          });
        },
      },
}