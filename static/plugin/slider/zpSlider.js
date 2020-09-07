/*
jQuery slider
by hamidZp
*/
(function($){
  $.fn.zpSlider = function(userOptions){
    var options = $.extend({
      slideTime: 5000,             // how long each slide stays on screen
      speed: 500,                  // slide transition speed
      outAnimation: 'random',      // swipeRight,swipeLeft,slide,fade,random
      inAnimation: 'random',       // swipeRight,swipeLeft,slide,fade,random
      pauseOnHover: true,          // pause when hovering with the mouse
      swipeSupport: true,          // support for swipe gestures (need jq.mobile)
      displayOrder: "sequential",  // sequential, random
      showCounter: true,           // slide page number at top left
      showCaption: true,           // show slide caption
      showNextPrev: true,          // show previous/next arrows
      showControls: true           // display slide number buttons
    },userOptions)

    function rand(start,end){
      var r = start + Math.floor(Math.random() * (end - start));
      return r
    }
    // start coding here ...
    var slider = $(this);
    var slides = slider.find('ul').children();
    var slideCount = slides.length;
    var i = 0; //current slide index;
    $(document).ready(function(){
       // add slide counter
       var counterTag = $('<div>').addClass('counter');
       if(options.showCounter){
         slider.append(counterTag);
         counterTag.html(slideCount + " / " + (i + 1))
       }
       // add slide caption
       var captionTag = $("<div>").addClass('sliderCaption');
       if(options.showCaption){
         slider.append(captionTag);
         if ($(slides[i]).is('[title]')){
           captionTag.html($(slides[i]).attr('title')).fadeIn(options.speed)
         }
       }
       // add showControls
       if(options.showControls){
         var buttonsRowTag = $('<div>').addClass('buttonsRow');
         for(var j = 0; j< slideCount ; j++){
           buttonsRowTag.append($('<span>').attr('data-sn',j).html(j + 1));
           slider.append(buttonsRowTag);
           slider.find('div.buttonsRow span').click(function(){
             var slideNumber = Number($(this).attr("data-sn"));
             if(slideNumber != i){
              showSlide(slideNumber)
             }
           })
         }
         $('div.buttonsRow span:eq(0)').addClass('curr')
       }
       // auto change slide
       var iv = setInterval(autoSlide,options.slideTime);

       function autoSlide(){
         if(options.displayOrder == "random"){
           var randomNumber = rand(0,slideCount-1)
           if(randomNumber == i){
             showSlide(randomNumber + 1);
           }else{
             showSlide(randomNumber);
           }
         }else {
           showSlide(i+1);
         }
       }
       // pause on hover
       if(options.pauseOnHover){
         slider.hover(function(){
           // stop
           clearInterval(iv)
         },function(){
           // start again
           iv = setInterval(autoSlide,options.slideTime);
         })
       }
       // swipe
       if(options.swipeSupport && $.fn.swipe){
         slider.on('dragstart',function(ev){
           ev.preventDefault()
         })
         slider.swiperight(function(){
           showSlide(i - 1,'swipeRight',"swipeRight")
         })
         slider.swipeleft(function(){
           showSlide(i + 1,'swipeLeft',"swipeLeft")
         })
       }
       // add navigation (next/prev) buttons
       var topDistance = slider.height()/2 - 20
       var nextTag = $('<i>').css({top:topDistance, position:"absolute", top:"50%", padding:"3px"}).addClass('next fa fa-caret-right')
       var prevTag = $('<i>').css({top:topDistance, position:"absolute", top:"50%", left:"0", padding:"3px"}).addClass('prev fa fa-caret-left')
       nextTag.css("fontSize", "24px")
       prevTag.css("fontSize", "24px")
       nextTag.addClass("slider_arrow")
       prevTag.addClass("slider_arrow")
       if (options.showNextPrev){
         slider.append(nextTag,prevTag);
         nextTag.click(function(){
           showSlide(i + 1)
         })
         prevTag.click(function(){
           showSlide(i - 1)
         })
       }

       function slideOut(customAnimation){
         var anim = (typeof customAnimation !== 'undefined')? customAnimation : options.outAnimation;
         if(anim == 'random'){
           var anims = ['fade', 'slide', 'swipeLeft', 'swipeRight'];
           anim = anims[rand(0,3)]
         }
         var slide = $(slides[i]);
         slide.addClass('current')
         switch (anim) {
           case 'slide':
             slide.slideUp(options.speed)
             break;
          case 'swipeRight':
             slide.animate({left:slider.width()},options.speed,function(){
               slide.css({left:0 , display:'none'})
             })
             break;
          case 'swipeLeft':
              slide.animate({left: -1 * slider.width()},options.speed,function(){
                slide.css({left:0 , display:'none'})
              })
              break;
          case 'fade':

              break;
          default:
              slide.fadeIn();
         }

         $(slides[i]).fadeOut();
       }
       function slideIn(customAnimation){
         var anim = (typeof customAnimation !== 'undefined')? customAnimation : options.inAnimation;
         if(anim == 'random'){
           var anims = ['fade', 'slide', 'swipeLeft', 'swipeRight'];
           anim = anims[rand(0,3)]
         }
         var slide = $(slides[i]);
         slide.removeClass('current')
         switch (anim) {
           case 'slide':
             slide.slideDown(options.speed)
             break;
          case 'swipeRight':
             slide.css({left:-1 * slider.width(),display:"list-item"})
             slide.animate({left:0},options.speed)
             break;
          case 'swipeLeft':
              slide.css({left:slider.width(),display:"list-item"})
              slide.animate({left:0},options.speed)
              break;
          case 'fade':

              break;
          default:
              slide.fadeIn();
         }

         $(slides[i]).fadeIn();
       }
       function showSlide(slideNumber,outAnimm,inAnim){
         slideOut(outAnimm);
         i = (slideNumber + slideCount) % slideCount;
         slideIn(inAnim)

         // show or fade caption
         if(options.showCaption){
           if($(slides[i]).is('[title]')){
             captionTag.html($(slides[i]).attr('title')).fadeIn(options.speed)
           }else {
             captionTag.html('').fadeOut(options.speed)
           }
         }
         // update counter text
         if(options.showCounter){
           counterTag.text(slideCount + " / " + (i + 1))
         }
         //
         if(options.showControls){
           slider.find('div.buttonsRow span').removeClass('curr')
           slider.find('div.buttonsRow span:eq(' + i + ')').addClass('curr')
         }
       }
    })
  }
})(jQuery)
