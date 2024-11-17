export default{
    data(){
        return{
          myimgSrc:'img-cropper.jpg',
          imgSrc:'',
          imageData:'',
          containerData:'',
          putData:'',
          viewmodeselected:0,
          cropImg: '',
          viewmodeOptions: [
            { text: 'VM0', value: 0 },
            { text: 'VM1', value: 1 },
            { text: 'VM2', value: 2 },
            { text: 'VM3', value: 3 },
          ],
          aspectRatioselected:1.7777777777777777,
          aspectRatioOptions: [
            { text: '16:9', value: 1.7777777777777777 },
            { text: '4:3', value: 1.3333333333333333 },
            { text: '1:1', value: 1 },
            { text: '2:3', value: 0.6666666666666666 },
            { text: 'Free', value: NaN }
          ]
        };
      },
      mounted(){
        this.imageData = this.$refs.cropper.getData();
      },
      methods:{
        getImgUrl() {
          var images = `require.context('/images/other-images/', false, /\.jpg$/)`;
          return ('/images/other-images/' + this.myimgSrc);
        },
        ready(){
          this.containerData = this.$refs.cropper.getContainerData();
        },
        cropImage(){
          this.imageData = this.$refs.cropper.getData();
          this.cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL(); 
        },
        moveImage(){
          this.$refs.cropper.move(1);
        },
        zoominImage(){
          this.$refs.cropper.zoomTo(0.5);
        },
        zoomoutImage(){
          this.$refs.cropper.zoomTo(0);
        },
        zoom100(){
          this.$refs.cropper.zoomTo(1);
        },
        moveImageLeft(){
          this.$refs.cropper.move(-10,0);
        },
        moveImageRight(){
          this.$refs.cropper.move(10,0);
        },
        moveImageUp(){
          this.$refs.cropper.move(0,10);
        },
        moveImageDown(){
          this.$refs.cropper.move(0,-10);
        },
        moveImageTo(){
          this.$refs.cropper.moveTo(0);
        },
        rotateLeft(){
          this.$refs.cropper.rotate(-45);
        },
        rotateRight(){
          this.$refs.cropper.rotate(45);
        },
        rotate180(){
          this.$refs.cropper.rotateTo(180);
        },
        fliphorizontal(){
          if(this.imageData.scaleX === 1) {
            this.$refs.cropper.scale(-1, 1);
          } else {
            this.$refs.cropper.scale(1, 1);
          }
        },
        flipvertical(){      
          if(this.imageData.scaleY === 1) {
            this.$refs.cropper.scale(1, -1);
          } else {
            this.$refs.cropper.scale(1, 1);
          }
        },
        scaleImage(){
          this.$refs.cropper.scale(-2, -1);
        },
        clear(){
          this.$refs.cropper.clear();
        },
        disable(){
          this.$refs.cropper.disable();
        },
        enable(){
          this.$refs.cropper.enable();
        },
        reset(){
          this.$refs.cropper.reset();
        },
        destroy(){
          this.$refs.cropper.destroy();
        },
        imageUpload(){
          
        },
        getCroppedCanvas(){
          this.$refs.getCroppedCanvasModal.show();
        },
        getCroppedCanvas4096(){
          this.$refs.getCroppedCanvas4096.show();
        },
        getCroppedCanvas16090(){
          this.$refs.getCroppedCanvas16090.show();
        },
        getCroppedCanvas320180(){
          this.$refs.getCroppedCanvas320180.show();
        },
        getCropperdata(){
          var data = this.$refs.cropper.getData();
          this.putData = '{"x":'+data.x+',"y":'+data.y+',"width":'+data.width+',"height":'+data.height+',"rotate":'+data.rotate+',"scaleX":'+data.scaleX+',"scaleY":'+data.scaleY+'}';
        },
        getContainerdata(){
          var data = this.$refs.cropper.getContainerData();
          this.putData = '{"width":'+data.width+',"height":'+data.height+'}';
        },
        getImagedata(){
          var data = this.$refs.cropper.getImageData();
          this.putData = '{"naturalWidth":'+data.naturalWidth+',"naturalHeight":'+data.naturalHeight+',"aspectRatio":'+data.aspectRatio+',"width":'+data.width+',"height":'+data.height+',"left":'+data.left+',"top":'+data.top+'}';
        },
        getCanvasData(){
          var data = this.$refs.cropper.getCanvasData();
          this.putData = '{"left":'+data.left+',"top":'+data.top+',"width":'+data.width+',"height":'+data.height+',"naturalWidth":'+data.naturalWidth+',"naturalHeight":'+data.naturalHeight+'}';
        },
        getCropBoxData(){
          var data = this.$refs.cropper.getCropBoxData();
          this.putData = '{"left":'+data.left+',"top":'+data.top+',"width":'+data.width+',"height":'+data.height+'}';
        }
      }
}