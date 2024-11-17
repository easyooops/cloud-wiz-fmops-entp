export default{
    data() {
        return {
            enterAnimation:'',
            exitAnimation:'',
            show:false,
            showd:false,
         animate: false,
            active: false,
            animationList: [
        "bounce",
        "flash",
        "flip",
        "headShake",
        "hinge",
        "jello",
        "pulse",
        "rubberBand",
        "shake",
        "swing",
        "tada",
        "wobble",
        "bounceIn",
        "bounceInDown",
        "bounceInLeft",
        "bounceInRight",
        "bounceInUp",
        "fadeIn",
        "fadeInDown",
        "fadeInDownBig",
        "fadeInLeft",
        "fadeInLeftBig",
        "fadeInRight",
        "fadeInRightBig",
        "fadeInUp",
        "fadeInUpBig",
        "flipInX",
        "flipInY",
        "lightSpeedIn",
        "rollIn",
        "rotateIn",
        "rotateInDownLeft",
        "rotateInDownRight",
        "rotateInUpLeft",
        "rotateInUpRight",
        "slideInDown",
        "slideInLeft",
        "slideInRight",
        "slideInUp",
        "zoomIn",
        "zoomInDown",
        "zoomInLeft",
        "zoomInRight",
        "zoomInUp",
        "bounceOut",
        "bounceOutDown",
        "bounceOutLeft",
        "bounceOutRight",
        "bounceOutUp",
        "fadeOut",
        "fadeOutDown",
        "fadeOutDownBig",
        "fadeOutLeft",
        "fadeOutLeftBig",
        "fadeOutRight",
        "fadeOutRightBig",
        "fadeOutUp",
        "fadeOutUpBig",
        "flipOutX",
        "flipOutY",
        "lightSpeedOut",
        "rollOut",
        "rotateOut",
        "rotateOutDownLeft",
        "rotateOutDownRight",
        "rotateOutUpLeft",
        "rotateOutUpRight",
        "slideOutDown",
        "slideOutLeft",
        "slideOutRight",
        "slideOutUp",
        "slideOutRight",
        "zoomOut",
        "zoomOutDown",
        "zoomOutLeft",
        "zoomOutRight",
        "zoomOutUp"
      ]
        }
    },
    methods: {
        isActive(path) {
            this.animate = path
            document.getElementById("mod").className = `modal-dialog ${path} animated`
        },
        close() {

            document.getElementById("mod").className = `modal-dialog ${this.exitAnimation} animated`
            },
            selectAnimate(enterAnimation) {
                this.show = enterAnimation;
                setTimeout(function(){
                  setTimeout(function(){
              var element = document.getElementById("animation-box");
           
            element.classList.remove(`${enterAnimation}`)},
             1000)
              
              var element = document.getElementById("animation-box");
            element.classList.remove("animated");
            
            },
             500)},
            selectAnimated() {
                  var element = document.getElementById("animation-box");
            element.classList.add("animated");
            element.classList.add(`${this.enterAnimation}`)
            },          
        
    },
    computed: {
        enterClass() {
          return `${this.enterAnimation} animated`;
        }
    }
}